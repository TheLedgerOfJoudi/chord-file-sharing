import grpc
import chord_pb2 as pb2
import chord_pb2_grpc as pb2_grpc
import sys

registry_channel = ""
node_channel = ""
con_registry = False
con_node = False

if __name__ == "__main__":
    while True:
        try:
            inp = input("> ")
            splits = inp.split(" ")
            if splits[0] == "connect":
                if con_registry:
                    node_channel = splits[1]
                    print("Connected To Node")
                    con_node = True
                else:
                    registry_channel = splits[1]
                    print("Connected To Registry")
                    con_registry = True
            elif splits[0] == "get_info":
                channel = ""
                if con_node:
                    channel = grpc.insecure_channel(node_channel)
                    stub = pb2_grpc.ChordStub(channel)
                    print(node_channel)
                    out = stub.GetFingerTable(pb2.GetFingerTableMessage(message="hi"))
                    print("Node id: " + str(out.node_id))
                    for i in range(len(out.ids)):
                        print(str(out.ids[i]) + ":  " + out.channels[i])
                else:
                    channel = grpc.insecure_channel(registry_channel)
                    stub = pb2_grpc.ChordStub(channel)
                    out = stub.GetChordInfo(pb2.GetChordInfoMessage(message="hi"))
                    for i in range(len(out.ids)):
                        print(str(out.ids[i]) + ":  " + out.channels[i])

        except KeyboardInterrupt:
            sys.exit(0)
