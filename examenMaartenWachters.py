#importing libraries
import RPi.GPIO as io
import time
import json
import paho.mqtt.client as mqtt

#Setting up GPIO pins
io.setmode(io.BCM)
io.setup(17, io.IN, pull_up_down=io.PUD_UP) #Declaring GPIO17
io.setup(18, io.OUT)



pers = 0
start = time.time()
tel = False

def on_message(mqttc, obj, msg):
    global sendstate, pers
    if msg.payload.decode() == 'send':
        sendstate = True

    if sendstate == True:
        mqttc.publish('examen', payload=pers, qos=0, retain=False)
        print('published personen')
        sendstate = False

    print(msg.topic)
    print(msg.payload.decode())

def manual():
    global pers, start, end, tel

    try:
        mqttc = mqtt.Client()
        mqttc.connect("127.0.0.1")
        #io.add_event_detect(17, io.FALLING, callback=manual, bouncetime=200) #Adding event_detected

        if io.input(17):
            #pers += 1
            #print(pers)
            start = time.time()
            tel = True

        if io.input(17) is 0:
            if tel == True:
                print('tis af')
                end = time.time()
                elapsed = end - start
                print(elapsed)


                if elapsed < 5:
                    pers += 1
                    print(pers)
                    tel = False
                elif elapsed > 5:
                    timeStamp = time.strftime("%a, %d %b %Y %H:%M:%S\n")
                    f = open("personLog", "a")
                    f.write(timeStamp)
                    f.write(pers)
                    f.close()
                    sendstate = True
                    tel = False
            elapsed = 0

    except KeyboardInterrupt:
        pass

def main():
    #global variables
    try:
        #while loop
        mqttc = mqtt.Client()
        mqttc.on_message = on_message
        mqttc.manual = manual
        mqttc.connect("127.0.0.1")
        mqttc.subscribe('examen')

        while True:
            manual()
            mqttc.loop()

            for x in range(0, pers):
                io.output(18,1)
                time.sleep(1)
                io.output(18,0)
                time.sleep(1)

    except KeyboardInterrupt:
        print('Shutting down program')
        io.cleanup()

if __name__ == "__main__":
    main()
