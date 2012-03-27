# Simple Blue Circle Tracker

## Introduction
Simeple Blue Circle Tracker is a simple program to track any blue circle in a video. The main idea is to construct a overlap area association matrix between the bounding box of blobs and tracks. We can then use the association matrix to link blobs in the current frame with the tracks from the previous frame. This code shows a basic idea on tracking multiple objects using an appearance model. You can find my demo [here](http://www.youtube.com/watch?v=icjEyZ605KQ "Simple Blue Circle Tracker Demo").

## Possible Future Work
This code does not handle any occlusion, so it would be great if this feature is implemented. It can also be improved by a better appearance model, Kalman filtering, or particle filtering.

## License
This work is licensed under a Creative Commons Attribution 3.0 License. You are free to use the code here for any purpose, but please give credit to its source. If you make improvements, I will appreciate it if you send me your updates.

