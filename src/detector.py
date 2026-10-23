
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
