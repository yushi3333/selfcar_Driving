

from __future__ import print_function


# ==============================================================================
# -- find carla module ---------------------------------------------------------
# ==============================================================================


import glob
import os
import sys
import random
import time
import numpy as np
import cv2

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass


import carla
IM_WIDTH = 640
IM_HEIGHT = 480

def process_img(image):
    i = np.array(image.raw_data)
    print(i.shape)
    i2 = i.reshape((IM_HEIGHT, IM_WIDTH, 4))
    #height, weight, first three rgb values
    i3 = i2[:, :, :3]
    cv2.imshow("", i3)
    cv2.waitKey(1)
    return i3/255.0




actor_list = []
try:
    client =carla.Client('localhost', 2000)
    client.set_timeout(10.0)
    world = client.get_world()
    blueprint_library = world.get_blueprint_library()

    #pick a car
    bp = blueprint_library.filter('model3')[0]
    print(bp)

    spawn_point = random.choice(world.get_map().get_spawn_points())
    vehicle = world.spawn_actor(bp, spawn_point)
    #vehicle.set_autopilot(True) #want some NPC cars to drive
    vehicle.apply_control(carla.VehicleControl(throttle=1.0, steer = 0.0))
    actor_list.append(vehicle)

#set up camera sensor
    cam_bp = blueprint_library.find('sensor.camera.rgb')
    cam_bp.set_attribute('image_size_x', f"{IM_WIDTH}")
    cam_bp.set_attribute('image_size_y', f"{IM_HEIGHT}")
    cam_bp.set_attribute('fov', '110')

    spawn_point = carla.Transform(carla.Location(x=2.5, z=0.7))
    sensor=world.spawn_actor(cam_bp, spawn_point, attach_to=vehicle)
    actor_list.append(sensor)
    sensor.listen(lambda data: process_img(data))



    time.sleep(10)

    pass
finally:
    for actor in actor_list:
        actor.destroy()
    print("ALL clean up done!")

