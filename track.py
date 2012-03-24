from SimpleCV import *
import glob
import time
import numpy

class Track:
    ID = 0
    color = (0, 0, 0)
    blob_list = []
    match = False

def get_overlap_area(minx1, miny1, maxx1, maxy1, minx2, miny2, maxx2, maxy2):
    if minx1 > maxx2 or maxx1 < minx2 or miny1 > maxy2 or maxy1 < miny2:
        return 0
    else:
        return (min(maxx2, maxx1) - max(minx2, minx1)) * (min(maxy2, maxy1) - max(miny2, miny2))

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
        for b in blobs:
            if not track_list:
                t = Track()
                track_id = track_id + 1
                t.ID = track_id
                # throw out the remainder
                # meanColor() returns BGR space, so need to reverse to RGB
                t.color = tuple([int(b.meanColor()) 
                    if isinstance(b.meanColor(), float) else int(x) 
                    for x in reversed(b.meanColor())])
                t.blob_list.append(b)
                track_list.append(t)
            else:
                matrix = numpy.zeros((len(track_list), len(blobs)))
                for i in range(len(track_list)):
                    for j in range(len(blobs)):
                        last_blob_idx = len(track_list[i].blob_list) - 1
                        matrix[i][j] = get_overlap_area(
                            track_list[i].blob_list[last_blob_idx].minX(),
                            track_list[i].blob_list[last_blob_idx].minX(),
                            track_list[i].blob_list[last_blob_idx].minX(),
                            track_list[i].blob_list[last_blob_idx].minX(),
                            blobs[j].minX(), blobs[j].minY(), 
                            blobs[j].maxX(), blobs[j].maxY())
                        print matrix[i][j]









                    
#                        last_blob_idx = len(track_list[i].blob_list) - 1
#                        if not track_list[i].match:
#                            print 'track #' + str(i)
#                            px = Image((1, 1), ColorSpace.RGB)
#                            px[0, 0] = track_list[i].blob_list[last_blob_idx].meanColor()
#                            pxHSV = px.toHSV()
#                            hue1 = pxHSV[0, 0][2]
#                            print 'hue1: ' + str(hue1)
#
#                            px[0, 0] = blobs[j].meanColor()
#                            pxHSV = px.toHSV()
#                            hue2 = pxHSV[0, 0][2]
#                            print 'hue2: ' + str(hue2)
#
#                            color_similarity = get_color_similarity(hue1, hue2)
#                            if color_similarity < 5:
#                                print 'match found'
#                                track_list[i].blob_list.append(blobs[j])
#                                track_list[i].match = True
#                                blobs.pop(j)

#        for b in blobs:
#            print 'create a new track'
#            t = Track()
#            track_id = track_id + 1
#            t.ID = track_id
#            # throw out the remainder
#            t.color = tuple([int(b.meanColor()) 
#                if isinstance(b.meanColor(), float) else int(x) 
#                for x in b.meanColor()])
#            t.blob_list.append(b)

        for i in range(len(track_list)):
            track_list[i].match = False

    for i in range(len(track_list)):
        last_blob_idx = len(track_list[i].blob_list) - 1
        
#        print track_list[i].blob_list[last_blob_idx].width()

        layer = DrawingLayer((img.width, img.height))
        rect_dim = (track_list[i].blob_list[last_blob_idx].width(),
            track_list[i].blob_list[last_blob_idx].height())
        centroid = track_list[i].blob_list[last_blob_idx].center()
        layer.centeredRectangle(centroid, rect_dim, track_list[i].color)
        img.addDrawingLayer(layer)
    
    img.applyLayers()

    img.show()
    
    time.sleep(1)


#            px = Image((1, 1), ColorSpace.RGB)
#            px[0, 0] = b.meanColor()
#            pxHSV = px.toHSV()
#            hue = pxHSV[0, 0][2]
#            print hue
#            print dist(b.meanColor(), Color.RED)

'''
                matrix = numpy.zeros((len(track_list), len(blobs)))
                for i in range(len(track_list)):
                    for j in range(len(blobs)):
                        last_blob_idx = len(track_list[i].blob_list) - 1
                        matrix[i][j] = get_overlap_area(
                            track_list[i].blob_list[last_blob_idx].minX(), 
                            track_list[i].blob_list[last_blob_idx].minY(), 
                            track_list[i].blob_list[last_blob_idx].maxX(), 
                            track_list[i].blob_list[last_blob_idx].maxY(), 
                            blobs[j].minX(), blobs[j].minY(), 
                            blobs[j].maxX(), blobs[j].maxY())

                num_zero_in_rows = 0
                num_zero_in_cols = 0
                num_non_zero_in_rows = 0
                num_non_zero_in_cols = 0

                for i in range(len(track_list)):
                    for j in range(len(blobs)):
                        if matrix[i][j] > 0:
                            num_non_zero_in_rows = num_non_zero_in_rows + 1
                        else:
                            num_zero_in_rows = num_zero_in_rows + 1

                # if there are more than one blob corresponding with the same track
                if num_non_zero_in_rows > 1:
                    
                    

#            px = Image((1, 1), ColorSpace.RGB)
#            px[0, 0] = b.meanColor()
#            pxHSV = px.toHSV()
#            hue = pxHSV[0, 0][2]
#            print hue
#            print dist(b.meanColor(), Color.RED)
        

#    time.sleep(1)
'''

