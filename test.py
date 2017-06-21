import RPi.GPIO as IO
import time
IO.setmode(IO.BCM)

IO.setup(19, IO.OUT)
IO.setup(26, IO.IN, pull_up_down=IO.PUD_UP)

IO.add_event_detect(26, IO.FALLING, bouncetime=200)

def main():
    try:
        while True:
            if IO.event_detected(26):
                print('event triggered')

                 #do nothing

     except KeyboardInterrupt:
         print("Shutting down program and disabling pins")
         GPIO.cleanup()

if __name__ == "__main__":
    main()
