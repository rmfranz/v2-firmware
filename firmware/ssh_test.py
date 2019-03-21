import os
print("starting")
os.system("sudo systemctl stop ssh")
os.system("sudo systemctl disable ssh")