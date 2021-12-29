import grpc
import time
import cv2
import numpy as np
from concurrent import futures
import sys
sys.path.append('./')
import detect

sys.path.append('../example')
# sys.path

from example import data_pb2, data_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
#_HOST = 'localhost'
_HOST = '192.168.101.117'
_PORT = '8020'
MAX_MESSAGE_LENGTH = 256 * 1024 * 1024


class FormatData(data_pb2_grpc.FormatDataServicer):
    def DoFormat(self, request, context):
        nparr = np.fromstring(request.encoded_image, dtype=np.int8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        # cv2.namedWindow("test", cv2.WINDOW_NORMAL)
        # cv2.imshow("test", image)
        # cv2.waitKey(1000)
        objs = detect.detectserver(image)
        print(objs)
        obj_list = []
        object=""
        for obj in objs:
           object = data_pb2.Object(rbox=data_pb2.Rbox(x=obj['rbox']['x'],y=obj['rbox']['y'],w=obj['rbox']['w'],h=obj['rbox']['h'],theta=obj['rbox']['theta']),
                                   class_name=obj['class_name'], score=obj['conf'])
           obj_list.append(object)
        return data_pb2.Response(objects=obj_list)


def serve():
    grpcServer = grpc.server(futures.ThreadPoolExecutor(max_workers=4), options=[
        ('grpc.max_send_message_length', MAX_MESSAGE_LENGTH),
        ('grpc.max_receive_message_length', MAX_MESSAGE_LENGTH),
    ])
    data_pb2_grpc.add_FormatDataServicer_to_server(FormatData(), grpcServer)
    grpcServer.add_insecure_port(_HOST + ':' + _PORT)
    grpcServer.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        grpcServer.stop(0)


if __name__ == '__main__':
    serve()