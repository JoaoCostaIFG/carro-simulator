from datetime import datetime
from can.listener import Listener
from can.message import Message

from os.path import join

from typing import Any

from messages.SimMessage import SimMessage

class CarLogger(Listener):

    def __init__(self, filename: str, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        full_path = join('/tmp/', f'{datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}-{filename}.txt')
        self.out = open(full_path, "w")

    def on_message_received(self, message: Message) -> None:
        sm = SimMessage(message.arbitration_id)
        params = sm.unpack(message.data)

        if self.out.closed:
            raise Exception('Cannot log to a closed file descriptor')

        self.out.write(f'{sm.getType().name}\t\t---- {*params,}\n')


    def cleanup(self):
        if not self.out.closed:
            self.out.close()
