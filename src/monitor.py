
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from .alert import send_alert
class RansomwareHandler(FileSystemEventHandler):
    def __init__(self, detector):
        self.detector = detector
    def on_modified(self, event):
        if event.is_directory: return
        print(f"File changed: {event.src_path}")
        alerts = self.detector.check_integrity()
        for a in alerts:
            print(a)
            send_alert(a)
    def on_deleted(self, event):
        print(f"File deleted: {event.src_path}")
        alerts = self.detector.check_integrity()
        for a in alerts:
            print(a)
            send_alert(a)
def start_monitoring(path_to_watch, detector):
    handler = RansomwareHandler(detector)
    obs = Observer()
    obs.schedule(handler, path_to_watch, recursive=True)
    obs.start()
    print(f"Monitoring {path_to_watch}... Press Ctrl+C to stop")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        obs.stop()
    obs.join()
