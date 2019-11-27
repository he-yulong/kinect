import sys

sys.path.append('../')

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
# from mlp_plot.transformation import Coordinate
from numpy import array
import time


class KeypointsMap:

    def __init__(self, index, name, parent):
        self.index = index
        self.name = name
        self.parent = parent


KEYPOINTS_CONFIG = [[0, 'PELVIS', None],
                    [1, 'SPINE_NAVAL', ]
                    ]

NODE_NAME = [
    'PELVIS', 'SPINE_NAVAL', 'SPINE_CHEST', 'NECK', 'CLAVICLE_LEFT',
    'SHOULDER_LEFT', 'ELBOW_LEFT', 'WRIST_LEFT', 'HAND_LEFT', 'HANDTIP_LEFT',
    'THUMB_LEFT', 'CLAVICLE_RIGHT', 'SHOULDER_RIGHT', 'ELBOW_RIGHT', 'WRIST_RIGHT',
    'HAND_RIGHT', 'HANDTIP_RIGHT', 'THUMB_RIGHT', 'HIP_LEFT', 'KNEE_LEFT',
    'ANKLE_LEFT', 'FOOT_LEFT', 'HIP_RIGHT', 'KNEE_RIGHT', 'ANKLE_RIGHT',
    'FOOT_RIGHT', 'HEAD', 'NOSE', 'EYE_LEFT', 'EAR_LEFT',
    'EYE_RIGHT', 'EAR_RIGHT'
]


class Visual3D:
    def __init__(self):
        fig = plt.figure(figsize=(12, 8))
        self.ax = Axes3D(fig)

        self.connect_map = [[0, 0, 0, 1, 2,
                             2, 2, 3, 4, 5,
                             6, 7, 7, 8, 11,
                             12, 13, 14, 14, 15,
                             18, 19, 20, 22, 23,
                             24, 26, 26, 26, 26,
                             26, ],
                            [1, 18, 22, 2, 3,
                             4, 11, 26, 5, 6,
                             7, 8, 10, 9, 12,
                             13, 14, 15, 17, 16,
                             19, 20, 21, 23, 24,
                             25, 27, 28, 29, 30,
                             31, ]]
        self.frame = 0
        self.fingers = [8, 9, 10, 15, 16, 17]
        # 坐标变换
        # axis1 = np.eye(3)
        # # axis2 = np.array([[0, 1, 0], [0, 0, 1], [-1, 0, 0]])
        # axis2 = np.array([[-1, 0, 0], [0, 0, 1], [0, -1, 0]])
        # # axis2 = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
        # orgin1 = np.array([[0, 0, 0]])
        # orgin2 = np.array([[0, 0, 0]])
        # self.coordinate = Coordinate(axis1, axis2, orgin1, orgin2)

    def plot_3d(self, person, confidence):
        self.ax.clear()
        # self.ax.plot(person[:, 0], person[:, 1], person[:, 2], 'co', markersize=7, zdir='z')
        # for i in range(person.shape[0]):
        #     self.ax.text(person[i, 0], person[i, 1], person[i, 2], NODE_NAME[i])

        for m, n in zip(self.connect_map[0], self.connect_map[1]):
            if (m in self.fingers) or (n in self.fingers):
                continue
            if confidence[m] >= 1.1 and confidence[n] >= 1.1:
                self.ax.plot((person[m][0], person[n][0]), (person[m][1], person[n][1]),
                             (person[m][2], person[n][2]),
                             lw=4, alpha=0.8, zdir='z')

        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.set_zlabel("Z")
        self.ax.set_xlim(-1200, 1200)
        self.ax.set_ylim(-1000, 1000)
        self.ax.set_zlim(2000, 2900)
        self.ax.set_title(str(self.frame))
        plt.pause(0.0001)

        self.frame += 1


if __name__ == '__main__':
    data_input = np.array([[134.349, -39.7078, 2535.55],
                           [129.783, -214.685, 2505.48],
                           [131.471, -356.037, 2492.2],
                           [137.509, -571.957, 2484.91],
                           [159.677, -537.643, 2494.98],
                           [294.016, -580.002, 2474.72],
                           [568.912, -569.624, 2476.47],
                           [797.945, -543.37, 2463.6],
                           [880.794, -517.25, 2423.07],
                           [944.235, -563.641, 2349.63],
                           [931.483, -573.053, 2417.06],
                           [109.082, -537.686, 2500.23],
                           [-18.5966, -563.012, 2486.22],
                           [-298.815, -569.716, 2484.81],
                           [-532.015, -577.184, 2469.61],
                           [-634.838, -572.831, 2461.75],
                           [-730.269, -591.419, 2503.31],
                           [-664.278, -560.546, 2531.8],
                           [224.589, -40.3812, 2525.77],
                           [250.683, 342.898, 2631.81],
                           [285.573, 692.248, 2779.46],
                           [300.229, 797.688, 2626.33],
                           [52.9758, -39.0971, 2544.38],
                           [46.5715, 346.963, 2641.34],
                           [56.9407, 709.513, 2770.11],
                           [12.2987, 799.955, 2631.3],
                           [135.496, -646.181, 2451.75],
                           [113.956, -699.875, 2302.62],
                           [155.732, -727.666, 2326.85],
                           [229.625, -713.531, 2428.17],
                           [86.908, -730.067, 2334.39],
                           [42.501, -719.928, 2456.61]])

    print(data_input.shape)
    print(data_input)
    v3d = Visual3D()
    while True:
        v3d.plot_3d(data_input)
        time.sleep(0.2)
