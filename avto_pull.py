import os
import time

while True:
    time.sleap(10000)
    try:
        os.systeam('git pull')
    except:
        print("pull error")
    else:
        print("pull successful")

