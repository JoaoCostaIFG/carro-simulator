#!/usr/bin/env python

import can


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


if __name__ == "__main__":
    send_one()
    # recv_one()
