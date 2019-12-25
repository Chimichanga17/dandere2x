from wrappers.ffmpeg.progressive_frame_extractor_ffmpeg import ProgressiveFramesExtractorFFMPEG
from dandere2xlib.utils.dandere2x_utils import get_operating_system
from context import Context
import yaml

# get config based on OS
configfile = "dandere2x_%s.yaml" % get_operating_system()


with open(configfile, "r") as read_file:
    config = yaml.safe_load(read_file)


context = Context(config)


frame_extractor = ProgressiveFramesExtractorFFMPEG(context, "C:\\Users\\windwoz\\Documents\\GitHub\\dandere2x\\src\\workspace\\yn_moving.mkv")

frame_extractor.start_task()


frame_extractor.extract_frames_to(100)

frame_extractor.kill_task()