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

    def update_all(self):
        result = self.firebase.put('/', 'Car_Info', {"Door_lock": self.door_lock,
                                                     "Gear": self.gear,
                                                     "Light": self.light,
                                                     "Pedal": {
                                                         "Gas_pedal": self.gas_pedal,
                                                         "Brake_pedal": self.brake_pedal,
                                                         "Foot_brake_pedal": self.foot_brake_pedal
                                                     },
                                                     "Speed": self.speed,
                                                     "Steering": self.steering
                                                     })
        if result is False:
            logging.error('Update error')
        else:
            logging.info('Update all')

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

