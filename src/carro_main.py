#!/usr/bin/env python

import asyncio
from signal import SIGINT, SIGTERM
from time import sleep, monotonic
from sys import stderr

import can

from carro.Carro import Carro
from messages.SimMessage import SimMessage
from messages.MessageTypes import MessageType


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
        c.sendMsg(msg)
        await asyncio.sleep(period)  # wait next period


async def carroBrakeReport():
    global c

    period: float = 0.05
    while True:
        msg: SimMessage = SimMessage(MessageType.BrakeSystem).pack(c.getBrakeDec())
        c.sendMsg(msg)
        await asyncio.sleep(period)  # wait next period


async def carroStatusReport():
    global c

    period: float = 0.05
    while True:
        msg: SimMessage = SimMessage(MessageType.CarStatus).pack(
            c.getSpeed(), c.getState().value
        )
        c.sendMsg(msg)
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
    c: Carro = Carro(0x123)
    loop = asyncio.new_event_loop()
    with can.interface.Bus(bustype="socketcan", channel="vcan0", bitrate=500000) as bus:
        loop.run_until_complete(main())
    loop.close()
