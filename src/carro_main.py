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
    c.parkingBrake = False
    c.engine.pedal = 100

    period: float = 0.05
    prevTime: float = monotonic()
    while True:
        newTime: float = monotonic()
        c.update(newTime - prevTime)
        prevTime = newTime

        print(f" state: {c.state} - s: {c.speed}")

        await asyncio.sleep(period)  # wait next tick


async def carroEngineReport():
    global c

    period: float = 0.05
    while True:
        msg: SimMessage = SimMessage(MessageType.Engine).pack(c.engine.acceleration)
        c.sendMsg(msg)
        await asyncio.sleep(period)  # wait next period


async def carroBrakeReport():
    global c

    period: float = 0.05
    while True:
        msg: SimMessage = SimMessage(MessageType.BrakeSystem).pack(c.brake.deceleration)
        c.sendMsg(msg)
        await asyncio.sleep(period)  # wait next period


async def carroStatusReport():
    global c

    period: float = 0.05
    while True:
        msg: SimMessage = SimMessage(MessageType.CarStatus).pack(c.speed, c.state.value)
        c.sendMsg(msg)
        await asyncio.sleep(period)  # wait next period


async def carroParkingBrakeReport():
    global c

    period: float = 0.1
    while True:
        msg: SimMessage = SimMessage(MessageType.ParkingBrake).pack(c.parkingBrake)
        c.sendMsg(msg)
        await asyncio.sleep(period)  # wait next period


async def carroAccPedalReport():
    global c

    period: float = 0.1
    while True:
        msg: SimMessage = SimMessage(MessageType.AccelleratorPedalPosition).pack(
            c.engine.pedal
        )
        c.sendMsg(msg)
        await asyncio.sleep(period)  # wait next period


async def carroBrakePedalReport():
    global c

    period: float = 0.1
    while True:
        msg: SimMessage = SimMessage(MessageType.BrakePedalPosition).pack(c.brake.pedal)
        c.sendMsg(msg)
        await asyncio.sleep(period)  # wait next period


async def main():
    for signal in [SIGINT, SIGTERM]:
        loop.add_signal_handler(signal, asyncio.current_task().cancel)

    # spawn tasks
    tasks = set()

    def addTask(taskFunc):
        task = asyncio.create_task(taskFunc())
        tasks.add(task)
        task.add_done_callback(tasks.discard)

    addTask(carroUpdateLoop)
    addTask(carroEngineReport)
    addTask(carroBrakeReport)
    addTask(carroStatusReport)
    addTask(carroParkingBrakeReport)
    addTask(carroAccPedalReport)
    addTask(carroBrakePedalReport)

    try:
        await asyncio.gather(*tasks, return_exceptions=False)
    except asyncio.CancelledError:
        # expected from the signal handler
        pass


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    with can.interface.Bus(bustype="socketcan", channel="vcan0", bitrate=500000) as bus:
        c: Carro = Carro(0x123, bus)
        loop.run_until_complete(main())
    loop.close()
