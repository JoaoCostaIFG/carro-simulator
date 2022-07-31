#!/usr/bin/env python3

import asyncio
from typing import List, Set
from struct import Struct
from signal import SIGINT, SIGTERM
from sys import stderr
from time import monotonic

import can

from gui.gui import GuiApp
from messages.MessageType import MessageType
from messages.SimMessage import SimMessage


def procMsg(canMsg: can.Message) -> None:
    global bus

    try:
        id: MessageType = MessageType(canMsg.arbitration_id)
    except ValueError:
        print(f"Invalid arbitration ID: [id={canMsg.arbitration_id}].", file=stderr)
        return

    # TODO use the info
    try:
        if id == MessageType.Engine:
            data: bytearray = SimMessage(MessageType.Engine).unpack(canMsg.data)
        elif id == MessageType.BrakeSystem:
            data: bytearray = SimMessage(MessageType.BrakeSystem).unpack(canMsg.data)
        elif id == MessageType.CarStatus:
            data: bytearray = SimMessage(MessageType.CarStatus).unpack(canMsg.data)
        else:
            # ignore unwanted messages
            pass
    except Struct.error:
        print(
            f"Invalid message data: [id={canMsg.arbitration_id}], [data={canMsg.data}].",
            file=stderr,
        )
        return


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


async def inputReports():
    global gui

    period: float = 0.1
    while True:
        startTime: float = monotonic()
        print("AAAAAAAAAAAAAAAAAA")
        sendMsg(
            MessageType.AccelleratorPedalPosition,
            SimMessage(MessageType.AccelleratorPedalPosition).pack(
                gui.accelerationPedal.position
            ),
        )
        sendMsg(
            MessageType.BrakePedalPosition,
            SimMessage(MessageType.BrakePedalPosition).pack(gui.brakePedal.position),
        )
        sendMsg(
            MessageType.ParkingBrake,
            SimMessage(MessageType.ParkingBrake).pack(gui.handBrake.active),
        )
        endTime: float = monotonic()

        sleepTime = max(0, period - (endTime - startTime))
        await asyncio.sleep(sleepTime)  # wait next period


async def main():
    global bus
    global gui

    asyncio.run(gui.async_run())

    loop = asyncio.get_running_loop()
    for signal in [SIGINT, SIGTERM]:
        loop.add_signal_handler(signal, asyncio.current_task().cancel)

    # spawn tasks
    tasks: Set[asyncio.Task] = set()

    # gui
    # guiRun = asyncio.create_task(gui.async_run())
    # tasks.add(guiRun)
    # guiRun.add_done_callback(tasks.discard)
    # input value communication
    reportLoop = asyncio.create_task(inputReports())
    tasks.add(reportLoop)
    reportLoop.add_done_callback(tasks.discard)

    canReader = can.AsyncBufferedReader()
    canLogger = can.Logger("controller.asc")
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
    gui: GuiApp = GuiApp()
    with can.interface.Bus(bustype="socketcan", channel="vcan0", bitrate=500000) as bus:
        asyncio.run(main())
