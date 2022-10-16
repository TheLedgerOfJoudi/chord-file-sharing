from asyncio.proactor_events import constants
import chord_pb2_grpc as pb2_grpc
import chord_pb2 as pb2
import grpc
from concurrent import futures
import sys
import random

reg_ip, reg_port = sys.argv[1].split(":")

m = int(sys.argv[2])
chord_info = {}

finger_table = {}
for i in range(2**m):
    finger_table[i] = []


def register(ipaddr, port):
    if len(chord_info) == 2**m:
        return -1, "No more slots"
    random.seed(0)
    while True:
        id = random.randrange(2**m)
        if id not in chord_info:
            break
    chord_info[id] = ipaddr + ":" + str(port)
    return id, m


def deregister(id):
    if chord_info.get(id):
        del chord_info[id]
        return "Node was deregisterd"
    else:
        return "No such node"


def populate_finger_table(id):
    def succ_find(target):
        nums = sorted(chord_info.keys())
        for value in nums:
            if value >= target:
                return value
        return nums[0]

    def pred_find(target):
        nums = sorted(chord_info.keys())
        nums.reverse()
        for value in nums:
            if value < target:
                return value
        return nums[len(nums) - 1]

    if chord_info.get(id):
        temp_fingers = []
        for i in range(1, m + 1):
            succ = succ_find((id + (2 ** (i - 1))) % (2**m))
            if succ is not None:
                temp_fingers.append(succ)
            else:
                finger_table[id].append(-1)
        finger_table[id] = temp_fingers
        return finger_table, pred_find(id)
    else:
        return False, "No such node"


def get_chord_info():
    return chord_info


class RegistryHandler(pb2_grpc.ChordServicer):
    def Register(self, request, context):
        ipaddr, port = request.ipaddr, request.port
        id, m = register(ipaddr, port)
        reply = {"id": id, "m": m}
        return pb2.RegisterResponse(**reply)

    def Deregister(self, request, context):
        id = request.id
        ack = deregister(id)
        reply = {"ack": ack}
        return pb2.DeregisterResponse(**reply)

    def PopulateFingerTable(self, request, context):
        id = request.id
        fingers, pred = populate_finger_table(id)
        reply = {"fingers": fingers[id], "pred": pred}
        return pb2.PopulateFingerTableResponse(**reply)

    def GetChordInfo(self, request, context):
        chord = get_chord_info()
        reply = {"ids": chord.keys(), "channels": chord.values()}
        return pb2.GetChordInfoResponse(**reply)


if __name__ == "__main__":
    reg = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_ChordServicer_to_server(RegistryHandler(), reg)
    reg.add_insecure_port("127.0.0.1:" + str(reg_port))
    reg.start()
    try:
        reg.wait_for_termination()
    except KeyboardInterrupt:
        print("Shutting down")
