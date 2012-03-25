from SimpleCV import *
import glob
import time
import numpy
import operator

def get_overlap_area(minx1, miny1, maxx1, maxy1, minx2, miny2, maxx2, maxy2):
    if minx1 > maxx2 or maxx1 < minx2 or miny1 > maxy2 or maxy1 < miny2:
        return 0
    else:
        return (min(maxx2, maxx1) - max(minx2, minx1)) * (min(maxy2, maxy1) - max(miny2, miny1))

def get_color_dissimilarity(hue1, hue2):
    return abs(hue1 - hue2)

class Track:
    def __init__(self):
        self.ID = 0
        self.color = (0, 0, 0)
        self.blobs = []
        self.mark_as_match = False

# sort files by name because the resulting list is in arbitrary order.
files = sorted(glob.glob('images/*.jpg'))

tracks = []
track_id = 0
overlap_th = 160

for file in files:
    img = Image(file)

    # remove noise then find blobs in the clean image
    blobs = img.morphOpen().morphClose().findBlobs(10)

    # if there are blobs detected
    if blobs:
        if not tracks:
            for b in blobs:
                t = Track()
                track_id = track_id + 1
                t.ID = track_id
                # meanColor() returns BGR space, so need to reverse to RGB (also, throw out the remainder)
                t.color = tuple([int(b.meanColor()) if isinstance(b.meanColor(), float) else int(x) for x in reversed(b.meanColor())])
                t.blobs.append(b)
                tracks.append(t)

        else:
            matrix = numpy.zeros((len(tracks), len(blobs)))
            for i in range(len(tracks)):
                last_blob_idx = len(tracks[i].blobs) - 1
                for j in range(len(blobs)):
                    # create a correspondence matrix
                   # print 'minX1: ' + str(track_list[i].minX)
                   # print 'maxX1: ' + str(track_list[i].maxX)
                   # print 'minY1: ' + str(track_list[i].minY)
                   # print 'maxY1: ' + str(track_list[i].maxY)
                         
                   # print 'minX2: ' + str(blobs[j].minX())
                   # print 'maxX2: ' + str(blobs[j].maxX())
                   # print 'minY2: ' + str(blobs[j].minY())
                   # print 'maxY2: ' + str(blobs[j].maxY())
                    
                    matrix[i][j] = get_overlap_area(
                        tracks[i].blobs[last_blob_idx].minX(), tracks[i].blobs[last_blob_idx].minY(),
                        tracks[i].blobs[last_blob_idx].maxX(), tracks[i].blobs[last_blob_idx].maxY(),
                        blobs[j].minX(), blobs[j].minY(), 
                        blobs[j].maxX(), blobs[j].maxY())
            
            print 'matrix:'
            for i in range(len(tracks)):
                for j in range(len(blobs)):
                    print str(matrix[i][j]),
                print '\n'

            removed_blob_list = []
            for i in range(len(tracks)):
                matched_blob_list = []

                for j in range(len(blobs)):
                    if matrix[i][j] >= overlap_th:
                        matched_blob_list.append(j)

                # splitting
                if len(matched_blob_list) > 1:
                    print 'blob splitting' + str(matched_blob_list)

                    # get track's color
                    px = Image((1, 1), ColorSpace.RGB)
                    px[0, 0] = tracks[i].color
                    pxHSV = px.toHSV()
                    hue1 = pxHSV[0, 0][2]
#                    print 'track ' + str(i) + ': ' + str(hue1)

                    min_diff = 10000
                    best_bob_match = -1
                    best_track_match = -1
                    for bid in matched_blob_list:
                        if bid in removed_blob_list:
                            continue

                        px[0, 0] = blobs[bid].meanColor()
                        pxHSV = px.toHSV()
                        hue2 = pxHSV[0, 0][2]
#                        print 'blob ' + str(bid) + ': ' + str(hue2)

                        color_dissimilarity = get_color_dissimilarity(hue1, hue2)

                        if color_dissimilarity == 0:
                            print 'track ' + str(i) + ' matches blob ' + str(bid) + ': ' + str(color_dissimilarity)

                            tracks[i].blobs.append(blobs[bid])
                            removed_blob_list.append(bid)
                        else:
                            tracks[i].blobs.append(blobs[bid])
                            removed_blob_list.append(bid)

#                            if min_diff > color_similarity:
#                                min_diff = color_similarity
#                                best_blob_match = bid
#                                best_track_match = tid

#                    print 'best match for track: ' + str(best_track_match) + ' is ' + str(best_blob_match)

#                    if not tracks[best_track_match].mark_as_match:
#                        tracks[best_track_match].blobs.append(blobs[best_blob_match])
#                        tracks[best_track_match].mark_as_match = True

                elif len(matched_blob_list) == 1:
                    if not tracks[i].mark_as_match:
                        tracks[i].mark_as_match = True
                        
            for j in range(len(blobs)):
                matched_track_idx = []
                for i in range(len(tracks)):
                    if matrix[i][j] >= overlap_th:
                        matched_track_idx.append(i) 

                # merging (only center is updated)
                if len(matched_track_idx) > 1:
                    print 'tracks merging: ' + str(matched_track_idx)
                    for idx in matched_track_idx:
                        tracks[idx].blobs.append(blobs[j])

                elif len(matched_track_idx) == 1:
                    if tracks[matched_track_idx[0]].mark_as_match: 
                        tracks[matched_track_idx[0]].blobs.append(blobs[j])

        for b in blobs:    
            layer = DrawingLayer((img.width, img.height))
            rect_dim = (b.maxX() - b.minX(),
                b.maxY() - b.minY())
            center = b.center()
            layer.centeredRectangle(center, rect_dim, Color.WHITE)
            img.addDrawingLayer(layer)

    for t in tracks:
        last_blob_idx = len(t.blobs) - 1
        print t.blobs[last_blob_idx].center()

    for t in tracks:
        last_blob_idx = len(t.blobs) - 1
        layer = DrawingLayer((img.width, img.height))
        rect_dim = (t.blobs[last_blob_idx].width(), t.blobs[last_blob_idx].height())
        center = t.blobs[last_blob_idx].center()
        layer.centeredRectangle(center, rect_dim, t.color)
        img.addDrawingLayer(layer)
    
    img.applyLayers()
    img.show()

    raw_input()

    img.clearLayers()
    
    time.sleep(1)

