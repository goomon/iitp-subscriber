from typing import TypedDict, List


class ChestAxis(TypedDict):
    x: int
    y: int
    z: int


# Chest Accelerometer
class ChestACC(TypedDict):
    hz: int
    value: List[ChestAxis]


# Chest Electrocardiogram
class ChestEGC(TypedDict):
    hz: int
    value: List[int]


# Chest Electrodemal
class ChestEDA(TypedDict):
    hz: int
    value: List[int]


# Chest Electromyogram
class ChestEMG(TypedDict):
    hz: int
    value: List[int]


# Chest Temperature
class ChestTemp(TypedDict):
    hz: int
    value: List[int]


# Chest Respiration
class ChestResp(TypedDict):
    hz: int
    value: List[int]


class ChestDeviceSensorValue(TypedDict):
    chest_acc: ChestACC
    chest_ecg: ChestEGC
    chest_eda: ChestEDA
    chest_emg: ChestEMG
    chest_temp: ChestTemp
    chest_resp: ChestResp


class ChestDeviceSensorRecord(TypedDict):
    user_id: str
    timestamp: int
    window_size: int
    value: List[ChestDeviceSensorValue]