# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: io_service.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x10io_service.proto\x12\x05\x61iswa\"\x1e\n\x0bPingRequest\x12\x0f\n\x07message\x18\x01 \x01(\t\"\x1c\n\tPingReply\x12\x0f\n\x07message\x18\x01 \x01(\t2;\n\tIOService\x12.\n\x04Ping\x12\x12.aiswa.PingRequest\x1a\x10.aiswa.PingReply\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'io_service_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_PINGREQUEST']._serialized_start=27
  _globals['_PINGREQUEST']._serialized_end=57
  _globals['_PINGREPLY']._serialized_start=59
  _globals['_PINGREPLY']._serialized_end=87
  _globals['_IOSERVICE']._serialized_start=89
  _globals['_IOSERVICE']._serialized_end=148
# @@protoc_insertion_point(module_scope)
