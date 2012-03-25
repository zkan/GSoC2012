from SimpleCV import *
import time
import numpy
import operator

def get_overlap_area(minx1, miny1, maxx1, maxy1, minx2, miny2, maxx2, maxy2):
    if minx1 > maxx2 or maxx1 < minx2 or miny1 > maxy2 or maxy1 < miny2:
        return 0
    else:
        return (min(maxx2, maxx1) - max(minx2, minx1)) * (min(maxy2, maxy1) - max(miny2, miny1))

class Track:
    def __init__(self):
        self.ID = 0
        self.blobs = []
        self.matched_blob_list = []

cam = Camera(0)

tracks = []
track_id = 0
overlap_th = 160

while True:
    img = cam.getImage()

    blue_stuff = img.colorDistance(Color.BLUE)
    bin_blue_stuff = blue_stuff.binarize(130)
    clean_bin_blue_stuff = bin_blue_stuff.morphOpen().morphClose()

    blobs = clean_bin_blue_stuff.findBlobs()

    if blobs:
        print 'num of blobs: ' + str(len(blobs))
        if not tracks:
            for b in blobs:
                if b.isCircle(0.3) and b.area() > 100:
                    t = Track()
                    track_id = track_id + 1
                    t.ID = track_id
                    t.blobs.append(b)
                    tracks.append(t)
        
        else:
            matrix = numpy.zeros((len(tracks), len(blobs)))
            for i in range(len(tracks)):
                last_blob_idx = len(tracks[i].blobs) - 1
                for j in range(len(blobs)):
                    matrix[i][j] = get_overlap_area(
                        tracks[i].blobs[last_blob_idx].minX(), tracks[i].blobs[last_blob_idx].minY(),
                        tracks[i].blobs[last_blob_idx].maxX(), tracks[i].blobs[last_blob_idx].maxY(),
                        blobs[j].minX(), blobs[j].minY(),
                        blobs[j].maxX(), blobs[j].maxY())

            for i in range(len(tracks)):
                matched_blob_list = []
                for j in range(len(blobs)):
                    if matrix[i][j] >= overlap_th:
                        matched_blob_list.append(j)

                if len(matched_blob_list) == 1:
                    tracks[i].matched_blob_list.append(j)
            
            unmatched_blob_list = []
            for j in range(len(blobs)):
                matched_track_list = []
                num_zero = 0
                for i in range(len(tracks)):
                    if matrix[i][j] >= overlap_th:
                        matched_track_list.append(i)
                    elif matrix[i][j] == 0:
                        num_zero = num_zero + 1

                if len(matched_track_list) == 1:
                    if j in tracks[matched_track_list[0]].matched_blob_list:
                        tracks[matched_track_list[0]].blobs.append(blobs[j])
#                        blobs.pop(j)

                if num_zero == len(tracks):
                    unmatched_blob_list.append(j)

            # create new tracks for unmatched blobs
            for idx in unmatched_blob_list:
                if blobs[idx].isCircle(0.3) and blobs[idx].area() > 100:
                    t = Track()
                    track_id = track_id + 1
                    t.ID = track_id
                    t.blobs.append(blobs[idx])
                    tracks.append(t)

    for t in tracks:
        last_blob_idx = len(t.blobs) - 1
        layer = DrawingLayer((img.width, img.height))
        rect_dim = (t.blobs[last_blob_idx].width(), 
            t.blobs[last_blob_idx].height())
        center = t.blobs[last_blob_idx].center()
        layer.centeredRectangle(center, rect_dim, Color.RED)
        img.addDrawingLayer(layer)
    
    img.applyLayers()
    img.show()

    time.sleep(0.1)

#    print blue_stuff.getNumpy()

#    blue_stuff = img.hueDistance(Color.BLUE).show()

#    blobs = img.findBlobs((0, 0, 100))

#    [circle.drawHull(color = Color.RED, width = 10) for circle in blobs.filter([b.isCircle() for b in blobs])]
'''
    clist = []
    for b in blobs:
        if b.isCircle():
            clist.append(b)

#    blue_stuff = img.colorDistancie(Color.BLUE)
#    blobs = blue_stuff.findBlobs()

#    blue_stuff.show()

'''
'''
    # remove noise then find blobs in the clean image
    blobs = img.morphOpen().morphClose().findBlobs(10)

    img.clearLayers()
    
    time.sleep(1)
'''


