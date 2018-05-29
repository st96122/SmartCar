import os
import sys
import time
import threading

from common.firebase_db import Car2Firebase
from common.realtime import Ratekeeper
from common.canbus import Prius

ROOT_PATH = os.path.expanduser('~')
DATA_PATH = os.path.join(ROOT_PATH, 'picture/car_logger')
# dbc_file = 'dbc/toyota_prius_2017_pt_generated.dbc'
dbc_file = 'dbc/521.dbc'

# Init
prius_can = Prius(dbc_file)
car2firebase = Car2Firebase()
can_recv = False


def upload_data(stop_event):
    while not stop_event.isSet():
        pre_time = time.time()
        # upload all data to firebase
        car2firebase.upload_all(can_recv)
        # print(can_recv)
        # print time.time() - pre_time


def main(rate=100):
    global can_recv
    thread_stop = threading.Event()
    thread = threading.Thread(target=upload_data, args=(thread_stop, ))
    thread.start()

    rk = Ratekeeper(rate, print_delay_threshold=2. / 1000)
    try:
        while 1:
            # prius_can.recv_print('dbc')
            can_recv = prius_can.recv()

            # RUN in 20 Hz
            # if (rk.frame % (rate / 100)) == 0:
            #     print(can_recv)

            rk.keep_time()
    except KeyboardInterrupt:
        thread_stop.set()
        sys.exit()


if __name__ == '__main__':
    main()
