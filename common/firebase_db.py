import logging
from firebase import firebase


class Car2Firebase(object):
    def __init__(self):
        self.firebase = firebase.FirebaseApplication('https://smartcar-87e42.firebaseio.com/', None)
        self.door_lock = False
        self.gear = 0
        self.light = 0
        self.gas_pedal = False
        self.brake_pedal = 0
        self.foot_brake_pedal = True
        self.speed = 0
        self.steering = 0

    def upload_all(self, can_recv):
        if can_recv:
            # Gear status update
            if can_recv['gear_1'] == 32:        # P
                self.gear = 0
            elif can_recv['gear_1'] == 34:      # N
                self.gear = 1
            elif can_recv['gear_1'] == 35:      # D
                self.gear = 2
            else:                               # R
                self.gear = 3

            # Brake status update
            if can_recv['brake_LI'] == 1:
                self.brake_pedal = 1
            elif can_recv['brake_H'] == 1:
                self.brake_pedal = 2
            else:
                self.brake_pedal = 0

            # Foot Brake status update
            if can_recv['handcrat'] == 1:
                self.foot_brake_pedal = True
            else:
                self.foot_brake_pedal = False

            # Light status update
            if can_recv['LIGHT_SMALL'] == 1:
                self.light = 1
            elif can_recv['LIGHT_BIG'] == 1:
                self.light = 2
            elif can_recv['LIGHT_FLASH'] == 1:
                self.light = 3
            else:
                self.light = 0

            # Door status update
            if can_recv['door_lock'] in [0x00, 0x01]:        # close
                self.door_lock = False
            elif can_recv['door_lock'] == [0x80, 0x81]:      # open
                self.door_lock = True

            result = self.firebase.put('/', 'Car_Info', {"Door_lock": self.door_lock,
                                                         "Gear": self.gear,
                                                         "Light": self.light,
                                                         "Pedal": {
                                                             "Gas_pedal": self.gas_pedal,
                                                             "Brake_pedal": self.brake_pedal,
                                                             "Foot_brake_pedal": self.foot_brake_pedal
                                                         },
                                                         "Speed": int(can_recv['SPEED']),
                                                         "Steering": can_recv['wheel_angle']
                                                         })
            # print("SPEED {}".format(int(can_recv['SPEED'])))
            # print("WHEEL {}".format(can_recv['wheel_angle']))
            # print("speed type {}".format(type(can_recv['SPEED'])))
            # print("wheel type {}".format(type(can_recv['wheel_angle'])))
            if result is False:
                logging.error('Update error')
            else:
                logging.info('Update all')

    def upload_test(self):
        result = self.firebase.put('/', 'Car_Info', {"Door_lock": self.door_lock,
                                                     "Gear": 1,
                                                     "Light": self.light,
                                                     "Pedal": {
                                                         "Gas_pedal": self.gas_pedal,
                                                         "Brake_pedal": self.brake_pedal,
                                                         "Foot_brake_pedal": self.foot_brake_pedal
                                                     },
                                                     "Speed": 20,
                                                     "Steering": -5
                                                     })
        if result is False:
            print('Update error')
        else:
            print('Update all')

    def update_speed(self, speed):
        self.speed = speed
        result = self.firebase.put('/Car_Info', 'Speed', self.speed)
        if result is False:
            logging.error('Update error')
        else:
            logging.info('Update speed')

    def update_steer(self, steer):
        self.steering = steer
        result = self.firebase.put('/Car_Info', 'Steering', self.steering)
        if result is False:
            logging.error('Update error')
        else:
            logging.info('Update steer')

    def update_pedal(self, pedal):
        self.gas_pedal, self.brake_pedal, self.foot_brake_pedal = pedal
        result = self.firebase.put('/Car_Info', 'Pedal', {"Gas_pedal": self.gas_pedal,
                                                          "Brake_pedal": self.brake_pedal,
                                                          "Foot_brake_pedal": self.foot_brake_pedal},)
        if result is False:
            logging.error('Update error')
        else:
            logging.info('Update pedal')


if __name__ == "__main__":
    car2firebase = Car2Firebase()
    car2firebase.upload_test()
