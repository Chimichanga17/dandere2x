import os
import time

from context import Context
from wrappers.frame.frame import Frame
import threading
from dandere2xlib.utils.dandere2x_utils import file_exists


class Compress_Frames(threading.Thread):

    def __init__(self, context: Context):
        threading.Thread.__init__(self)
        self.is_alive = True
        self.inputs_dir = context.input_frames_dir
        self.frame_count = context.frame_count
        self.quality_moving_ratio = context.quality_moving_ratio
        self.compressed_static_dir = context.compressed_static_dir
        self.compressed_moving_dir = context.compressed_moving_dir
        self.quality_minimum = context.quality_minimum
        self.extension_type = context.extension_type
        self._is_stopped = False

    def kill(self):
        self.is_alive = False

    def is_alive(self):
        return self.is_alive

    def run(self):
        # start from 1 because ffmpeg's extracted frames starts from 1
        for x in range(1, self.frame_count + 1):

            while not file_exists(self.inputs_dir + "frame" + str(x) + self.extension_type) and self.is_alive:
                time.sleep(.05)

            if not self.is_alive:
                return

            # if the compressed frame already exists, don't compress it
            if os.path.exists(self.compressed_static_dir + "compressed_" + str(x) + ".jpg"):
                continue

            frame = Frame()

            frame.load_from_string_wait(self.inputs_dir + "frame" + str(x) + self.extension_type)
            frame.save_image_quality(self.compressed_static_dir + "compressed_" + str(x) + ".jpg",
                                     self.quality_minimum)
            frame.save_image_quality(self.compressed_moving_dir + "compressed_" + str(x) + ".jpg",
                                     int(self.quality_minimum * self.quality_moving_ratio))

