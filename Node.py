import chord_pb2_grpc as pb2_grpc
import chord_pb2 as pb2
import grpc
from concurrent import futures
import sys
import random
import zlib

reg_ip, reg_port = sys.argv[1].split(":")
node_ip, node_port = sys.argv[2].split(":")

data = ""
finger_table = {}
m = -1
id = -1


def get_finger_table():
    return finger_table


def save(key, test):
    hash_value = zlib.adler32(key.encode())
    target_id = hash_value % 2**m


def remove(key):
    return


def find(key):
    return key


def quit():
    return


if __name__ == "__main__":
    channel = grpc.insecure_channel(reg_ip + ":" + reg_port)
    stub = pb2_grpc.ChordStub(channel)
    out = stub.Register(pb2.RegisterMessage(ipaddr=node_ip, port=int(node_port)))
    id, m = out.id, out.m
