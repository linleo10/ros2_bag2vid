#!/usr/bin/env python3
import os

import cv2
from cv_bridge import CvBridge
import rosbag2_py as rosbag2
import rclpy
import rclpy.serialization

from sensor_msgs.msg import Image

def getBagPath(root_dir):
    bag_paths = []
    for subdir, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.db3'):
                bag_paths.append(os.path.join(subdir, file))
    return bag_paths

def convert(bag_path):
    fps = 1.0 / 0.25
    fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
    is_init = False
    reader = rosbag2.SequentialReader()
    storage_options = rosbag2.StorageOptions(uri=bag_path, storage_id='sqlite3')
    converter_options = rosbag2.ConverterOptions(input_serialization_format='cdr', output_serialization_format='cdr')
    
    try:
        reader.open(storage_options, converter_options)
    except:
        return
    print("--- BAG FILE OPENED ---")

    try:
        while reader.has_next():
            serialized_msg = reader.read_next()
            deserialized_msg = rclpy.serialization.deserialize_message(serialized_msg[1], Image)
            # msg = deserialier.message

            bridge = CvBridge()
            image = bridge.imgmsg_to_cv2(deserialized_msg, desired_encoding="bgr8")

            if not is_init:
                filename = bag_path.split("/")[-1].split(".db3")[0]
                writer = cv2.VideoWriter("{0}.avi".format(filename), fourcc, fps, (deserialized_msg.width, deserialized_msg.height))
                is_init = True

            writer.write(image)
    except cv2.error as e:
        print(f"Error converting image: {e}")
        return

    print("Finished...")
    # reader.close()
    # writer.release()

if __name__ == '__main__':
    # convert()
    bag_paths = getBagPath('/home/ttt/video/num_3/')

    for bag_path in bag_paths:
        convert(bag_path)
```