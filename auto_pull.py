import os
import time

while True:
    time.sleep(10)
    try:
        os.system('git pull')
    except Exception as error:
        print(f"pull error:\n{error}")
    else:
        print("pull successful")

