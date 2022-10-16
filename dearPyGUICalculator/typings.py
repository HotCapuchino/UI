from enum import Enum


class PayloadType(Enum):
    NUMBER = 1,
    OPERATION = 2

class ButtonPayload:
    def __init__(self, payload_type: PayloadType, data: str):
        self.payload_type = payload_type
        self.data = data

    def __str__(self):
        return f'{self.payload_type}, {self.data}'