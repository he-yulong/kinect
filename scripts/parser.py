# -*- coding: utf-8 -*-  
"""
hello
"""

import json
import numpy as np

filename = '../Kinect/Kinect/result.json'

with open(filename,'r') as f:
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
data = np.concatenate((pos_data, confidence_data), axis=2)

print(data)
print(data.shape)

np.save('parsed_data', data)

