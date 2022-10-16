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
        return True, "Node was deleted"
    else:
        return False, "No such node"


def populate_finger_table(id):

    def succ_find(target):
        # end = -1
        # low = 0
        # end = 0
        # nums = sorted(chord_info.keys())
        # if (target>nums[len(nums)-1]):
        #     return nums[0]
        # high = len(chord_info) - 1
        # print(target)
        # while low < high:
        #     mid = low + (high - low) // 2
        #     if nums[mid] <= target:
        #         low = mid + 1
        #         if nums[mid] == target:
        #             end = mid
        #         if low < len(nums) and nums[low] == target:
        #             end = low
        #     else:
        #         high = mid

        # return nums[end]
        nums = sorted(chord_info.keys())
        print("nums:")
        print(nums)
        for value in nums:
            if value>=target:
                print("target | successor: ", target, value)
                return value
        print("target | successor: ", target, nums[0])
        return nums[0]  


    def pred_find(target):
        # start = -1
        # low = 0
        # nums = sorted(chord_info.keys())
        # if (target<nums[0]):
        #     return nums[len(nums)-1]
        # high = len(nums) - 1
        # start = 0
        # while low < high:
        #     mid = low + (high - low) // 2
        #     if nums[mid] >= target:
        #         high = mid
        #         if nums[mid] == target:
        #             start = mid
        #     else:
        #         low = mid + 1
        # if nums[low] == target:
        #     start = low
        # return nums[start]
        nums = sorted(chord_info.keys())
        nums.reverse()
        print("nums:")
        print(nums)
        for value in nums:
            if value<target:
                print("target | predecessor: ", target, value)
                return value
        print("target | predecessor: ", target, nums[len(nums)-1])
        return nums[len(nums)-1]

    
    if chord_info.get(id):
        temp_fingers = []
        for i in range(1, m + 1):
            succ = succ_find((id + (2 ** (i - 1))) % (2**m))
            print(i, succ)
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
        print(id,m)
        reply = {"id": id, "m": m}
        return pb2.RegisterResponse(**reply)

    def PopulateFingerTable(self, request, context):
        id = request.id
        
        fingers, pred = populate_finger_table(id)
        print(pred)
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
