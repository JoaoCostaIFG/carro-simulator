from enum import IntEnum

class MessageType(IntEnum):
    AccelleratorPedalPosition = 0x01
    BrakePedalPosition = 0x02
    Engine = 0x03
    BrakeSystem = 0x04
    ParkingBrake = 0x05
    CarStatus = 0x06

_messageFormats = {
    MessageType.AccelleratorPedalPosition.value: 's',
    MessageType.BrakePedalPosition.value: 's',
    MessageType.Engine.value: 'f',
    MessageType.BrakeSystem.value: 'f',
    MessageType.ParkingBrake.value: '?',
    MessageType.CarStatus.value: 'fs',    
}
