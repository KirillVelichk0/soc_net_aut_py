# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: AuthServ.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0e\x41uthServ.proto\x12\x03\x43\x41S\"4\n\x11RegistrationInput\x12\r\n\x05\x65mail\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\"8\n\x1dRegistrationVerificationInput\x12\x17\n\x0frandomDataToken\x18\x01 \x01(\t\"\x1d\n\tAuthInput\x12\x10\n\x08jwtToken\x18\x01 \x01(\t\"4\n\x11PasswordAuthInput\x12\r\n\x05\x65mail\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\"2\n\x12RegistrationResult\x12\x0e\n\x06\x61nswer\x18\x01 \x01(\t\x12\x0c\n\x04isOk\x18\x02 \x01(\x08\"=\n\x1eRegistrationVerificationResult\x12\r\n\x05token\x18\x01 \x01(\t\x12\x0c\n\x04isOk\x18\x02 \x01(\x08\"/\n\nAuthResult\x12\x0e\n\x06userId\x18\x01 \x01(\x03\x12\x11\n\tnextToken\x18\x02 \x01(\t\"?\n\x12PasswordAuthResult\x12\x10\n\x08jwtToken\x18\x01 \x01(\t\x12\x17\n\x0fresponceMessage\x18\x02 \x01(\t2\xa7\x02\n\x14\x41uthAndRegistService\x12=\n\nTryRegistr\x12\x16.CAS.RegistrationInput\x1a\x17.CAS.RegistrationResult\x12Z\n\x0fTryVerifRegistr\x12\".CAS.RegistrationVerificationInput\x1a#.CAS.RegistrationVerificationResult\x12/\n\x0c\x41uthenticate\x12\x0e.CAS.AuthInput\x1a\x0f.CAS.AuthResult\x12\x43\n\x10\x41uthFromPassword\x12\x16.CAS.PasswordAuthInput\x1a\x17.CAS.PasswordAuthResultb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'AuthServ_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _REGISTRATIONINPUT._serialized_start=23
  _REGISTRATIONINPUT._serialized_end=75
  _REGISTRATIONVERIFICATIONINPUT._serialized_start=77
  _REGISTRATIONVERIFICATIONINPUT._serialized_end=133
  _AUTHINPUT._serialized_start=135
  _AUTHINPUT._serialized_end=164
  _PASSWORDAUTHINPUT._serialized_start=166
  _PASSWORDAUTHINPUT._serialized_end=218
  _REGISTRATIONRESULT._serialized_start=220
  _REGISTRATIONRESULT._serialized_end=270
  _REGISTRATIONVERIFICATIONRESULT._serialized_start=272
  _REGISTRATIONVERIFICATIONRESULT._serialized_end=333
  _AUTHRESULT._serialized_start=335
  _AUTHRESULT._serialized_end=382
  _PASSWORDAUTHRESULT._serialized_start=384
  _PASSWORDAUTHRESULT._serialized_end=447
  _AUTHANDREGISTSERVICE._serialized_start=450
  _AUTHANDREGISTSERVICE._serialized_end=745
# @@protoc_insertion_point(module_scope)
