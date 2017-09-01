#!/usr/bin/python

import sys
import time
import getopt
import picamera


class TimeLapse:
    file_lst = []
    duration_minutes = 0
    delay_seconds = 0
    duration_seconds = 0
    prefix = '../output/'

    def __init__(self, delay_minutes=0, delay_seconds=0, duration_minutes=0, prefix=''):
        self.delay_minutes = int(delay_minutes)
        self.delay_second = int(delay_seconds)
        duration_minutes = int(duration_minutes)

        if delay_seconds < 0 and delay_minutes < 0:
            raise ValueError("DELAY must be strictly positive !")

        if duration_minutes <= 0:
            raise ValueError("DURATION must be strictly positive !")
        if duration_minutes < delay_minutes:
            raise ValueError("DURATION must be greater than DELAY !")

        self.prefix += prefix
        self.delay_seconds = delay_minutes * 60 + self.delay_seconds
        self.duration_seconds = duration_minutes * 60

        pass

    def capture(self):
        with picamera.PiCamera() as camera:
            camera.start_preview()
            try:
                for i, file_name in enumerate(camera.capture_continuous(self.prefix + '_{timestamp:%H-%M-%S}.jpg')):
                    print("Capturing %s ..." % file_name)
                    print(str(i))
                    self.file_lst.append(file_name)
                    if i == self.duration_minutes - 1:
                        break
                    time.sleep(self.delay_seconds)
            finally:
                camera.stop_preview()


def help():
    print 'help'


def main():
    delay_minutes = 0
    delay_seconds = 0
    duration_minutes = 0
    prefix = ''
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h m:v s:v t:v p:v", ["help", "output="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print str(err)  # will print something like "option -a not recognized"
        sys.exit(2)
    for o, a in opts:
        if o == "-h":
            help()
            sys.exit(0)
        elif o in ("-m", "--minutes"):
            delay_minutes = a
        elif o in ("-s", "--seconds"):
            delay_seconds = a
        elif o in ("-t", "--time"):
            duration_minutes = a
        elif o in ("-p", "--prefix"):
            prefix = a
        else:
            assert False, "unhandled option"
    time_lapse = TimeLapse(
        delay_minutes=delay_minutes,
        delay_seconds=delay_seconds,
        duration_minutes=duration_minutes,
        prefix=prefix
    )
    time_lapse.capture()


if __name__ == '__main__':
    main()
