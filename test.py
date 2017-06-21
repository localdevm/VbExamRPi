import RPi.GPIO as IO
import time
IO.setmode(IO.BCM)

IO.setup(19, IO.OUT)
IO.setup(26, IO.IN, pull_up_down=IO.PUD_UP)

IO.add_event_detect(26, IO.FALLING, bouncetime=200)
IO.output(19,0)

led1 = False
def main():
    global led1
    try:
        while True:
            if IO.event_detected(26):
                if led1 == False:
                    print('LED aan')
                    IO.output(19,1)
                    led1 = True

                elif led1 == True:
                    print('LED uit')
                    IO.output(19,0)
                    led1 = False

    except KeyboardInterrupt:
         print("Shutting down program and disabling pins")
         GPIO.cleanup()

if __name__ == "__main__":
    main()
