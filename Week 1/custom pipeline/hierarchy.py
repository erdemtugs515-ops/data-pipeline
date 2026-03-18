import json
from dataclasses import dataclass


@dataclass
class hierarchy:
    device_id: str
    location: str
    data: dict
    device_type: str = "IoTDevice"

    def to_row(self):
        return [self.device_type, self.device_id, self.location, json.dumps(self.data)]

    @staticmethod
    def from_row(row):
        dtype, did, loc, raw = row
        data = json.loads(raw)
        cls = {"TemperatureSensor": TemperatureSensor,
               "HumiditySensor": HumiditySensor,
               "MotionSensor": MotionSensor}.get(dtype, hierarchy)
        obj = cls.__new__(cls)
        obj.device_type = dtype
        obj.device_id = did
        obj.location = loc
        obj.data = data
        return obj

    def __str__(self):
        return f"[{self.device_type}] id={self.device_id} loc={self.location} data={self.data}"


@dataclass
class TemperatureSensor(hierarchy):
    device_type: str = "TemperatureSensor"


@dataclass
class HumiditySensor(hierarchy):
    device_type: str = "HumiditySensor"


@dataclass
class MotionSensor(hierarchy):
    device_type: str = "MotionSensor"