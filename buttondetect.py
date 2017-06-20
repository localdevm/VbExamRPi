#Importing libraries
import RPi.GPIO as io
import time

#pinmode to BCM
io.setmode(io.BCM)

io.setup(4, io.out)
io.setup(17, io.IN, pull_up_down=io.PUD_UP)

io.add_event_detect(17, io.FALLING, bouncetime=200)

def main():
    try:
        if io.event_detected(17):
            io.output(4,1)

    except KeyboardInterrupt:
        print('Interrupted')
        pass

    finally:
        io.cleanup()

if __name__ == "__main__":
    main()
