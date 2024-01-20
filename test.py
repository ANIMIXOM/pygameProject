import time

sec = 0
while True:
    time.sleep(1)
    sec += 1
    if sec == 10:
        break
print(sec)
