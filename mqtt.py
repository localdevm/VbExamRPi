#importing libraries
import RPi.GPIO as IO
import time
import json
import paho.mqtt.client as mqtt

#Setters
io.setmode(IO.BCM)

IO.setup(4, IO.OUT) #Led setup on gpio 4
IO.setup(17, IO.IN, pull_up_down=IO.PUD_UP) #Led setup on gpio 17

IO.add_event_detect(17, IO.FALLING, bouncetime=200)

led1 = False

def set_leds(leds, states):
    IO.output(leds, states)

def on_message(mqttc, obj, msg):
    if msg.payload.decode() == 'on':
        IO.output(4, 1)
    elif msg.payload.decode() == 'off':
        IO.output(4, 0)

    print(msg.topic)
    print(msg.payload.decode())

def manual():
    global led1
    try:
        mqttc = mqtt.Client()
        mqttc.connect("127.0.0.1")

        if IO.event_detected(17):
            mqttc.publish('home/alarm', payload='on', qos=0, retain=False)
            led1 = True
            print(led1)
        elif led1 == True:
            mqttc.publish('home/alarm', payload='off', qos=0, retain=False)
            led1 = False
            print(led1)

    except KeyboardInterrupt:
        pass

def main():
    try:
        mqttc = mqttc.Client()
        mqttc.on_message = on_message
        mqttc.manual = manual
        mqttc.connect("127.0.0.1")
        mqttc.subscribe('home/alarm')

        while True:
            manual()
            mqttc.loop()

    except KeyboardInterrupt:
        pass

    finally:
        IO.cleanup()

if __name__ == "__main__":
    main()
