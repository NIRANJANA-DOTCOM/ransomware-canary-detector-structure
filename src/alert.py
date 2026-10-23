
import datetime
def send_alert(msg):
    t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{t}] {msg}"
    print(f"LOGGED: {line}")
    with open("ransomware_alerts.log", "a") as f:
        f.write(line+"\n")
