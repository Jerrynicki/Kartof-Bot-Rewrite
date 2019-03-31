import urllib.request
import time
import subprocess
import hashlib

last_update = ""

def get_update():
    req = urllib.request.Request("https://raw.githubusercontent.com/Jerrynicki/Kartof-Bot-Rewrite/master/kartof/main.py", headers={"User-Agent": "Mozilla/5.0"})
    recvd = urllib.request.urlopen(req).read()

    return recvd

 
print("Downloading latest version...")

recvd = get_update()

last_update = hashlib.md5(recvd).hexdigest()

with open("main.py", "wb") as file:
    file.write(recvd)

print("Done! Starting...")

proc = subprocess.Popen(["python3", "main.py"])

while True:
    time.sleep(3600)

    print("Checking for new updates...")

    recvd = get_update()

    if hashlib.md5(recvd).hexdigest() != last_update:
        print("Restarting bot with new update applied...")
        proc.terminate() # I know it's bad practice to just kill the process, but I'm honestly to tired to do anything else right now
        
        last_update = hashlib.md5(recvd).hexdigest()

        with open("main.py", "wb") as file:
            file.write(recvd)

        proc = subprocess.Popen(["python3", "main.py"])

    else:
        print("No new updates found.")
