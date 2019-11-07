import picamera
import time
import numpy
from PIL import Image, ImageDraw, ImageFont

#############
# Constants
#############
TOTAL_DISTANCE = 5  # miles


RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 225)
YELLOW = (225, 225, 0)
CYAN = (0, 225, 225)
PURPLE = (225, 0, 225)
WHITE = (225, 225, 225)

class Osd:
    # Video Settings
    VIDEO_HEIGHT = 720
    VIDEO_WIDTH = 1280
    FRAMERATE = 60
    BRIGHTNESS = 70

    def __init__(self):
        # Camera settings
        camera = picamera.PiCamera()
        camera.resolution = (self.VIDEO_WIDTH, self.VIDEO_HEIGHT)
        camera.framerate = self.FRAMERATE
        camera.brightness = self.BRIGHTNESS
        self.camera = camera
        self.camera.start_preview()

        self.canvas = Image.new("RGB", (self.VIDEO_WIDTH, self.VIDEO_HEIGHT))
        self.img = self.canvas.copy()
        self.overlay = camera.add_overlay(self.img.tobytes(), layer=3,
                                          alpha=100)

    def _renderText(self, text, position, color=WHITE, size=40):
        font = ImageFont.truetype("../res/consola.ttf", size)
        draw = ImageDraw.Draw(self.img)
        draw.text(position, text, color, font)

    def RenderTime(self):
        timeText = "Time: {0}".format(time.strftime('%H:%M:%S'))
        self._renderText(timeText, (10, 10))

    def RenderBatteryPercentage(self, batteryPercentage):
        batteryText = "Battery: {:0.0f}%".format(round(batteryPercentage,-1))
        batteryTextColour = GREEN
        if batteryPercentage < 50:
            batteryTextColour = RED
        self._renderText(batteryText,
                         (900, 10),
                         batteryTextColour,
                         30)

    def RenderSpeed(self, speedKph, speedMph):
        speedText = "       Speed:"
        self._renderText(speedText,
                         (10, 560),
                         WHITE,
                         30)

        speedText = " {:4.1f} KPH/{:4.1f} MPH".format(speedKph, speedMph)
        self._renderText(speedText,
                         (210, 550),
                         CYAN,
                         50)

    def RenderTargetSpeed(self, speedKph, speedMph):
        speedText = "Target Speed:"
        self._renderText(speedText,
                         (10, 610),
                         WHITE,
                         30)

        speedText = " {:4.1f} KPH/{:4.1f} MPH".format(speedKph, speedMph)
        self._renderText(speedText,
                         (210, 600),
                         CYAN,
                         50)

    def RenderCadence(self, cadence):
        cadenceText = "Cadence:"
        self._renderText(cadenceText,
                         (900, 610),
                         WHITE,
                         30)

        cadenceText = " {0} RPM".format(cadence)
        self._renderText(cadenceText,
                         (1020, 600),
                         CYAN)

    def RenderDistance(self, distance):
        tickPosition = int((distance / TOTAL_DISTANCE) * 1170) + 50

        # Make the tick blink
        if ((time.time() % 1) < 0.5):
            self._renderText(">",
                             (tickPosition, 660),
                             WHITE,
                             30)

        distanceText = "{:0.2f} M".format(distance)
        distanceTextPosition = tickPosition - 40
        if (distanceTextPosition < 50):
            distanceTextPosition = 50
        elif (distanceTextPosition > 1130):
            distanceTextPosition = 1130
        self._renderText(distanceText,
                         (distanceTextPosition, 690),
                         GREEN,
                         30)

        self._renderText("|",
                         (50, 660),
                         WHITE,
                         30)
        self._renderText("0 M",
                         (10, 690),
                         WHITE,
                         30)

        self._renderText("|",
                         (1220, 660),
                         WHITE,
                         30)
        self._renderText("5 M",
                         (1220, 690),
                         WHITE,
                         30)

    def Display(self,
            speedKph,
            speedMph,
            targetSpeedKph,
            targetSpeedMph,
            cadence,
            distance,
            batteryPercentage):
        self.img = self.canvas.copy()

        # Render everything
        self.RenderTime()
        self.RenderSpeed(speedKph, speedMph)
        self.RenderTargetSpeed(targetSpeedKph, targetSpeedMph)
        self.RenderCadence(cadence)
        self.RenderDistance(distance)
        self.RenderBatteryPercentage(batteryPercentage)

        self.overlay.update(self.img.tobytes())
