import sys
import time
import threading

from context import Context


# todo
# This could probably be improved visually for the user.. it's not the most pleasing to look at
# Also, in a very niche case the GUI didn't catch up with the deletion of files, so it ceased updating


class Status(threading.Thread):

    def __init__(self, context: Context):
        self.context = context
        self.workspace = context.workspace
        self.extension_type = context.extension_type
        self.frame_count = context.frame_count
        self.is_alive = True

        threading.Thread.__init__(self)

    def kill(self):
        self.is_alive = False

    def run(self):

        last_10 = [0]

        for x in range(1, self.frame_count - 1):

            if not self.is_alive:
                break

            percent = int((x / self.frame_count) * 100)

            average = 0
            for time_count in last_10:
                average = average + time_count

            average = round(average / len(last_10), 2)

            sys.stdout.write('\r')
            sys.stdout.write("Frame: [%s] %i%%    Average of Last 10 Frames: %s sec / frame" % (x, percent, average))

            if len(last_10) == 10:
                last_10.pop(0)

            now = time.time()

            while x >= self.context.signal_merged_count:
                time.sleep(.00001)

