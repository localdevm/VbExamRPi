#importing libraries
import RPi.GPIO as io
import time
import json
import paho.mqtt.client as mqtt

#Setting up GPIO pins
io.setmode(io.BCM)
io.setup(17, io.IN, pull_up_down=io.PUD_UP) #Declaring GPIO17
io.setup(18, io.OUT)

io.add_event_detect(17, io.FALLING, bouncetime=200) #Adding event_detected

pers = 0
def on_message(mqttc, obj, msg):
    global sendstate
    if msg.payload.decode() == 'send':
        sendstate = True

    if sendstate == True:
        mqttc.publish('examen', payload=pers, qos=0, retain=False)
        print('published personen')
        sendstate = False

    print(msg.topic)
    print(msg.payload.decode())

def manual():
    try:
        mqttc = mqtt.Client()
        mqttc.connect("127.0.0.1")

        if io.event_detected(17):
            pers = pers + 1
            print(pers)
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
        print('Shutting program')
        io.cleanup()

if __name__ == "__main__":
    main()
