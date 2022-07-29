#!/usr/bin/env python

import asyncio
from signal import SIGINT, SIGTERM
from time import sleep, monotonic

import can

from carro.Carro import Carro
from messages.SimMessage import SimMessage
from messages.MessageTypes import MessageType


def send_one():
    """Sends a single message."""

    # this uses the default configuration (for example from the config file)
    # see https://python-can.readthedocs.io/en/stable/configuration.html
    with can.interface.Bus(bustype="socketcan", channel="vcan0", bitrate=500000) as bus:
        msg = can.Message(
            arbitration_id=0xC0FFEE, data=[0, 25, 0, 1, 3, 1, 4, 1], is_extended_id=True
        )

        try:
            bus.send(msg)
            print(f"Message sent on {bus.channel_info}")
        except can.CanError:
            print("Message NOT sent")


def recv_one():
    with can.interface.Bus(bustype="socketcan", channel="vcan0", bitrate=500000) as bus:
        try:
            msg = bus.recv()
            print(msg)
        except can.CanError:
            print("Message NOT recv")


async def carroUpdateLoop():
    global c

    # TODO remove
    c.setParkingBrakeState(False)
    c.setAccelerationPedal(100)

    period: float = 0.05
    prevTime: float = monotonic()
    while True:
        newTime: float = monotonic()
        c.update(newTime - prevTime)
        prevTime = newTime

        print(f" state: {c.state} - s: {c.getSpeed()}")

        await asyncio.sleep(period)  # wait next tick


async def carroEngineReport():
    global c

    period: float = 0.05
    while True:
        msg: SimMessage = SimMessage(MessageType.Engine).pack(c.getEngineAcc())
        # TODO send message
        await asyncio.sleep(period)  # wait next period


async def carroBrakeReport():
    global c

    period: float = 0.05
    while True:
        msg: SimMessage = SimMessage(MessageType.BrakeSystem).pack(c.getBrakeDec())
        # TODO send message
        await asyncio.sleep(period)  # wait next period


async def carroStatusReport():
    global c

    period: float = 0.05
    while True:
        msg: SimMessage = SimMessage(MessageType.CarStatus).pack(
            c.getSpeed(), c.getState().value
        )
        # TODO send message
        await asyncio.sleep(period)  # wait next period


async def main():
    for signal in [SIGINT, SIGTERM]:
        loop.add_signal_handler(signal, asyncio.current_task().cancel)

    # spawn tasks
    tasks = set()
    # carro update loop
    taskCUP = asyncio.create_task(carroUpdateLoop())
    tasks.add(taskCUP)
    taskCUP.add_done_callback(tasks.discard)
    # carro engine report
    taskCER = asyncio.create_task(carroEngineReport())
    tasks.add(taskCER)
    taskCER.add_done_callback(tasks.discard)
    # carro brake report
    taskCBR = asyncio.create_task(carroBrakeReport())
    tasks.add(taskCBR)
    taskCBR.add_done_callback(tasks.discard)
    # carro status report
    taskCSR = asyncio.create_task(carroStatusReport())
    tasks.add(taskCSR)
    taskCSR.add_done_callback(tasks.discard)

    try:
        await asyncio.gather(*tasks, return_exceptions=False)
    except asyncio.CancelledError:
        # expected from the signal handler
        pass


if __name__ == "__main__":
    c: Carro = Carro()

    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
