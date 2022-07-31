#!/usr/bin/env python3

from argparse import ArgumentDefaultsHelpFormatter
from sys import stderr
import can
from messages.MessageType import MessageType
from messages.SimMessage import SimMessage

with can.interface.Bus(bustype="socketcan", channel="vcan0", bitrate=500000) as bus:
    while True:
        print("cmd? [1-acc] [2-brake] [3-park]")
        cmd = int(input())
        if cmd == 1:
            # acc
            print("acc val?")
            val = int(input())
            msg = can.Message(
                arbitration_id=MessageType.AccelleratorPedalPosition,
                data=SimMessage(
                    MessageType.AccelleratorPedalPosition).pack(val),
            )
        elif cmd == 2:
            # brake
            print("brake val?")
            val = int(input())
            msg = can.Message(
                arbitration_id=MessageType.BrakePedalPosition,
                data=SimMessage(MessageType.BrakePedalPosition).pack(val),
            )
        elif cmd == 3:
            # brake
            print("parking brake?")
            val = bool(input())
            msg = can.Message(
                arbitration_id=MessageType.ParkingBrake,
                data=SimMessage(MessageType.ParkingBrake).pack(val),
            )
        else:
            continue
        try:
            bus.send(msg)
        except can.CanError:
            print(f"Message sending failure: [msg={msg}].", file=stderr)
