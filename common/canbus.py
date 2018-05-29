from __future__ import print_function
import struct
import numpy as np
from collections import OrderedDict
from panda import Panda
from cantools.db import load_file as load_dbc_file


fingerprint = OrderedDict(((37, ['wheel_angle']),
                           (180, ['SPEED']),
                           (288, ['gear_1', 'gear_2']),
                           (560, ['brake_LI', 'brake_H', 'handcrat']),
                           (1407, ['LIGHT_SMALL', 'LIGHT_BIG', 'LIGHT_FLASH']),
                           (1462, ['door_lock'])))


def binary_show(bytes):
    fmt = '!'
    for i in range(len(bytes)):
        fmt += 'B'
    output_int = struct.unpack(fmt, bytes)
    return ' '.join('{:02X}'.format(b) for b in output_int)


def add_checksum(addr, msg):
    IDH = (addr & 0xff00) >> 8
    IDL = addr & 0xff
    checksum = IDH + IDL + len(msg) + 1
    for byte in msg:
        checksum += ord(byte)
    return struct.pack('B', checksum & 0xff)


def create_speedometer_B4(frame, speed, bus=0, cks=False):
    counter = frame & 0xff  # fix
    counter = 0x00
    msg = struct.pack('!BBBBBH', 0x00, 0x00, 0x00, 0x00, counter, speed)
    if cks:
        check = add_checksum(0xB4, msg)
        msg = msg + check
    return [0xB4, 0, msg, bus]


def create_speedometer_B1(speed, bus=0, cks=False):
    msg = struct.pack('!HBBB', speed, 0x00, 0x00, 0x39)
    if cks:
        check = add_checksum(0xB1, msg)
        msg = msg + check
    return [0xB1, 0, msg, bus]


def create_speedometer_B3(speed, bus=0, cks=False):
    msg = struct.pack('!HBBB', speed, 0x00, 0x00, 0x39)
    if cks:
        check = add_checksum(0xB3, msg)
        msg = msg + check
    return [0xB3, 0, msg, bus]


def create_speedometer_3CA(speed, bus=0, cks=False):
    speed = np.ceil(speed / 255)
    msg = struct.pack('!BBBBB', 0x00, 0x21, speed, 0x00, 0xfc)
    if cks:
        check = add_checksum(0x3CA, msg)
        msg = msg + check
    return [0x3CA, 0, msg, bus]


class Prius(object):
    def __init__(self, dbc=False):
        panda_list = Panda.list()
        # choose panda serial prot
        if len(panda_list) > 1:
            for i, s in enumerate(panda_list, 1):
                print('{}) {}'.format(i, s))
            serial = panda_list[input('Please input 1, 2,.... or 10 number: ') - 1]
        else:
            serial = panda_list[0]
        # Connect to panda
        if serial in panda_list:
            self.panda = Panda(serial)
            self.panda.set_safety_mode(Panda.SAFETY_ALLOUTPUT)
            self.panda.can_clear(0)
            self.frame = 0
            print('Connect Panda [Send]')
        else:
            print('Not Panda connect')
            exit()
        # add dbc decoder
        if dbc:
            self.can_msg_parser = load_dbc_file(dbc)
            print(self.can_msg_parser.messages)
        self.upload_data = OrderedDict((('wheel_angle', 0), ('SPEED', 0), ('gear_1', 35), ('gear_2', 96),
                                        ('brake_LI', 0), ('brake_H', 0), ('handcrat', 0),
                                        ('LIGHT_SMALL', 0), ('LIGHT_BIG', 0), ('LIGHT_FLASH', 0),
                                        ('door_lock', 128)))

    def send_speed(self, speed=0):
        can_send = [create_speedometer_B4(self.frame, speed, 0, True), create_speedometer_B1(speed, 0, True),
                    create_speedometer_B3(speed, 0, True), create_speedometer_3CA(speed, 0)]
        # speedometer
        self.frame += 1
        self.panda.can_send_many(can_send)

    def send_door_lock(self, lock=True):
        can_send = []
        if lock:
            msg = struct.pack('!BBB', 0xe4, 0x81, 0x00)
            can_send.append([0x5B6, 0, msg, 0])
            self.panda.can_send_many(can_send)
        else:
            msg = struct.pack('!BBB', 0xe4, 0x00, 0x00)
            can_send.append([0x5B6, 0, msg, 0])
            self.panda.can_send_many(can_send)

    def recv_print(self, mode='all'):
        can_msgs = self.panda.can_recv()
        if mode == 'dbc':
            for msg in can_msgs:
                if msg[0] in fingerprint.keys():
                    try:
                        print(msg[0])
                        print(self.can_msg_parser.decode_message(msg[0], msg[2]))
                    except:
                        pass
        else:
            can_msgs_bytes = []
            for address, _, dat, src in can_msgs:
                can_msgs_bytes.append((address, 0, bytes(dat), src))
                if mode == 'all':
                    print("Address: {}\t Data: {}\t src: {}".format(address, binary_show(dat), src))
                elif address == 0xb4:
                    print("Address: {}\t Data: {}\t src: {}".format(address, binary_show(dat), src))

    def recv(self):
        can_msgs = self.panda.can_recv()
        for msg in can_msgs:
            try:
                if msg[0] in fingerprint.keys():
                    data_dict = self.can_msg_parser.decode_message(msg[0], msg[2])
                    for i in fingerprint[msg[0]]:
                        self.upload_data[i] = data_dict[i]
            except:
                pass
        return self.upload_data


