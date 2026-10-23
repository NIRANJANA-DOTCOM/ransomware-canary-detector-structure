
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
