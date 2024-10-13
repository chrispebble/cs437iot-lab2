# Christopher Rock
# for CS 437 IOT, Fall 2024

import picar_4wd as fc
import time
import math

POW = 50


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


def follow_moves(path):
    init()
    print("========== STARTING FOLLOW MOVES =============")
    print(path)
    for i, step in enumerate(path):
        # print("MOVING!", step)
        spin(step[0])
        move_dist(step[1])
    print("SUCCESS ALL MOVES COMPLETE")
    return True


initialized = False


def init():
    global initialized
    if not initialized:
        fc.right_rear_speed.start()  # start monitoring speed thread
        fc.left_rear_speed.start()  # start monitoring speed thread
        initialized = True


def cleanup():
    if initialized:
        print("Sweeping up motors...")
        fc.right_rear_speed.deinit()  # stop thread
        fc.left_rear_speed.deinit()  # stop thread
    fc.stop()


if __name__ == "__main__":
    try:
        init()
        path = [
            (0, 1.4),
            (0, 1.4),
            (0, 1.4),
            (0, 1.4),
            (0, 1.4),
            (0, 1.4),
            (0, 1.4),
            (45, 1),
            (0, 1),
            (0, 1),
            (0, 1),
            (0, 1),
            (0, 1),
        ]
        follow_moves(path)

    finally:
        cleanup()
