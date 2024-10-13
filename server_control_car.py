# Christopher Rock (cmrock2)
# CS 437 IOT Fall 2024
# Lab 2: LTE: Self-Driving Car - Networking

import picar_4wd as fc
import time
import math
import threading


POW = 50
path = []
keep_running = True  # flag to break out of loop when exiting


def right_turn():
    fc.left_front.set_power(POW)
    fc.left_rear.set_power(POW)
    fc.right_front.set_power(-POW)
    fc.right_rear.set_power(-POW)


def left_turn():
    fc.left_front.set_power(-POW)
    fc.left_rear.set_power(-POW)
    fc.right_front.set_power(POW)
    fc.right_rear.set_power(POW)


def spin(turn_angle):
    init()
    if turn_angle == 0:
        return True
    # print(f"--> Spinning {turn_angle} degrees")
    SLIP = 0.6  # used to account for wheel slip
    SLEEP_TIME = 0.05
    CIRC = math.pi * 14
    delta_theta = 0
    turned_dist = 0
    turn_func = right_turn
    if turn_angle < 0:
        turn_func = left_turn
    turn_angle = abs(turn_angle)
    while delta_theta < turn_angle:
        start_time = time.time()
        turn_func()
        time.sleep(SLEEP_TIME)
        rt_speed = fc.right_rear_speed()  # get instantaneous speed
        lt_speed = fc.left_rear_speed()  # get instantaneous speed
        fc.stop()
        runtime = time.time() - start_time
        # speeds are returned in cm/s, use our averaged turn speed
        turned_dist += ((rt_speed + lt_speed) / 2) * runtime
        # print(
        #     f"left: {round(lt_speed,2)}cm/s right:{round(rt_speed,2)}cm/s ({round(runtime,2)}s)"
        # )
        delta_theta = (turned_dist / CIRC) * 360 * SLIP
    # print("spun", delta_theta, "degrees")
    return delta_theta


# move a certain number of centimeters forward (can also go backward)
def move_dist(dist_goal):
    init()
    # print(f"--> Moving {dist_goal}")
    delta = 0
    SLEEP_TIME = 0.005
    while delta < abs(dist_goal):
        while pebglobal.obstacle_detected:
            time.sleep(1)
        start_time = time.time()
        fc.forward(POW)
        time.sleep(SLEEP_TIME)
        rt_speed = fc.right_rear_speed()  # get instantaneous speed
        lt_speed = fc.left_rear_speed()  # get instantaneous speed
        # print("speeds:", lt_speed, rt_speed)
        fc.stop()
        runtime = time.time() - start_time
        delta += ((rt_speed + lt_speed) / 2) * runtime
        # print(delta, runtime)
    # print("moved", delta, "cm")
    return delta


def add_move(new_move):
    global path
    if new_move == "forward":
        path.append((0, 5))
    elif new_move == "back":
        path.append((0, -5))
    elif new_move == "left":
        path.append((-45, 0))
    elif new_move == "right":
        path.append((45, 0))


def follow_moves():
    print("========== STARTING FOLLOW MOVES THREAD =============")
    global path, keep_running
    try:
        while keep_running:
            if len(path) > 0:
                next_move = path[0]
                path = path[1:]
                print("Doing next move:", next_move)
                spin(next_move[0])
                move_dist(next_move[1])
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Program stopped by the user.")


def get_status():
    curr_speed = fc.speed_val()
    cpu_temp = fc.cpu_temperature()
    pow = fc.power_read()
    # Create a formatted string containing all the information
    status = f"Current Speed: {curr_speed} units, CPU Temperature: {cpu_temp} °C, Power: {pow} watts"
    return status


def init():
    global move_thread
    fc.right_rear_speed.start()  # start monitoring speed thread
    fc.left_rear_speed.start()  # start monitoring speed thread
    move_thread = threading.Thread(target=follow_moves)
    move_thread.start()


def cleanup():
    global move_thread, keep_running
    print("Sweeping up motors...")
    fc.right_rear_speed.deinit()  # stop thread
    fc.left_rear_speed.deinit()  # stop thread
    fc.stop()
    keep_running = False  # signal to break out of loop
    move_thread.join()
