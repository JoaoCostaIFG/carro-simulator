#!/usr/bin/env python3

import asyncio
from typing import List, Set
from signal import SIGINT, SIGTERM
from sys import stderr
from time import monotonic

import can
from CarLogger import CarLogger
from carro.CarroState import CarroState

from gui.gui import GuiApp
from messages.MessageType import MessageType
from messages.SimMessage import SimMessage


def procMsg(canMsg: can.Message) -> None:
    global bus
    global gui

    try:
        id: MessageType = MessageType(canMsg.arbitration_id)
    except ValueError:
        print(f"Invalid arbitration ID: [id={canMsg.arbitration_id}].", file=stderr)
        return

    # TODO use the info
    try:
        if id == MessageType.Engine:
            data: bytearray = SimMessage(MessageType.Engine).unpack(canMsg.data)
            gui.root.onChangeAccel(data[0])
            gui.root.onChangeRpm(data[1])
        elif id == MessageType.BrakeSystem:
            data: bytearray = SimMessage(MessageType.BrakeSystem).unpack(canMsg.data)
            gui.root.onChangeDecel(data[0])
        elif id == MessageType.CarStatus:
            data: bytearray = SimMessage(MessageType.CarStatus).unpack(canMsg.data)
            gui.root.onChangeSpeed(data[0])
            gui.root.onChangeOperMode(CarroState(data[1]).name)
        else:
            # ignore unwanted messages
            pass
    except Exception as e:
        print(
            f"Invalid message data: [id={canMsg.arbitration_id}], [data={canMsg.data}].\n{e}",
            file=stderr,
        )
        return


def sendMsg(arbitrationId: int, msg: bytearray) -> None:
    global bus

    canMsg: can.Message = can.Message(
        arbitration_id=arbitrationId,
        data=msg,
    )
    try:
        # TODO deal with timeouts (this is a blocking task)
        bus.send(canMsg)
    except can.CanError as e:
        print(f"Message sending failure: [msg={msg}].\n{e}", file=stderr)


async def inputReports():
    global gui

    period: float = 0.1
    while True:
        startTime: float = monotonic()
        sendMsg(
            MessageType.AccelleratorPedalPosition,
            SimMessage(MessageType.AccelleratorPedalPosition).pack(int(gui.root.getAccelPos())),
        )
        sendMsg(
            MessageType.BrakePedalPosition,
            SimMessage(MessageType.BrakePedalPosition).pack(int(gui.root.getBrakePos())),
        )
        sendMsg(
            MessageType.ParkingBrake,
            SimMessage(MessageType.ParkingBrake).pack(int(gui.root.getHandBrakeValue())),
        )
        endTime: float = monotonic()

        sleepTime = max(0, period - (endTime - startTime))
        await asyncio.sleep(sleepTime)  # wait next period


async def busWatch():
    global bus

    canReader = can.AsyncBufferedReader()
    canLogger = CarLogger("gui-controller-log")
    listeners: List[can.notifier.MessageRecipient] = [
        canReader,
        canLogger,
    ]
    loop = asyncio.get_running_loop()
    notifier = can.Notifier(bus, listeners=listeners, loop=loop)

    while not asyncio.current_task().cancelled():
        canMsg: can.Message = await canReader.get_message()
        procMsg(canMsg)
    notifier.stop()


async def main():
    global bus

    loop = asyncio.get_running_loop()
    for signal in [SIGINT, SIGTERM]:
        loop.add_signal_handler(signal, asyncio.current_task().cancel)

    # spawn tasks
    tasks: Set[asyncio.Task] = set()

    # gui
    busWatchLoop = asyncio.create_task(busWatch())
    tasks.add(busWatchLoop)
    busWatchLoop.add_done_callback(tasks.discard)
    # input value communication
    reportLoop = asyncio.create_task(inputReports())
    tasks.add(reportLoop)
    reportLoop.add_done_callback(tasks.discard)

    try:
        await gui.async_run()
    except asyncio.CancelledError:
        # expected from the signal handler
        pass
    for task in tasks:
        task.cancel()


if __name__ == "__main__":
    gui: GuiApp = GuiApp()
    with can.interface.Bus(bustype="socketcan", channel="vcan0", bitrate=500000) as bus:
        asyncio.run(main())
