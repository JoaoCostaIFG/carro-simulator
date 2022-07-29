from email import message
import struct
from typing import List
from messages.MessageTypes import _messageFormats, MessageType


class SimMessage:
    def __init__(self, messageType: int) -> None:
        self.type: MessageType = messageType
        self.format = _messageFormats.get(messageType)

    def unpack(self, payload) -> List:
        return struct.unpack(self.format, payload)

    def pack(self, *args) -> bytearray:
        return struct.pack(self.format, *args)

    def getType(self) -> MessageType:
        return self.type
