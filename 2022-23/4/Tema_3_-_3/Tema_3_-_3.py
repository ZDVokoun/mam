from ElevatorSimulator import elevators
from enum import Enum
from heapq import heapify, heappop, heappush

PRECISION = 0.01
ACCELERATION = 1
WAIT = 20
ID = 'A'

class MinHeap:
    def __init__(self):
        self.h = []
        heapify(self.h)

    def push(self, v: int) -> None:
        heappush(self.h, v)

    def pop(self) -> int:
        return heappop(self.h)

    def empty(self) -> bool:
        return len(self.h) == 0

class MaxHeap:
    def __init__(self):
        self.h = []
        heapify(self.h)

    def push(self, v: int) -> None:
        heappush(self.h, v * -1)

    def pop(self) -> int:
        return heappop(self.h) * -1

    def empty(self) -> bool:
        return len(self.h) == 0

class Direction(Enum):
    down = 0
    up = 1

class LiftState(Enum):
    inactive = 0
    prepairing = 3
    accelerating = 1
    disceleration = 2

class DoorState(Enum):
    closed = 0
    closing = 1
    opened = 2
    opening = 3

class GD:
    direction = Direction.up
    lift = LiftState.inactive
    door = DoorState.opening
    flat = 0
    above = MinHeap()
    below = MaxHeap()
    dest = 0
    start = 0
    waitUntil = 0

def processButtons(e: elevators.Simulator):
    while e.numEvents() > 0:
        ev = e.getNextEvent()
        if ev.isnumeric():
            newFlat = int(ev)
            if newFlat > GD.dest:
                GD.above.push(newFlat)
            elif newFlat < GD.dest:
                GD.below.push(newFlat)
        elif GD.lift == LiftState.inactive:
            if ev == "Open":
                GD.door = DoorState.opening
            else:
                GD.door = DoorState.closing

def openDoor(e: elevators.Simulator, floor: int) -> bool:
    if e.getDoorsPosition(ID, floor) > 1 - PRECISION / 2:
        return True
    else:
        e.openDoors(ID, floor)
        return False

def closeDoor(e: elevators.Simulator, floor: int) -> bool:
    if e.getDoorsPosition(ID, floor) < PRECISION / 2:
        return True
    else:
        e.closeDoors(ID, floor)
        return False

def elevatorSimulationStep(e: elevators.Simulator):
    processButtons(e)
    if GD.door == DoorState.closing and closeDoor(e, GD.start):
        GD.door = DoorState.closed
        if GD.lift == LiftState.prepairing:
            GD.lift = LiftState.accelerating
    elif GD.door == DoorState.opening and openDoor(e, GD.start):
        GD.door = DoorState.opened
    if GD.lift == LiftState.inactive and GD.door == DoorState.opened:
        if (GD.above.empty() and GD.below.empty()) or e.getTime() < GD.waitUntil:
            return
        elif GD.above.empty() and GD.direction == Direction.up:
            GD.direction = Direction.down
        elif GD.below.empty() and GD.direction == Direction.down:
            GD.direction = Direction.up

        if GD.direction == Direction.up:
            GD.dest = GD.above.pop()
        else:
            GD.dest = GD.below.pop()
        GD.door = DoorState.closing
        GD.lift = LiftState.prepairing
    if GD.lift == LiftState.accelerating:
        disceleration_dist = ((e.getSpeed(ID)) ** 2) / (2 * ACCELERATION)
        if disceleration_dist - PRECISION > abs(GD.dest - e.getPosition(ID)):
            GD.lift = LiftState.disceleration
        elif GD.direction == Direction.up:
            e.speedUp(ID)
        else:
            e.speedDown(ID)
    if GD.lift == LiftState.disceleration:
        if abs(e.getSpeed(ID)) < PRECISION / 2:
            GD.lift = LiftState.inactive
            GD.door = DoorState.opening
            GD.start = GD.dest
            GD.waitUntil = e.getTime() + WAIT
        elif GD.direction == Direction.up:
            e.speedDown(ID)
        else:
            e.speedUp(ID)
    
configFileName = 'elevators.json'
elevators.runSimulation(configFileName, elevatorSimulationStep)
