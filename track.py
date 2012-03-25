from SimpleCV import *
import glob
import time
import numpy
import operator

class Track:
    def __init__(self):
        self.ID = 0
        self.center = (0, 0)
        self.minX = 0
        self.maxX = 0
        self.minY = 0
        self.maxY = 0
        self.width = 0
        self.height = 0
        self.color = (0, 0, 0)
        mark_as_match = False

def get_overlap_area(minx1, miny1, maxx1, maxy1, minx2, miny2, maxx2, maxy2):
    if minx1 > maxx2 or maxx1 < minx2 or miny1 > maxy2 or maxy1 < miny2:
        return 0
    else:
        return (min(maxx2, maxx1) - max(minx2, minx1)) * (min(maxy2, maxy1) - max(miny2, miny1))

def get_color_similarity(hue1, hue2):
    return abs(hue1 - hue2)

# sort files by name because the resulting list is in arbitrary order.
files = sorted(glob.glob('images/*.jpg'))

# list of tracks
track_list = []
track_id = 0

for file in files:
    img = Image(file)

    # remove noise then find blobs in the clean image
    blobs = img.morphOpen().morphClose().findBlobs(10)

    # if there are blobs detected
    if blobs:
        if not track_list:
            for b in blobs:
                t = Track()
                track_id = track_id + 1
                t.ID = track_id
                # throw out the remainder
                # meanColor() returns BGR space, so need to reverse to RGB
                t.color = tuple([int(b.meanColor()) 
                    if isinstance(b.meanColor(), float) else int(x) 
                    for x in reversed(b.meanColor())])
                t.center = b.center()
                t.minX = b.minX()
                t.maxX = b.maxX()
                t.minY = b.minY()
                t.maxY = b.maxY()
                t.width = b.maxX() - b.minX()
                t.height = b.maxY() - b.minY()
                track_list.append(t)

        else:
            matrix = numpy.zeros((len(track_list), len(blobs)))
            for i in range(len(track_list)):
                for j in range(len(blobs)):
                    # create a correspondence matrix
                    print 'minX1: ' + str(track_list[i].minX)
                    print 'maxX1: ' + str(track_list[i].maxX)
                    print 'minY1: ' + str(track_list[i].minY)
                    print 'maxY1: ' + str(track_list[i].maxY)
                         
                    print 'minX2: ' + str(blobs[j].minX())
                    print 'maxX2: ' + str(blobs[j].maxX())
                    print 'minY2: ' + str(blobs[j].minY())
                    print 'maxY2: ' + str(blobs[j].maxY())
                    
                    matrix[i][j] = get_overlap_area(
                        track_list[i].minX, track_list[i].minY,
                        track_list[i].maxX, track_list[i].maxY,
                        blobs[j].minX(), blobs[j].minY(), 
                        blobs[j].maxX(), blobs[j].maxY())

                    print matrix[i][j]
            
            print 'matrix:'
            for i in range(len(track_list)):
                for j in range(len(blobs)):
                    print str(matrix[i][j]),
                print '\n'

            for i in range(len(track_list)):
                print 'processing on track ' + str(i)
                matched_blob_idx = []
                track_list[i].mark_as_match = False
                for j in range(len(blobs)):
                    if matrix[i][j] >= 100:
                        matched_blob_idx.append(j)

                # splitting
                if len(matched_blob_idx) > 1:
                    print 'blob splitting' + str(matched_blob_idx)
                    px = Image((1, 1), ColorSpace.RGB)
                    px[0, 0] = track_list[i].color
                    pxHSV = px.toHSV()
                    hue1 = pxHSV[0, 0][2]

                    print 'track ' + str(i) + ': ' + str(hue1)
                    min_diff = 10000
                    best_match_idx = -1
                    for idx in matched_blob_idx:
                        px[0, 0] = blobs[idx].meanColor()
                        pxHSV = px.toHSV()
                        hue2 = pxHSV[0, 0][2]

                        color_similarity = get_color_similarity(hue1, hue2)
                        print 'blob ' + str(idx) + ': ' + str(hue2)
                        print 'track ' + str(i) + ' and blob ' + str(idx) + ': ' + str(color_similarity)

                        if min_diff > color_similarity:
                            min_diff = color_similarity
                            best_match_idx = idx

                    print 'best macth for track: ' + str(i) + ' is ' + str(best_match_idx)
                    if not track_list[i].mark_as_match:
                        track_list[i].center = blobs[best_match_idx].center()
                        track_list[i].minX = blobs[best_match_idx].minX()
                        track_list[i].maxX = blobs[best_match_idx].maxX()
                        track_list[i].minY = blobs[best_match_idx].minY()
                        track_list[i].maxY = blobs[best_match_idx].maxY()
                        track_list[i].mark_as_match = True

                elif len(matched_blob_idx) == 1:
                    if not track_list[i].mark_as_match:
                        track_list[i].mark_as_match = True

            for j in range(len(blobs)):
                matched_track_idx = []
                for i in range(len(track_list)):
                    if matrix[i][j] >= 100:
                        matched_track_idx.append(i)

                # merging (only center is updated)
                if len(matched_track_idx) > 1:
                    print 'tracks merging: ' + str(matched_track_idx)
                    for idx in matched_track_idx:
                        track_list[idx].center = tuple(map(operator.div, 
                            tuple(map(operator.add, track_list[idx].center, 
                            blobs[j].center())), (2, 2)))
#                        track_list[idx].minX = track_list[idx].minX + (track_list[idx].center[0] + blobs[j].center()[0])/2
#                        track_list[idx].maxX = track_list[idx].maxX + (track_list[idx].center[0] + blobs[j].center()[0])/2
#                        track_list[idx].minY = track_list[idx].minY + (track_list[idx].center[1] + blobs[j].center()[1])/2
#                        track_list[idx].maxY = track_list[idx].maxY + (track_list[idx].center[1] + blobs[j].center()[1])/2

                elif len(matched_track_idx) == 1:
                    if track_list[matched_track_idx[0]].mark_as_match: 
                        track_list[matched_track_idx[0]].center = blobs[j].center()
                        track_list[matched_track_idx[0]].minX = blobs[j].minX()
                        track_list[matched_track_idx[0]].maxX = blobs[j].maxX()
                        track_list[matched_track_idx[0]].minY = blobs[j].minY()
                        track_list[matched_track_idx[0]].maxY = blobs[j].maxY()

        for b in blobs:    
            layer = DrawingLayer((img.width, img.height))
            rect_dim = (b.maxX() - b.minX(),
                b.maxY() - b.minY())
            center = b.center()
            layer.centeredRectangle(center, rect_dim, Color.WHITE)
            img.addDrawingLayer(layer)

    for t in track_list:
        print t.center

    for i in range(len(track_list)):
        layer = DrawingLayer((img.width, img.height))
        rect_dim = (track_list[i].maxX - track_list[i].minX,
            track_list[i].maxY - track_list[i].minY)
        center = track_list[i].center
        layer.centeredRectangle(center, rect_dim, track_list[i].color)
        img.addDrawingLayer(layer)
    
    img.applyLayers()
    img.show()

    raw_input()

    img.clearLayers()
    
    time.sleep(1)

