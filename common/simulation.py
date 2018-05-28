import os
import struct
import time

from pandas.io.parsers import read_csv
from canbus import Prius

ROOT_PATH = os.path.expanduser('~')
DATA_PATH = os.path.join(ROOT_PATH, 'picture/car_logger')
canfile2 = os.path.join(DATA_PATH, 'canbus_output2.csv')
output = os.path.join(DATA_PATH, "combine2file.csv")


class Prius_sim(Prius):
    def __init__(self):
        super(Prius_sim, self).__init__()

    def send_data(self, can_send):
        self.panda.can_send_many(can_send)


def main():
    sim = Prius_sim()

    df = read_csv(canfile2)
    can_data = df.values
    sys_start_time = time.time()
    can_start_time = can_data[0][0]
    can_pre_time = can_data[0][0]
    first_time = True
    for data in can_data:
        can_now_time = data[0]
        addr = int(data[2], 16)
        msg = data[3].split('x')[-1]
        msg = [struct.pack('B', int(msg[i:i + 2], 16)) for i in xrange(0, len(msg), 2)]
        msg = "".join(msg)
        sim.send_data([[addr, 0, msg, 0]])

        # print "can {}".format(can_now_time - can_pre_time)
        # print "sys {}".format((time.time() - sys_pre_time))
        # print can_now_time - can_pre_time - (time.time() - sys_pre_time)
        if first_time:
            time.sleep(can_now_time - can_pre_time)
            first_time = False
        else:
            can_time = can_now_time - can_pre_time
            delay_time = can_time - time.time() + sys_pre_time
            if delay_time > 0:
                time.sleep(delay_time)
            else:
                can_now_time = can_now_time - delay_time + 15.000e-05

        sys_pre_time = time.time()
        can_pre_time = can_now_time

    print "System running time\t{}".format(time.time()-sys_start_time)
    print "CAN messing running time\t{}".format(can_now_time-can_start_time)


if __name__ == '__main__':
    main()