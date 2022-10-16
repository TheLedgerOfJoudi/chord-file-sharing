from asyncio.proactor_events import constants
import chord_pb2_grpc as pb2_grpc
import chord_pb2 as pb2
import grpc
from concurrent import futures
import sys
import random
import zlib
import time
import threading

reg_ip, reg_port = sys.argv[1].split(":")
node_ip, node_port = sys.argv[2].split(":")

data = ""
finger_table = []
m = -1
id = -1
succ = -1
pred = -1


def get_finger_table():
    return finger_table


def save(key, text):
    hash_value = zlib.adler32(key.encode())
    target_id = hash_value % (2**m)
    if target_id in range(pred, id + 1):
        data = text
    elif target_id in range(id + 1, finger_table[0] + 1):
        channel = grpc.insecure_channel(reg_ip + ":" + reg_port)
        stub = pb2_grpc.ChordStub(channel)
        out = stub.GetChordInfo()
        for i in range(len(out.ids)):
            if succ == out.ids[i]:
                succ_channel = out.values[i]
                break
        channel = grpc.insecure_channel(succ_channel)
        stub = pb2_grpc.ChordStub(channel)
        out = stub.SaveData(pb2.SaveDataMessage(key=succ, text=text))
    else:
        for i in range(len(finger_table) - 1):
            if target_id >= finger_table[i] and target_id < finger_table[i + 1]:
                next = i
                break
        channel = grpc.insecure_channel(reg_ip + ":" + reg_port)
        stub = pb2_grpc.ChordStub(channel)
        out = stub.GetChordInfo()
        for i in range(len(out.ids)):
            if next == out.ids[i]:
                next_channel = out.values[i]
                break
        channel = grpc.insecure_channel(next_channel)
        stub = pb2_grpc.ChordStub(channel)
        out = stub.SaveData(pb2.SaveDataMessage(key=next, text=text))


def remove(key):
    return


def find(key):
    return key


def quit():
    return


class NodeHandler(pb2_grpc.ChordServicer):
    def SaveData(self, request, context):
        key = request.key
        text = request.text
        save(key, text)

    def GetFingerTable(self, request, context):
        channels = []
        channel = grpc.insecure_channel(reg_ip + ":" + reg_port)
        stub = pb2_grpc.ChordStub(channel)
        print(stub)
        out = stub.GetChordInfo(pb2.GetChordInfoMessage(message="hi"))
        print(out)
        for node_id in finger_table:
            for i in range(len(out.ids)):
                if node_id == out.ids[i]:
                    channels.append(out.channels[i])
                    break
        reply = {"node_id": id, "ids": finger_table, "channels": channels}
        return pb2.GetFingerTableResponse(**reply)


if __name__ == "__main__":
    channel = grpc.insecure_channel(reg_ip + ":" + reg_port)
    stub = pb2_grpc.ChordStub(channel)
    out = stub.Register(pb2.RegisterMessage(ipaddr=node_ip, port=int(node_port)))
    id, m = out.id, out.m
    node = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_ChordServicer_to_server(NodeHandler(), node)
    node.add_insecure_port("127.0.0.1:" + str(node_port))
    node.start()
    while True:
        time.sleep(1)
        finger_table_response = stub.PopulateFingerTable(
            pb2.PopulateFingerTableMessage(id=id)
        )
        finger_table = finger_table_response.fingers
        pred = finger_table_response.pred
    try:
        node.wait_for_termination()
    except KeyboardInterrupt:
        print("Shutting down")
