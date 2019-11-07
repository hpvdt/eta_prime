import PIL.Image as Image
import subprocess
import os
from sys import platform

class PiCamera:
    def __init__(self):
        self.winID = None
        self.first = True

    def start_preview(self):
        pass

    def add_overlay(self, image_bytes, layer=3, alpha=100):
        self._display_image(image_bytes)
        return self

    def update(self, image_bytes):
        self._display_image(image_bytes)

    def _display_image(self, image_bytes):
        ''' This function displays an image in a preview window. This shadows
        the original behavior of displaying to the screen framebuffer.'''
        # This "if linux" block is to make the updated OSD image show in the same
        # window at each interval. There is no way this would work on Windows.
        if platform == "linux" or platform == "linux2":
            if self.first:
                self.first = False
            else:
                if self.winID is None:
                    output = subprocess.check_output("xwininfo")
                    self.winID = output.split('\n')[5].split(' ')[3]
                    function = os.system
                    # Monkey patch os.system so that it will include the window
                    # argument when PIL will call it. Assumes os.system is used
                    # nowhere else in the software, which isn't completely true.
                    def new_system(string):
                        command_split = string.split(" ")
                        new_command = " ".join([command_split[0]] + ['-window ' + self.winID] + command_split[1:])
                        function(new_command)
                    os.system = new_system

        Image.frombytes('RGB', self.resolution, image_bytes).show()
