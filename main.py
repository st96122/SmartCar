import os
import csv
from common.update import Car2Firebase
from common.realtime import Ratekeeper
from common.canbus import Prius


ROOT_PATH = os.path.expanduser('~')
DATA_PATH = os.path.join(ROOT_PATH, 'picture/car_logger')


def main(rate=100):
    prius_can = Prius()
    car2firebase = Car2Firebase()
    rk = Ratekeeper(rate, print_delay_threshold=2. / 1000)

    while 1:
        prius_can.recv()
        rk.keep_time()

if __name__ == '__main__':
    main()
