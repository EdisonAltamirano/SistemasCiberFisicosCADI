#!/usr/bin/env python3
# Software License Agreement (BSD License)
#
# Copyright (c) 2019, UFACTORY, Inc.
# All rights reserved.
#
# Author: Vinman <vinman.wen@ufactory.cc> <vinman.cub@gmail.com>

"""
Description: Move Joint
"""

import os
import sys
import time
import math
from pyModbusTCP.client import ModbusClient
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

from xarm.wrapper import XArmAPI


#######################################################
"""
Just for test example
"""
if len(sys.argv) >= 2:
    ip = sys.argv[1]
else:
    try:
        from configparser import ConfigParser
        parser = ConfigParser()
        parser.read('../robot.conf')
        ip = parser.get('xArm', 'ip')
    except:
        ip = "192.168.31.180"
        #ip = input('Please input the xArm ip address:')
        if not ip:
            print('input error, exit')
            sys.exit(1)
########################################################
try:
    myhost = "10.22.240.51"
    myport = 12345
    c = ModbusClient(host=myhost,port=myport)
    if c.open():
        c.write_multiple_registers(0, [200])     
except Exception as error:
    print("Writing registers not ready")
    print(error)

arm = XArmAPI(ip)
arm.motion_enable(enable=True)
arm.set_mode(0)
arm.set_state(state=0)

arm.reset(wait=True)

speed = 50
arm.set_servo_angle(angle=[90, 0, 0, 0, 0], speed=speed, wait=True)
print(arm.get_servo_angle(), arm.get_servo_angle(is_radian=True))
try:
    if c.open():
        c.write_multiple_registers(15, [90,0,0,0,0])     
except Exception as error:
    print("Writing registers not ready")
    print(error)
arm.set_servo_angle(angle=[90, 0, -60, 0, 0], speed=speed, wait=True)
print(arm.get_servo_angle(), arm.get_servo_angle(is_radian=True))
try:
    if c.open():
        c.write_multiple_registers(15, [90,0,1160,0,0])     
except Exception as error:
    print("Writing registers not ready")
    print(error)
arm.set_servo_angle(angle=[90, -30, -60, 0, 0], speed=speed, wait=True)
try:
    if c.open():
        c.write_multiple_registers(15, [90,1130,1160,0,0])     
except Exception as error:
    print("Writing registers not ready")
    print(error)
print(arm.get_servo_angle(), arm.get_servo_angle(is_radian=True))
arm.set_servo_angle(angle=[0, -30, -60, 0, 0], speed=speed, wait=True)
try:
    if c.open():
        c.write_multiple_registers(15, [0,1130,1160,0,0])     
except Exception as error:
    print("Writing registers not ready")
    print(error)
print(arm.get_servo_angle(), arm.get_servo_angle(is_radian=True))
arm.set_servo_angle(angle=[0, 0, -60, 0, 0], speed=speed, wait=True)
try:
    if c.open():
        c.write_multiple_registers(15, [0,0,1160,0,0])     
except Exception as error:
    print("Writing registers not ready")
    print(error)
print(arm.get_servo_angle(), arm.get_servo_angle(is_radian=True))
arm.set_servo_angle(angle=[0, 0, 0, 0, 0], speed=speed, wait=True)
try:
    if c.open():
        c.write_multiple_registers(15, [0,0,0,0,0])     
except Exception as error:
    print("Writing registers not ready")
    print(error)
print(arm.get_servo_angle(), arm.get_servo_angle(is_radian=True))


#arm.reset(wait=True)
#speed = math.radians(50)
#arm.set_servo_angle(angle=[math.radians(90), 0, 0, 0, 0], speed=speed, is_radian=True, wait=True)
#print(arm.get_servo_angle(), arm.get_servo_angle(is_radian=True))
#arm.set_servo_angle(angle=[math.radians(90), 0, math.radians(-60), 0, 0], speed=speed, is_radian=True, wait=True)
#print(arm.get_servo_angle(), arm.get_servo_angle(is_radian=True))
#arm.set_servo_angle(angle=[math.radians(90), math.radians(-30), math.radians(-60), 0, 0], speed=speed, is_radian=True, wait=True)
#print(arm.get_servo_angle(), arm.get_servo_angle(is_radian=True))
#arm.set_servo_angle(angle=[0, math.radians(-30), math.radians(-60), 0, 0], speed=speed, is_radian=True, wait=True)
#print(arm.get_servo_angle(), arm.get_servo_angle(is_radian=True))
#arm.set_servo_angle(angle=[0, 0, math.radians(-60), 0, 0], speed=speed, is_radian=True, wait=True)
#print(arm.get_servo_angle(), arm.get_servo_angle(is_radian=True))
#arm.set_servo_angle(angle=[0, 0, 0, 0, 0], speed=speed, is_radian=True, wait=True)
#print(arm.get_servo_angle(), arm.get_servo_angle(is_radian=True))

arm.reset(wait=True)
arm.disconnect()


