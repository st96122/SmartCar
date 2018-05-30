import os
import sys
import time
import threading
import cv2
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
i=1

def upload_data(stop_event):

    while not stop_event.isSet():
        pre_time = time.time()

        # upload all data to firebase
        car2firebase.upload_all(can_recv)

        print(can_recv)

        #print time.time() - pre_time
def video(stop_event):
    i=1
    while not stop_event.isSet():

        k = str(i).zfill(10)


        img = cv2.imread(DATA_PATH + '/' + k + '.png')
        cv2.imshow('img', img)
        i += 1
        if cv2.waitKey(115) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            return
        if i>1052:
            cv2.destroyAllWindows()
            return
def main(rate=100):
    global can_recv
    global cap
    global thread2
    cap = cv2.VideoCapture(DATA_PATH + '/0524.avi')

    thread_stop = threading.Event()
    thread = threading.Thread(target=upload_data, args=(thread_stop, ))
    thread.start()

    thread2 = threading.Thread(target=video, args=(thread_stop,))
    thread2.start()

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
