#!/usr/bin/env python

import asyncio
from struct import Struct
from typing import List, Set
from signal import SIGINT, SIGTERM
from time import monotonic
from sys import stderr

import can

from carro.Carro import Carro
from messages.simMessage import SimMessage
from messages.messageTypes import MessageType


def sendMsg(arbitrationId: int, msg: bytearray) -> None:
    global bus

    # TODO logging
    canMsg: can.Message = can.Message(
        arbitration_id=arbitrationId,
        data=msg,
    )
    try:
        # TODO deal with timeouts
        bus.send(canMsg)
    except can.CanError as e:
        print(f"Message sending failure: [msg={msg}].\n{e}", file=stderr)


def procMsg(canMsg: can.Message) -> None:
    global bus
    global c

    try:
        id: MessageType = MessageType(canMsg.arbitration_id)
    except ValueError:
        print(f"Invalid arbitration ID: [id={canMsg.arbitration_id}].", file=stderr)
        return

    try:
        if id == MessageType.AccelleratorPedalPosition:
            data: bytearray = SimMessage(MessageType.AccelleratorPedalPosition).unpack(
                canMsg.data
            )
            c.engine.pedal = data[0]
        elif id == MessageType.BrakePedalPosition:
            data: bytearray = SimMessage(MessageType.BrakePedalPosition).unpack(
                canMsg.data
            )
            c.brake.pedal = data[0]
        elif id == MessageType.ParkingBrake:
            data: bytearray = SimMessage(MessageType.ParkingBrake).unpack(canMsg.data)
            c.parkingBrake = data[0]
        else:
            # ignore unwanted messages
            pass
    except Struct.error:
        print(
            f"Invalid message data: [id={canMsg.arbitration_id}], [data={canMsg.data}].",
            file=stderr,
        )
        return


async def carroReports():
    global c

    period: float = 0.05
    while True:
        startTime: float = monotonic()
        sendMsg(
            MessageType.Engine,
            SimMessage(MessageType.Engine).pack(c.engine.acceleration),
        )
        sendMsg(
            MessageType.BrakeSystem,
            SimMessage(MessageType.BrakeSystem).pack(c.brake.deceleration),
        )
        sendMsg(
            MessageType.CarStatus,
            SimMessage(MessageType.CarStatus).pack(c.speed, c.state.value),
        )
        endTime: float = monotonic()

        sleepTime = max(0, period - (endTime - startTime))
        await asyncio.sleep(sleepTime)  # wait next period


async def carroUpdateLoop():
    global c

    period: float = 0.025
    prevTime: float = monotonic()
    while True:
        startTime: float = monotonic()
        c.update(startTime - prevTime)
        prevTime = startTime

        print(f" state: {c.state} - s: {c.speed}")

        await asyncio.sleep(period)  # wait next tick


async def main():
    global bus

    loop = asyncio.get_running_loop()
    for signal in [SIGINT, SIGTERM]:
        loop.add_signal_handler(signal, asyncio.current_task().cancel)

    # spawn tasks
    tasks: Set[asyncio.Task] = set()

    # carro update loop
    updateLoop = asyncio.create_task(carroUpdateLoop())
    tasks.add(updateLoop)
    updateLoop.add_done_callback(tasks.discard)

    # reports schedule
    reports = asyncio.create_task(carroReports())
    tasks.add(reports)
    reports.add_done_callback(tasks.discard)

    canReader = can.AsyncBufferedReader()
    canLogger = can.Logger("logfile.asc")
    listeners: List[can.notifier.MessageRecipient] = [
        canReader,
        canLogger,
    ]
    notifier = can.Notifier(bus, listeners=listeners, loop=loop)

    try:
        while not asyncio.current_task().cancelled():
            canMsg: can.Message = await canReader.get_message()
            procMsg(canMsg)
    except asyncio.CancelledError:
        # expected from the signal handler
        for task in tasks:
            task.cancel()
    notifier.stop()


if __name__ == "__main__":
    c: Carro = Carro()
    with can.interface.Bus(bustype="socketcan", channel="vcan0", bitrate=500000) as bus:
        asyncio.run(main())
