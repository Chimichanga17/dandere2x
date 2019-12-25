#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Licensed under the GNU General Public License Version 3 (GNU GPL v3),
    available at: https://www.gnu.org/licenses/gpl-3.0.txt

(C) 2018-2019 aka_katto

Dandere2X is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Dandere2X is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

Description: Dandere2X is an automation software based on waifu2x image
enlarging engine. It extracts frames from a video, enlarge it by a
number of times without losing any details or quality, keeping lines
smooth and edges sharp.
"""

import logging
import os
import sys
import threading
import time

from dandere2xlib.core.merge import merge_loop
from dandere2xlib.core.residual import residual_loop
from dandere2xlib.frame_compressor import compress_frames
from dandere2xlib.mindiskusage import MinDiskUsage
from dandere2xlib.status import print_status
from dandere2xlib.utils.dandere2x_utils import delete_directories, create_directories
from dandere2xlib.utils.dandere2x_utils import valid_input_resolution, file_exists
from wrappers.dandere2x_cpp import Dandere2xCppWrapper
from wrappers.ffmpeg.ffmpeg import extract_frames, append_video_resize_filter
from wrappers.waifu2x.waifu2x_caffe import Waifu2xCaffe
from wrappers.waifu2x.waifu2x_converter_cpp import Waifu2xConverterCpp
from wrappers.waifu2x.waifu2x_vulkan import Waifu2xVulkan
from wrappers.waifu2x.waifu2x_vulkan_legacy import Waifu2xVulkanLegacy


class Dandere2x:
    """
    The main driver that can be called in a various level of circumstances - for example, dandere2x can be started
    from dandere2x_gui_wrapper.py, raw_config_driver.py, or raw_config_gui_driver.py. In each scenario, this is the
    class that is called when Dandere2x ultimately needs to start.
    """

    def __init__(self, context):
        self.context = context
        self.jobs = {}
        self.min_disk_demon = None
        self.waifu2x = self._get_waifu2x_class(self.context.waifu2x_type)

    def __extract_frames(self):

        if self.context.use_min_disk:
            self.min_disk_demon.progressive_frame_extractor.extract_frames_to(100)
            self.min_disk_demon.extract_initial_frames()
        elif not self.context.use_min_disk:
            extract_frames(self.context, self.context.input_file)

    def __setup_jobs(self):
        self.jobs['compress_frames_thread'] = threading.Thread(target=compress_frames, args=([self.context]),
                                                               daemon=True)
        self.jobs['dandere2xcpp_thread'] = Dandere2xCppWrapper(self.context)
        self.jobs['merge_thread'] = threading.Thread(target=merge_loop, args=([self.context]),
                                                     daemon=True)
        self.jobs['residual_thread'] = threading.Thread(target=residual_loop, args=([self.context]),
                                                        daemon=True)

        self.jobs['waifu2x_thread'] = self.waifu2x
        self.jobs['status_thread'] = threading.Thread(target=print_status, args=([self.context]),
                                                      daemon=True)

        if self.context.use_min_disk:
            self.min_disk_demon = MinDiskUsage(self.context)
            self.jobs['min_disk_thread'] = threading.Thread(target=self.min_disk_demon.run,
                                                            daemon=True)

    def __upscale_first_frame(self):

        one_frame_time = time.time()
        self.waifu2x.upscale_file(input_file=self.context.input_frames_dir + "frame100" + self.context.extension_type,
                                  output_file=self.context.merged_dir + "merged_100" + self.context.extension_type)

        if not file_exists(self.context.merged_dir + "merged_100" + self.context.extension_type):
            """ 
            Ensure the first file was able to get upscaled. We literally cannot continue if it doesn't.
            """

            print("Could not upscale first file.. check logs file to see what's wrong")
            logging.info("Could not upscale first file.. check logs file to see what's wrong")
            logging.info("Exiting Dandere2x...")
            sys.exit(1)

        print("\n Time to upscale an uncompressed frame: " + str(round(time.time() - one_frame_time, 2)))

    def run_concurrent(self):
        """
        Starts the dandere2x_python process at large.
        """

        # directories need to be created before we do anything
        create_directories(self.context.directories)

        # dandere2x needs the width and height to be a share a common factor with the block size,
        # so append a video filter if needed to make the size conform
        if not valid_input_resolution(self.context.width, self.context.height, self.context.block_size):
            append_video_resize_filter(self.context)

        # create the list of threads to use for dandere2x
        self.__setup_jobs()

        # extract the initial frames needed for execution depending on type (min_disk_usage / non min_disk_usage )
        self.__extract_frames()

        # first frame needs to be upscaled manually before dandere2x process starts.
        self.__upscale_first_frame()

        # run and wait for all the dandere2x threads.
<<<<<<< Updated upstream
        for job in self.jobs:
            self.jobs[job].start()
            logging.info("Starting new %s process" % job)
=======
        # for job in self.jobs:
        #     self.jobs[job].start()
        #     logging.info("Starting new %s process" % job)

        print("threading before thread calls")
        print(threading.enumerate())

        self.compress_frames_thread.start()
        self.dandere2x_cpp_thread.start()
        self.merge_thread.start()
        self.residual_thread.start()
        self.waifu2x.start()
        self.status_thread.start()
        self.min_disk_demon.start()

        #time.sleep(10)


        # print("killing da jobs")
        # for job in self.jobs:
        #     print("killing " + str(job))
        #     self.jobs[job].kill()
        #
        #     logging.info("%s process thread joined" % job)


        # there's an issue where even if we call kill, there's wait_on_files inside of the
        # threads which are holding up a proper dandere2x closure.


        print("killing all da jobs")
        #self.residual_thread.join()
        #self.min_disk_demon.kill()
        self.min_disk_demon.join()


        # print('waiting on res')
        #self.residual_thread.kill()
        self.residual_thread.join()
        #
        # print('waiting on merge')
        #self.merge_thread.kill()
        self.merge_thread.join()
        #
        # print('waiting on waifu2x')
        #self.waifu2x.kill()
        self.waifu2x.join()
        #
        # print('waiting on cpp')
        #self.dandere2x_cpp_thread.kill()
        self.dandere2x_cpp_thread.join()
        #
        # print('waiting on status')
        #self.status_thread.kill()
        self.status_thread.join()
        #
        # print('waiting on compress')
        #self.compress_frames_thread.kill()
        self.compress_frames_thread.join()

        # for job in self.jobs:
        #     self.jobs[job].join()
        #
        #     logging.info("%s process thread joined" % job)
>>>>>>> Stashed changes

        for job in self.jobs:
            self.jobs[job].join()

            logging.info("%s process thread joined" % job)

        self.context.logger.info("All threaded processes have finished")

    def _get_waifu2x_class(self, name: str):

        if name == "caffe":
            return Waifu2xCaffe(self.context)

        elif name == "converter_cpp":
            return Waifu2xConverterCpp(self.context)

        elif name == "vulkan":
            return Waifu2xVulkan(self.context)

        elif name == "vulkan_legacy":
            return Waifu2xVulkanLegacy(self.context)

        else:
            logging.info("no valid waifu2x selected")
            print("no valid waifu2x selected")
            exit(1)

    def delete_workspace_files(self):
        """
        Delete the files produced by dandere2x (beside logs) if this method is called.
        """
        delete_directories(self.context.directories)
        no_sound = os.path.join(self.context.workspace, "nosound.mkv")

        try:
            os.remove(no_sound)

        except OSError:
            print("Deletion of the file %s failed" % no_sound)
            print(OSError.strerror)
        else:
            print("Successfully deleted the file %s " % no_sound)
