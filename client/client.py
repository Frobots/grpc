import grpc
import sys
import sys
import cv2
import json
import numpy as np

sys.path.append('../example')

from example import data_pb2, data_pb2_grpc

# sys.path.append(r'C:\Users\huaru\PycharmProjects\GRPC_demo')

#_HOST = 'localhost'
#_PORT = '8080'
_HOST = '192.168.101.117'
_PORT = '8020'


def run():
    conn = grpc.insecure_channel(_HOST + ':' + _PORT)
    client = data_pb2_grpc.FormatDataStub(channel=conn)
    image = cv2.imread("img2.jpg")
    img = cv2.imencode('.jpg', image)[1]
    data_encode = np.array(img)
    test_bytes = data_encode.tostring()
    response = client.DoFormat(data_pb2.Request(encoded_image=test_bytes, width=image.shape[1], height=image.shape[0]))
    print("received: ", response)


if __name__ == '__main__':
    run()