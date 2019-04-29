from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import cv2

from ..core.node import ProducerNode, ContextNode

class VideofileReader(ProducerNode, ContextNode):
    '''
    Opens a video capture object and returns subsequent frames
    from the video each time ``next`` is called
    '''
    def __init__(self, video_file : str):
        '''
        - Arguments:
            - video_file: path to video file
        '''
        self._video_file = video_file
        self._video = None
        super(VideofileReader, self).__init__()
    
    def __enter__(self):
        '''
        Opens the video stream
        '''
        if self._video is None:
            self._video = cv2.VideoCapture(self._video_file)

    def __exit__(self, exc_type, exc_value, exc_traceback):
        '''
        Releases the video stream object
        '''
        self._video.release()
        if exc_type is not None:
            return False
        return True

    def next(self):
        '''
        - Returns:
            - frame: np.array of shape (h, w, 3)
        
        - Raises:
            - StopIteration: after it finishes reading the videofile.
        '''
        
        if self._video.isOpened():
            success, frame = self._video.read()
            if not success:
                self._video.release()
                raise StopIteration()
            else:
                return frame
        else:
            raise StopIteration()
