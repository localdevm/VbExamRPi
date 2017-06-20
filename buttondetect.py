#Importing libraries
import RPi.GPIO as IO
import time

#Setters
IO.setmode(IO.BCM)

IO.setup(4, IO.OUT) #Led setup on gpio 4
IO.setup(17, IO.IN, pull_up_down=IO.PUD_UP) #Led setup on gpio 17

IO.add_event_detect(17, IO.FALLING, bouncetime=200)

def main():
    try:
        while True:
            if IO.event_detected(17):
                IO.output(4, 1)

    except KeyboardInterrupt:
        print('Interrupted')
        pass

    finally:
        IO.cleanup()

#Main seg
if __name__ == "__main__":
    main()
