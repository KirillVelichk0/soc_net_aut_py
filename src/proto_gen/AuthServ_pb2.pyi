from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class AuthInput(_message.Message):
    __slots__ = ["jwtToken"]
    JWTTOKEN_FIELD_NUMBER: _ClassVar[int]
    jwtToken: str
    def __init__(self, jwtToken: _Optional[str] = ...) -> None: ...

class AuthResult(_message.Message):
    __slots__ = ["nextToken", "userId"]
    NEXTTOKEN_FIELD_NUMBER: _ClassVar[int]
    USERID_FIELD_NUMBER: _ClassVar[int]
    nextToken: str
    userId: int
    def __init__(self, userId: _Optional[int] = ..., nextToken: _Optional[str] = ...) -> None: ...

class PasswordAuthInput(_message.Message):
    __slots__ = ["email", "password"]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    email: str
    password: str
    def __init__(self, email: _Optional[str] = ..., password: _Optional[str] = ...) -> None: ...

class PasswordAuthResult(_message.Message):
    __slots__ = ["jwtToken", "user_id"]
    JWTTOKEN_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    jwtToken: str
    user_id: int
    def __init__(self, jwtToken: _Optional[str] = ..., user_id: _Optional[int] = ...) -> None: ...

class RegistrationInput(_message.Message):
    __slots__ = ["email", "password"]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    email: str
    password: str
    def __init__(self, email: _Optional[str] = ..., password: _Optional[str] = ...) -> None: ...

class RegistrationResult(_message.Message):
    __slots__ = ["answer", "isOk"]
    ANSWER_FIELD_NUMBER: _ClassVar[int]
    ISOK_FIELD_NUMBER: _ClassVar[int]
    answer: str
    isOk: bool
    def __init__(self, answer: _Optional[str] = ..., isOk: bool = ...) -> None: ...

class RegistrationVerificationInput(_message.Message):
    __slots__ = ["randomDataToken"]
    RANDOMDATATOKEN_FIELD_NUMBER: _ClassVar[int]
    randomDataToken: str
    def __init__(self, randomDataToken: _Optional[str] = ...) -> None: ...

class RegistrationVerificationResult(_message.Message):
    __slots__ = ["response_message"]
    RESPONSE_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    response_message: str
    def __init__(self, response_message: _Optional[str] = ...) -> None: ...
