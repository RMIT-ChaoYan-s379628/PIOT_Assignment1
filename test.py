import os

data = ["-u o.p6OF0MXEo2huO3Ajf687fBUczZsTfvHV: https://api.pushbullet.com/v2/pushes -d type=note -d title='Raspberry Pi' -d body=$(hostname - I) "]

for item in data:
    tmpres = os.popen('curl %s' % item).readlines()

print("ok..") 