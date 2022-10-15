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
        return True, "Node was deleted"
    else:
        return False, "No such node"


def populate_finger_table(id):
    finger_table = {}

    def succ_find(target):
        end = -1
        low = 0
        nums = sorted(chord_info.keys())
        high = len(chord_info) - 1
        while low < high:
            mid = low + (high - low) / 2
            if nums[mid] <= target:
                low = mid + 1
                if nums[mid] == target:
                    end = mid
                if low < len(nums) and nums[low] == target:
                    end = low
            else:
                high = mid

            return end

    def pred_find(target):
        start = -1
        low = 0
        nums = sorted(chord_info.keys())
        high = len(nums) - 1
        while low < high:
            mid = low + (high - low) / 2
            if nums[mid] >= target:
                high = mid
                if nums[mid] == target:
                    start = mid
            else:
                low = mid + 1
        if nums[low] == target:
            start = low
        return start

    if chord_info.get(id):
        for i in range(1, m + 1):
            finger_table[id].append(succ_find(id + 2 ** (i - 1) % 2**m))
        return finger_table, pred_find(id)
    else:
        return False, "No such node"


def get_chord_info():
    return chord_info


class RegistryHandler(pb2_grpc.ChordServicer):
    def Register(self, request, context):
        ipaddr, port = request.ipaddr, request.port
        id, m = register(ipaddr, port)
        print(id,m)
        reply = {"id": id, "m": m}
        return pb2.RegisterResponse(**reply)


if __name__ == "__main__":
    reg = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_ChordServicer_to_server(RegistryHandler(), reg)
    reg.add_insecure_port("127.0.0.1:" + str(reg_port))
    reg.start()
    try:
        reg.wait_for_termination()
    except KeyboardInterrupt:
        print("Shutting down")
