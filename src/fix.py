import os
# This will auto-fix your empty files
detector_code = '''
import os, hashlib
class RansomwareDetector:
    def __init__(self, canary_dir="canary_files"):
        self.canary_dir = canary_dir
        self.canary_files = []
    def create_canary_files(self, count=5):
        if not os.path.exists(self.canary_dir):
            os.makedirs(self.canary_dir)
        for i in range(count):
            filename = os.path.join(self.canary_dir, f"important_doc_{i}.docx")
            with open(filename, "w") as f:
                f.write("Canary file - DO NOT MODIFY")
            self.canary_files.append({"path": filename, "hash": self.get_file_hash(filename)})
        print(f"[+] Created {count} canary files")
        return self.canary_files
    def get_file_hash(self, filepath):
        try:
            with open(filepath, "rb") as f:
                return hashlib.md5(f.read()).hexdigest()
        except:
            return None
    def check_integrity(self):
        alerts = []
        for canary in self.canary_files:
            path = canary["path"]
            if not os.path.exists(path):
                alerts.append(f"ALERT! Canary DELETED: {path}")
                continue
            cur = self.get_file_hash(path)
            if cur != canary["hash"]:
                alerts.append(f"ALERT! RANSOMWARE DETECTED: {path} modified!")
        return alerts
'''

monitor_code = '''
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
'''

alert_code = '''
import datetime
def send_alert(msg):
    t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{t}] {msg}"
    print(f"LOGGED: {line}")
    with open("ransomware_alerts.log", "a") as f:
        f.write(line+"\\n")
'''

main_code = '''
import os
from .detector import RansomwareDetector
from .monitor import start_monitoring
def main():
    print("==== RANSOMWARE CANARY DETECTOR ====")
    d = RansomwareDetector()
    d.create_canary_files(5)
    path = os.path.abspath("canary_files")
    print(f"Canary files at: {path}")
    print("Try deleting a file there to test detection!")
    start_monitoring(path, d)
if __name__ == "__main__":
    main()
'''

os.makedirs("src", exist_ok=True)
open("src/detector.py","w").write(detector_code)
open("src/monitor.py","w").write(monitor_code)
open("src/alert.py","w").write(alert_code)
open("src/main.py","w").write(main_code)
print("SUCCESS! All 4 files fixed!")