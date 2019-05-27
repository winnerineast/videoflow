# Videoflow

![Videoflow](assets/videoflow_logo.png)

[![Build Status](https://travis-ci.org/videoflow/videoflow.svg?branch=master)](https://travis-ci.org/videoflow/videoflow)
[![license](https://img.shields.io/github/license/mashape/apistatus.svg?maxAge=2592000)](https://github.com/videoflow/videoflow/blob/master/LICENSE)

**Videoflow** is a Python framework for video stream processing. The library is designed to facilitate easy and quick definition of computer vision stream processing applications. It empowers developers to build applications and systems with self-contained Deep Learning and Computer Vision capabilities using simple and few lines of code.  It contains off-the-shelf components for object detection, object tracking, human pose estimation, etc, and it is easy to extend with your own.

The complete documentation to the project is located in [**Read the docs.**](https://videoflow.readthedocs.io)

[1.2]: http://i.imgur.com/wWzX9uB.png
[1]: http://www.twitter.com/videoflow_py
<!--Follow us on [![alt text][1.2]][1]-->

## Installing the framework
### Requirements
Before installing, be sure that you have `cv2` and `tensorflow >= 1.12` already installed.

### Installation
You can install directly using **pip** by doing `pip3 install videoflow`

Alternatively, you can install by:

1. Clone this repository
2. Inside the repository folder, execute `pip3 install . --user`

Python 2 is **NOT SUPPORTED**.  Requires Python 3.6+

## Sample Videoflow application:
Below a sample videoflow application that detects automobiles in an intersection. For more examples see the [examples](examples/) folder.

```python
import videoflow
import videoflow.core.flow as flow
from videoflow.core.constants import BATCH
from videoflow.consumers import VideofileWriter
from videoflow.producers import VideofileReader
from videoflow.processors.vision.detectors import TensorflowObjectDetector
from videoflow.processors.vision.annotators import BoundingBoxAnnotator
from videoflow.utils.downloader import get_file

URL_VIDEO = "https://github.com/videoflow/videoflow/releases/download/examples/intersection.mp4"

class FrameIndexSplitter(videoflow.core.node.ProcessorNode):
    def __init__(self):
        super(FrameIndexSplitter, self).__init__()
    
    def process(self, data):
        index, frame = data
        return frame

input_file = get_file("intersection.mp4", URL_VIDEO)
output_file = "output.avi"
reader = VideofileReader(input_file)
frame = FrameIndexSplitter()(reader)
detector = TensorflowObjectDetector()(frame)
annotator = BoundingBoxAnnotator()(frame, detector)
writer = VideofileWriter(output_file, fps = 30)(annotator)
fl = flow.Flow([reader], [writer], flow_type = BATCH)
fl.run()
fl.join()
```

The output of the application is an annotated video:


## The Structure of a flow application

A flow application usually consists of three parts:

1. In the first part of the application you define a directed acyclic graph of computation nodes. There are 3 different kinds of nodes: producers, processors and consumers.  Producer nodes create data (commonly they will get the data from a source that is external to the flow).  Processors receive data as input and produce data as output. Consumers read data and do not produce any output.  You usually use a consumer when you want to write results to a log file, or when you want to push results to an external source (rest API, S3 bucket, etc.)

2. To create a flow object, you need to pass to it your list of producers and your list of consumers. Once a flow is defined you can start it.  Starting the flow means that the producers start putting data into the flow and processors and consumers start receiving data.  Starting the flow also means allocating resources for producers, processors and consumers.  For simplicity for now we can say that each producer, processor and consumer will run on its own process space.

3. Once the flow starts, you can also stop it.  When you stop the flow, it will happen organically.  Producers will stop producing data.  The rest of the nodes in the flow will continue running until the pipes run dry.  The resources used in the flow are deallocated progressively, as each node stops producing/processing/consuming data.
