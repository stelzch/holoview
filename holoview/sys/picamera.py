"""A fake PiCamera-class for debugging and testing purposes."""
import time

class PiResolution:
    def __init__(self, width, height):
        self.width = width
        self.height = height

class PiCamera:    
    resolution = PiResolution(1280, 720)

    def __init__(self):
        pass
    def close(self):
        pass
    def add_overlay(self, source, size=None, format=None, **options):
        pass
    def capture(self, output, format="PNG", use_video_port=False, resize=None,
            splitter_port=0, bayer=False, **options):
        pass
    def close(self):
        pass
    def remove_overlay(self, overlay):
        pass
        
    def start_preview(self):
        pass

    def stop_preview(self):
        pass
