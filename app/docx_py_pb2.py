# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: docx_py.proto
# Protobuf Python Version: 5.27.2
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    27,
    2,
    '',
    'docx_py.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rdocx_py.proto\x1a\x1cgoogle/protobuf/struct.proto\"e\n\x0f\x44ocumentRequest\x12\x13\n\x0btemplate_id\x18\x01 \x01(\x04\x12\x13\n\x0b\x63lient_uuid\x18\x02 \x01(\t\x12(\n\x07\x63ontext\x18\x03 \x01(\x0b\x32\x17.google.protobuf.Struct\"$\n\x10\x44ocumentResponse\x12\x10\n\x08\x64ocument\x18\x01 \x01(\x0c\x32\x41\n\x06\x44ocxPy\x12\x37\n\x10GenerateDocument\x12\x10.DocumentRequest\x1a\x11.DocumentResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'docx_py_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_DOCUMENTREQUEST']._serialized_start=47
  _globals['_DOCUMENTREQUEST']._serialized_end=148
  _globals['_DOCUMENTRESPONSE']._serialized_start=150
  _globals['_DOCUMENTRESPONSE']._serialized_end=186
  _globals['_DOCXPY']._serialized_start=188
  _globals['_DOCXPY']._serialized_end=253
# @@protoc_insertion_point(module_scope)