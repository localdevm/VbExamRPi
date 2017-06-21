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
    global pers, start, end

    try:
        mqttc = mqtt.Client()
        mqttc.connect("127.0.0.1")
        io.add_event_detect(17, io.FALLING, callback=manual, bouncetime=200) #Adding event_detected

        if io.input(17):
            #pers += 1
            #print(pers)
            start = time.time()

        if io.input(17) is 0:
            print('tis af')
            end = time.time()
            elapsed = end - start
            print(elapsed)

            if elapsed < 5:
                pers += 1
                print(pers)
            elif elapsed > 5:
                #log
                sendstate = True

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

    except KeyboardInterrupt:
        print('Shutting down program')
        io.cleanup()

if __name__ == "__main__":
    main()
