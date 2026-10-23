import os, time, hashlib, datetime

def get_hash(p):
    try:
        with open(p,"rb") as f:
            return hashlib.md5(f.read()).hexdigest()
    except:
        return None

def send_alert(m):
    t=datetime.datetime.now().strftime("%H:%M:%S")
    print(f"\n{'='*50}\n🚨 [{t}] {m}\n{'='*50}\n")
    with open("ransomware_alerts.log","a") as f:
        f.write(f"[{t}] {m}\n")

print("==== RANSOMWARE CANARY DETECTOR v1.0 ====")
canary_dir="canary_files"
os.makedirs(canary_dir, exist_ok=True)
canary_files=[]
for i in range(5):
    fp=os.path.join(canary_dir,f"important_doc_{i}.docx")
    with open(fp,"w") as f:
        f.write("Canary file - DO NOT MODIFY - System file")
    canary_files.append({"path":fp,"hash":get_hash(fp)})
    print(f"[+] Created {fp}")

print(f"\n[*] Monitoring {os.path.abspath(canary_dir)}")
print("[*] TEST: Delete or edit a file inside canary_files folder to see detection!\n")

# Simple monitoring without watchdog - works always
try:
    while True:
        for c in canary_files:
            p=c["path"]
            if not os.path.exists(p):
                send_alert(f"RANSOMWARE DETECTED! Canary DELETED: {p}")
                c["hash"]=None
                continue
            cur=get_hash(p)
            if cur!=c["hash"]:
                send_alert(f"RANSOMWARE DETECTED! Canary MODIFIED: {p}")
                c["hash"]=cur
        time.sleep(1)
except KeyboardInterrupt:
    print("Stopped")