# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import runhouse.servers.grpc.unary_pb2 as unary__pb2


class UnaryStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.RunModule = channel.unary_unary(
            "/unary.Unary/RunModule",
            request_serializer=unary__pb2.Message.SerializeToString,
            response_deserializer=unary__pb2.MessageResponse.FromString,
        )
        self.InstallPackages = channel.unary_unary(
            "/unary.Unary/InstallPackages",
            request_serializer=unary__pb2.Message.SerializeToString,
            response_deserializer=unary__pb2.MessageResponse.FromString,
        )
        self.ClearPins = channel.unary_unary(
            "/unary.Unary/ClearPins",
            request_serializer=unary__pb2.Message.SerializeToString,
            response_deserializer=unary__pb2.MessageResponse.FromString,
        )
        self.CancelRun = channel.unary_unary(
            "/unary.Unary/CancelRun",
            request_serializer=unary__pb2.Message.SerializeToString,
            response_deserializer=unary__pb2.MessageResponse.FromString,
        )
        self.ListKeys = channel.unary_unary(
            "/unary.Unary/ListKeys",
            request_serializer=unary__pb2.Message.SerializeToString,
            response_deserializer=unary__pb2.MessageResponse.FromString,
        )
        self.PutObject = channel.unary_unary(
            "/unary.Unary/PutObject",
            request_serializer=unary__pb2.Message.SerializeToString,
            response_deserializer=unary__pb2.MessageResponse.FromString,
        )
        self.AddSecrets = channel.unary_unary(
            "/unary.Unary/AddSecrets",
            request_serializer=unary__pb2.Message.SerializeToString,
            response_deserializer=unary__pb2.MessageResponse.FromString,
        )
        self.GetRunObject = channel.unary_unary(
            "/unary.Unary/GetRunObject",
            request_serializer=unary__pb2.Message.SerializeToString,
            response_deserializer=unary__pb2.MessageResponse.FromString,
        )
        self.GetObject = channel.unary_stream(
            "/unary.Unary/GetObject",
            request_serializer=unary__pb2.Message.SerializeToString,
            response_deserializer=unary__pb2.MessageResponse.FromString,
        )


class UnaryServicer(object):
    """Missing associated documentation comment in .proto file."""

    def RunModule(self, request, context):
        """A simple RPC.

        Obtains the MessageResponse at a given position.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def InstallPackages(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def ClearPins(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def CancelRun(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def ListKeys(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def PutObject(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def AddSecrets(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def GetRunObject(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def GetObject(self, request, context):
        """streaming RPC"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_UnaryServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "RunModule": grpc.unary_unary_rpc_method_handler(
            servicer.RunModule,
            request_deserializer=unary__pb2.Message.FromString,
            response_serializer=unary__pb2.MessageResponse.SerializeToString,
        ),
        "InstallPackages": grpc.unary_unary_rpc_method_handler(
            servicer.InstallPackages,
            request_deserializer=unary__pb2.Message.FromString,
            response_serializer=unary__pb2.MessageResponse.SerializeToString,
        ),
        "ClearPins": grpc.unary_unary_rpc_method_handler(
            servicer.ClearPins,
            request_deserializer=unary__pb2.Message.FromString,
            response_serializer=unary__pb2.MessageResponse.SerializeToString,
        ),
        "CancelRun": grpc.unary_unary_rpc_method_handler(
            servicer.CancelRun,
            request_deserializer=unary__pb2.Message.FromString,
            response_serializer=unary__pb2.MessageResponse.SerializeToString,
        ),
        "ListKeys": grpc.unary_unary_rpc_method_handler(
            servicer.ListKeys,
            request_deserializer=unary__pb2.Message.FromString,
            response_serializer=unary__pb2.MessageResponse.SerializeToString,
        ),
        "PutObject": grpc.unary_unary_rpc_method_handler(
            servicer.PutObject,
            request_deserializer=unary__pb2.Message.FromString,
            response_serializer=unary__pb2.MessageResponse.SerializeToString,
        ),
        "AddSecrets": grpc.unary_unary_rpc_method_handler(
            servicer.AddSecrets,
            request_deserializer=unary__pb2.Message.FromString,
            response_serializer=unary__pb2.MessageResponse.SerializeToString,
        ),
        "GetRunObject": grpc.unary_unary_rpc_method_handler(
            servicer.GetRunObject,
            request_deserializer=unary__pb2.Message.FromString,
            response_serializer=unary__pb2.MessageResponse.SerializeToString,
        ),
        "GetObject": grpc.unary_stream_rpc_method_handler(
            servicer.GetObject,
            request_deserializer=unary__pb2.Message.FromString,
            response_serializer=unary__pb2.MessageResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        "unary.Unary", rpc_method_handlers
    )
    server.add_generic_rpc_handlers((generic_handler,))


# This class is part of an EXPERIMENTAL API.
class Unary(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def RunModule(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/unary.Unary/RunModule",
            unary__pb2.Message.SerializeToString,
            unary__pb2.MessageResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def InstallPackages(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/unary.Unary/InstallPackages",
            unary__pb2.Message.SerializeToString,
            unary__pb2.MessageResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def ClearPins(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/unary.Unary/ClearPins",
            unary__pb2.Message.SerializeToString,
            unary__pb2.MessageResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def CancelRun(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/unary.Unary/CancelRun",
            unary__pb2.Message.SerializeToString,
            unary__pb2.MessageResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def ListKeys(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/unary.Unary/ListKeys",
            unary__pb2.Message.SerializeToString,
            unary__pb2.MessageResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def PutObject(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/unary.Unary/PutObject",
            unary__pb2.Message.SerializeToString,
            unary__pb2.MessageResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def AddSecrets(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/unary.Unary/AddSecrets",
            unary__pb2.Message.SerializeToString,
            unary__pb2.MessageResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def GetRunObject(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/unary.Unary/GetRunObject",
            unary__pb2.Message.SerializeToString,
            unary__pb2.MessageResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def GetObject(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_stream(
            request,
            target,
            "/unary.Unary/GetObject",
            unary__pb2.Message.SerializeToString,
            unary__pb2.MessageResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )
