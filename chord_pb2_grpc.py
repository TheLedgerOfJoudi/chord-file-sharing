# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import chord_pb2 as chord__pb2


class ChordStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Register = channel.unary_unary(
                '/Chord/Register',
                request_serializer=chord__pb2.RegisterMessage.SerializeToString,
                response_deserializer=chord__pb2.RegisterResponse.FromString,
                )
        self.PopulateFingerTable = channel.unary_unary(
                '/Chord/PopulateFingerTable',
                request_serializer=chord__pb2.PopulateFingerTableMessage.SerializeToString,
                response_deserializer=chord__pb2.PopulateFingerTableResponse.FromString,
                )
        self.SaveData = channel.unary_unary(
                '/Chord/SaveData',
                request_serializer=chord__pb2.SaveDataMessage.SerializeToString,
                response_deserializer=chord__pb2.SaveDataResponse.FromString,
                )
        self.GetChordInfo = channel.unary_unary(
                '/Chord/GetChordInfo',
                request_serializer=chord__pb2.GetChordInfoMessage.SerializeToString,
                response_deserializer=chord__pb2.GetChordInfoResponse.FromString,
                )
        self.GetFingerTable = channel.unary_unary(
                '/Chord/GetFingerTable',
                request_serializer=chord__pb2.GetFingerTableMessage.SerializeToString,
                response_deserializer=chord__pb2.GetFingerTableResponse.FromString,
                )


class ChordServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Register(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def PopulateFingerTable(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SaveData(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetChordInfo(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetFingerTable(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ChordServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Register': grpc.unary_unary_rpc_method_handler(
                    servicer.Register,
                    request_deserializer=chord__pb2.RegisterMessage.FromString,
                    response_serializer=chord__pb2.RegisterResponse.SerializeToString,
            ),
            'PopulateFingerTable': grpc.unary_unary_rpc_method_handler(
                    servicer.PopulateFingerTable,
                    request_deserializer=chord__pb2.PopulateFingerTableMessage.FromString,
                    response_serializer=chord__pb2.PopulateFingerTableResponse.SerializeToString,
            ),
            'SaveData': grpc.unary_unary_rpc_method_handler(
                    servicer.SaveData,
                    request_deserializer=chord__pb2.SaveDataMessage.FromString,
                    response_serializer=chord__pb2.SaveDataResponse.SerializeToString,
            ),
            'GetChordInfo': grpc.unary_unary_rpc_method_handler(
                    servicer.GetChordInfo,
                    request_deserializer=chord__pb2.GetChordInfoMessage.FromString,
                    response_serializer=chord__pb2.GetChordInfoResponse.SerializeToString,
            ),
            'GetFingerTable': grpc.unary_unary_rpc_method_handler(
                    servicer.GetFingerTable,
                    request_deserializer=chord__pb2.GetFingerTableMessage.FromString,
                    response_serializer=chord__pb2.GetFingerTableResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Chord', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Chord(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Register(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Chord/Register',
            chord__pb2.RegisterMessage.SerializeToString,
            chord__pb2.RegisterResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def PopulateFingerTable(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Chord/PopulateFingerTable',
            chord__pb2.PopulateFingerTableMessage.SerializeToString,
            chord__pb2.PopulateFingerTableResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SaveData(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Chord/SaveData',
            chord__pb2.SaveDataMessage.SerializeToString,
            chord__pb2.SaveDataResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetChordInfo(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Chord/GetChordInfo',
            chord__pb2.GetChordInfoMessage.SerializeToString,
            chord__pb2.GetChordInfoResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetFingerTable(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Chord/GetFingerTable',
            chord__pb2.GetFingerTableMessage.SerializeToString,
            chord__pb2.GetFingerTableResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
