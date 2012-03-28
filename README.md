# Simple Blue Circle Tracker

## Introduction 

Simeple Blue Circle Tracker is a simple program to track any blue
circle in a video. This program has two parts: (1) blue circle
detection and (2) blue circle tracking. This code shows a basic idea
on multiple object tracking using an appearance model. You can find my
demo [here](http://www.youtube.com/watch?v=icjEyZ605KQ "Simple Blue
Circle Tracker Demo").

## Tracking Algorithm

This algorithm aims to link blobs detected in the current frame with
the tracks from the previous frame using a bounding box overlap
rule. The first step is to construct an overlap area association
matrix between the bounding box of blobs and tracks. This matrix gives
us four possible cases: (1) existing object detected, (2) new object
detected, (3) merging object detected, and (4) splitting object
detected. However, the current program does not handle case (3) and
(4). Also, it does not remove any track when it is no longer visible.

For case (1), the matrix will have at most one non-zero element in
each row or column. It means each track associates with each blob, and
each blob associates with each track, respectively. So that we can
easily link blobs with tracks. For case (2), columns with all zero
elements represent newly appeared objects in a video. It means these
blobs do not associate with any existing track. So that we create new
tracks for them.

## Possible Future Work

This code does not handle any occlusion, so it would be great if this
feature is implemented. It can also be improved by a better appearance
model, Kalman filtering, or particle filtering.

## License

This work is licensed under a Creative Commons Attribution 3.0
License. You are free to use the code here for any purpose, but please
give credit to its source. If you make improvements, I will appreciate
it if you send me your updates.

