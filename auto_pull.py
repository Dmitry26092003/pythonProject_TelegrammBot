import os
import time
import config

while True:
    time.sleep(config.ap_sleep)
    try:
        os.system('git pull')
    except Exception as error:
        print(f"pull error:\n{error}")
    else:
        print("pull successful")

