"""
Using kinect's own confidence
"""
import os
import argparse
import json
import math
import time
# import cv2
import numpy as np
from plot_3d import Visual3D

# Dictionary containing some colors:
COLOR = {'blue': (255, 0, 0), 'green': (0, 255, 0), 'red': (0, 0, 255), 'yellow': (0, 255, 255),
         'magenta': (255, 0, 255), 'cyan': (255, 255, 0), 'white': (255, 255, 255), 'black': (0, 0, 0),
         'gray': (125, 125, 125), 'rand': np.random.randint(0, high=256, size=(3,)).tolist(),
         'dark_gray': (50, 50, 50), 'light_gray': (220, 220, 220)}


def get_image_path(image_dir):
    """
    Get list of image path.
    :param image_dir:
    :return:
    """
    image_path = []
    idx = 1
    path = '{}color-{}.png'.format(image_dir, idx)
    while os.path.exists(path):
        path = '{}color-{}.png'.format(image_dir, idx)
        image_path.append(path)
        idx += 1
    return image_path


class StateManager:
    def __init__(self, max_frame_count=30, max_occulated_count=2):
        self.max_frame_count = max_frame_count
        self.max_occulated_count = max_occulated_count

        self.is_occulated = False
        self.occulated_count = 0
        self.frame_count = 0

        self.bag = []
        self.prev_xy = None
        self.delta = 2

    def _set_state(self, max_frame_count, max_occulated_count):
        self.max_frame_count = max_frame_count
        self.max_occulated_count = max_occulated_count

    def get_state(self):
        if self.occulated_count >= self.max_occulated_count:
            self.is_occulated = True
        else:
            self.is_occulated = False
        return self.is_occulated

    def forward(self, diff, status):
        if status:
            self.bag.append(diff)
            if len(self.bag) >= 10:
                self.bag = self.bag[1:]
                norm = np.linalg.norm(self.bag)
                print(self.bag)
                print('norm: ', norm)
                if norm > 40:
                    print('speed quick!!!!!!')
                    self._set_state(3, 1)
                else:
                    print('speed slow......')
                    self._set_state(30, 2)

        self.frame_count += 1
        if self.frame_count >= self.max_frame_count:
            self._refresh()

    def increment_occlusion(self):
        self.occulated_count += 1

    def _refresh(self):
        # self.is_occulated = False
        self.frame_count = 0
        self.occulated_count = 0


class OcclusionAwarer:
    interesting_points = [6, 7, 13, 14, 19, 20, 21, 23, 24, 25]
    # interesting_points = [6, 7, 13, 14]
    state_manager = {}
    for key in interesting_points:
        state_manager[key] = StateManager()

    def __init__(self, images, keypoints):
        self.images = images
        self.frame = None
        self.keypoints = keypoints
        self.frame_idx = 0

        # self.prev_gray = self.get_gray_frame()
        self.prev_frame_keypoints = self.get_frame_keypoints('float32')
        self.curr_frame_keypoints_float = None

        self.diff_list = []

        self.v3d1 = Visual3D()
        # self.v3d2 = Visual3D()
        # self.v3d3 = Visual3D()

    # def get_frame(self):
    #     self.frame = cv2.imread(self.images[self.frame_idx])
    #     return self.frame
    #
    # def get_gray_frame(self):
    #     return cv2.cvtColor(self.get_frame(), cv2.COLOR_BGR2GRAY)

    def get_frame_keypoints(self, type):
        if type == 'int':
            frame_keypoints = self.keypoints[self.frame_idx, :, :3].astype(np.int)
            confidence = self.keypoints[self.frame_idx, :, 3]
            return frame_keypoints, confidence
        elif type == 'float32':
            frame_keypoints = self.keypoints[self.frame_idx, :, :4].astype(np.float32).reshape((1, -1, 4))
            return frame_keypoints
        else:
            print('get_frame_keypoints: type is wrong!')

    def _update(self):
        # Updates previous good feature points
        self.prev_frame_keypoints = self.get_frame_keypoints('float32')
        self.frame_idx += 1

    def _display(self):
        # color_frame = self.get_frame()
        # image_position, confidence = self.get_frame_keypoints('int')
        # Display Image
        print('#' * 40)
        print('frame: ', self.frame_idx)
        # for i in self.interesting_points:
        #     diff = self.curr_frame_keypoints_float[0, i, :] - self.prev_frame_keypoints[0, i, :]
        #     status = (confidence[i] >= 1.1)
        #     xy = tuple(image_position[i, :])
        #     print('node: ', i)
        #     print('status', status)
        #     self.state_manager[i].forward(diff, status)
        #     if confidence[i] < 1.1:
        #         self.state_manager[i].increment_occlusion()
        #     if self.state_manager[i].get_state():
        #         # if really on occlusion
        #         pass
        #     else:
        #         pass

        # print(self.curr_frame_keypoints_float)
        # print(self.curr_frame_keypoints_float.shape)
        # exit(0)
        a = self.curr_frame_keypoints_float[0, :, 3]
        all_good_confidence = self.curr_frame_keypoints_float[0, :, 3].copy()
        all_good_confidence.fill(4.0)
        self.v3d1.plot_3d(self.curr_frame_keypoints_float[0, :, :3], all_good_confidence)
        # self.v3d2.plot_3d(self.curr_frame_keypoints_float[0, :, :3], self.curr_frame_keypoints_float[0, :, 3])
        print('-' * 10)
        # cv2.imshow('loaded image', color_frame)
        # if (cv2.waitKey(1) & 0xFF) == ord('q'):
        #     self.close()
        #     exit(0)

        print('#' * 40)

        # return color_frame.copy()

    def process(self):
        self.curr_frame_keypoints_float = self.get_frame_keypoints('float32')
        frame = self._display()
        self._update()
        return frame

    def _check_distribution(self):
        print('arr_mean', np.mean(self.diff_list))
        print('arr_var', np.var(self.diff_list))
        print('arr_std', np.std(self.diff_list))

    def close(self):
        self._check_distribution()
        # cv2.destroyAllWindows()

    def is_empty(self):
        # return self.frame_idx == min(len(self.images), len(self.keypoints)) - 3
        return self.frame_idx == 900


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--image_dir', default='./data/20191126/', help='image directory.')
    parser.add_argument('--json_filename', default='./result_output4_smooth1.0.json', help='json filename.')
    parser.add_argument("--output_path", default='./result.mp4', help="path to the video file to write")
    args = parser.parse_args()

    with open(args.json_filename, 'r') as f:
        data = json.load(f)

    print(data.keys())
    body_per_frame = data['frames'][120]
    print(body_per_frame['bodies'][0].keys())

    pos = []
    confidence = []

    for bodies_per_frame in data['frames']:
        if bodies_per_frame['bodies']:
            body = bodies_per_frame['bodies'][0]
            # print(body.keys())
            # print(body['body_id'])
            # print(body['joint_orientations'])
            # print(body['joint_positions'])
            # print(body['joint_confidence'])
            pos.append(body['joint_positions'])

            confidence.append(body['joint_confidence'])
        else:
            pos.append(np.zeros((32, 3)).tolist())
            confidence.append(np.zeros((32, 1)).tolist())

    pos_data = np.array(pos).reshape((-1, 32, 3))
    confidence_data = np.array(confidence).reshape((-1, 32, 1))

    # get image path
    # image_path = get_image_path(args.image_dir)
    image_path = None
    # get keypoints data
    keypoints = np.concatenate((pos_data, confidence_data), axis=2)

    awarer = OcclusionAwarer(image_path, keypoints)

    while not awarer.is_empty():
        awarer.process()

    awarer.close()
