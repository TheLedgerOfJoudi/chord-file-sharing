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

data = {}
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
    channel = grpc.insecure_channel(reg_ip + ":" + reg_port)
    stub = pb2_grpc.ChordStub(channel)
    out = stub.GetChordInfo(pb2.GetChordInfoMessage(message="hi"))
    if target_id in range(pred, id + 1) or len(out.ids) == 1:
        if data.get(key):
            return "False", id
        data[key] = text
        return "True", id
    elif target_id in range(id + 1, finger_table[0] + 1):
        channel = grpc.insecure_channel(reg_ip + ":" + reg_port)
        stub = pb2_grpc.ChordStub(channel)
        out = stub.GetChordInfo(pb2.GetChordInfoMessage(message="hi"))
        for i in range(len(out.ids)):
            if finger_table[0] == out.ids[i]:
                succ_channel = out.channels[i]
                break
        channel = grpc.insecure_channel(succ_channel)
        stub = pb2_grpc.ChordStub(channel)
        out = stub.SaveData(pb2.SaveDataMessage(key=key, text=text))
        return out.status, out.node_id
    else:
        next = -1
        next_channel = ""
        for i in range(len(finger_table) - 1):
            if target_id >= finger_table[i] and target_id < finger_table[i + 1]:
                next = finger_table[i]
                break
        channel = grpc.insecure_channel(reg_ip + ":" + reg_port)
        stub = pb2_grpc.ChordStub(channel)
        out = stub.GetChordInfo(pb2.GetChordInfoMessage(message="hi"))
        for i in range(len(out.ids)):
            if next == out.ids[i]:
                next_channel = out.channels[i]
                break
        channel = grpc.insecure_channel(next_channel)
        stub = pb2_grpc.ChordStub(channel)
        out = stub.SaveData(pb2.SaveDataMessage(key=key, text=text))
        return out.status, out.node_id


def remove(key):
    hash_value = zlib.adler32(key.encode())
    target_id = hash_value % (2**m)
    channel = grpc.insecure_channel(reg_ip + ":" + reg_port)
    stub = pb2_grpc.ChordStub(channel)
    out = stub.GetChordInfo(pb2.GetChordInfoMessage(message="hi"))
    if target_id in range(pred, id + 1) or len(out.ids) == 1:
        if data.get(key):
            del data[key]
            return "Removed", id
        return "Not Found", id
    elif target_id in range(id + 1, finger_table[0] + 1):
        channel = grpc.insecure_channel(reg_ip + ":" + reg_port)
        stub = pb2_grpc.ChordStub(channel)
        out = stub.GetChordInfo(pb2.GetChordInfoMessage(message="hi"))
        for i in range(len(out.ids)):
            if finger_table[0] == out.ids[i]:
                succ_channel = out.channels[i]
                break
        channel = grpc.insecure_channel(succ_channel)
        stub = pb2_grpc.ChordStub(channel)
        out = stub.RemoveData(pb2.RemoveDataMessage(key=key))
        return out.status, out.node_id
    else:
        next = -1
        next_channel = ""
        for i in range(len(finger_table) - 1):
            if target_id >= finger_table[i] and target_id < finger_table[i + 1]:
                next = finger_table[i]
                break
        channel = grpc.insecure_channel(reg_ip + ":" + reg_port)
        stub = pb2_grpc.ChordStub(channel)
        out = stub.GetChordInfo(pb2.GetChordInfoMessage(message="hi"))
        for i in range(len(out.ids)):
            if next == out.ids[i]:
                next_channel = out.channels[i]
                break
        channel = grpc.insecure_channel(next_channel)
        stub = pb2_grpc.ChordStub(channel)
        out = stub.RemoveData(pb2.RemoveDataMessage(key=key))
        return out.status, out.node_id


def find(key):
    hash_value = zlib.adler32(key.encode())
    target_id = hash_value % (2**m)
    channel = grpc.insecure_channel(reg_ip + ":" + reg_port)
    stub = pb2_grpc.ChordStub(channel)
    out = stub.GetChordInfo(pb2.GetChordInfoMessage(message="hi"))
    if target_id in range(pred, id + 1) or len(out.ids) == 1:
        if data.get(key):
            return "Found", id
        return "Not Found", id
    elif target_id in range(id + 1, finger_table[0] + 1):
        channel = grpc.insecure_channel(reg_ip + ":" + reg_port)
        stub = pb2_grpc.ChordStub(channel)
        out = stub.GetChordInfo(pb2.GetChordInfoMessage(message="hi"))
        for i in range(len(out.ids)):
            if finger_table[0] == out.ids[i]:
                succ_channel = out.channels[i]
                break
        channel = grpc.insecure_channel(succ_channel)
        stub = pb2_grpc.ChordStub(channel)
        out = stub.FindData(pb2.FindDataMessage(key=key))
        return out.status, out.node_id
    else:
        next = -1
        next_channel = ""
        for i in range(len(finger_table) - 1):
            if target_id >= finger_table[i] and target_id < finger_table[i + 1]:
                next = finger_table[i]
                break
        channel = grpc.insecure_channel(reg_ip + ":" + reg_port)
        stub = pb2_grpc.ChordStub(channel)
        out = stub.GetChordInfo(pb2.GetChordInfoMessage(message="hi"))
        for i in range(len(out.ids)):
            if next == out.ids[i]:
                next_channel = out.channels[i]
                break
        channel = grpc.insecure_channel(next_channel)
        stub = pb2_grpc.ChordStub(channel)
        out = stub.FindData(pb2.FindDataMessage(key=key))
        return out.status, out.node_id


def quit():
    dereg_status = False
    succ_channel = ""
    channel = grpc.insecure_channel(reg_ip + ":" + reg_port)
    stub = pb2_grpc.ChordStub(channel)
    out = stub.Deregister(pb2.DeregisterMessage(id=id))
    dereg_status = out.ack
    out = stub.GetChordInfo(pb2.GetChordInfoMessage(message="hi"))
    for i in range(len(out.ids)):
        if finger_table[0] == out.ids[i]:
            succ_channel = out.channels[i]
            break
    channel = grpc.insecure_channel(succ_channel)
    stub = pb2_grpc.ChordStub(channel)
    out = stub.NotifySucc(
        pb2.NotifySuccMessage(pred=pred, keys=data.keys(), values=data.values())
    )
    out = stub.NotifyPred(pb2.NotifyPredMessage(succ=succ))
    if dereg_status == "Node was deregisterd":
        print("Deleted, Shutting down")
        sys.exit(1)
    else:
        print("Error, Shutting down")
        sys.exit(1)


class NodeHandler(pb2_grpc.ChordServicer):
    def SaveData(self, request, context):
        key = request.key
        text = request.text
        status, node_id = save(key, text)
        reply = {"node_id": node_id, "status": status}
        return pb2.SaveDataResponse(**reply)

    def RemoveData(self, request, context):
        key = request.key
        status, node_id = remove(key)
        reply = {"node_id": node_id, "status": status}
        return pb2.RemoveDataResponse(**reply)

    def FindData(self, request, context):
        key = request.key
        status, node_id = find(key)
        reply = {"node_id": node_id, "status": status}
        return pb2.FindDataResponse(**reply)

    def GetFingerTable(self, request, context):
        channels = []
        channel = grpc.insecure_channel(reg_ip + ":" + reg_port)
        stub = pb2_grpc.ChordStub(channel)
        out = stub.GetChordInfo(pb2.GetChordInfoMessage(message="hi"))
        for node_id in finger_table:
            for i in range(len(out.ids)):
                if node_id == out.ids[i]:
                    channels.append(out.channels[i])
                    break
        reply = {"node_id": id, "ids": finger_table, "channels": channels}
        return pb2.GetFingerTableResponse(**reply)

    def NotifySucc(self, request, context):
        pred = request.pred
        for i in range(len(request.keys)):
            data[request.keys[i]] = request.values[i]
        reply = {"ack": "Notified"}
        return pb2.NotifySuccResponse(**reply)

    def NotifyPred(self, request, context):
        succ = request.succ
        reply = {"ack": "Notified"}
        return pb2.NotifyPredResponse(**reply)


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
        try:
            time.sleep(1)
            finger_table_response = stub.PopulateFingerTable(
                pb2.PopulateFingerTableMessage(id=id)
            )
            finger_table = finger_table_response.fingers
            pred = finger_table_response.pred
            succ = finger_table[0]
        except KeyboardInterrupt:
            quit()

    try:
        node.wait_for_termination()
    except KeyboardInterrupt:
        print("Shutting down")
