# Christopher Rock (cmrock2)
# CS 437 IOT Fall 2024
# Lab 2: LTE: Self-Driving Car - Networking

import picar_4wd as fc
import time

POW = 100


def right_turn():
    fc.left_front.set_power(POW)
    fc.left_rear.set_power(POW)
    fc.right_front.set_power(-POW)
    fc.right_rear.set_power(-POW)
    time.sleep(0.3)
    fc.stop()


def left_turn():
    fc.left_front.set_power(-POW)
    fc.left_rear.set_power(-POW)
    fc.right_front.set_power(POW)
    fc.right_rear.set_power(POW)
    time.sleep(0.3)
    fc.stop()


def move_forward():
    fc.forward(POW)
    time.sleep(0.5)
    fc.stop()


def move_backward():
    fc.backward(POW)
    time.sleep(0.5)
    fc.stop()


def get_status():
    cpu_temp = fc.cpu_temperature()
    cpu_usage = fc.cpu_usage()
    pow = fc.power_read()
    status = (
        f"CPU Temperature: {cpu_temp}°C, CPU Usage: {cpu_usage}%, Power: {pow} watts"
    )
    return status
