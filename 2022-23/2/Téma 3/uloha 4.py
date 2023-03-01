from ElevatorSimulator import elevators
from dataclasses import dataclass
from typing import List
from math import floor, ceil
from decimal import Decimal as D

ACCELERATION = D("0.1")


@dataclass
class State:
    queue: List[bool]
    stop: bool
    halfway: D
    wait_until: int


state = State([], False, D("0.0"), 0)


def processEvents(e):
    while e.numEvents() > 0:
        match e.getNextEvent():
            case "nahoru":
                state.queue.append(True)
                state.stop = False
            case "dolu":
                state.queue.append(False)
                state.stop = False
            case "stop":
                state.queue.clear()
                state.stop = True
            case _:
                print("Unknown event")


def processQueue(e):
    if state.wait_until > e.getTime():
        return
    if state.stop:
        if e.getSpeed("A") > 0.0:
            e.speedDown("A")
        elif e.getSpeed("A") < 0.0:
            e.speedUp("A")
        return
    if len(state.queue) > 0:
        speed = D(e.getSpeed("A")).quantize(D("1.00"))
        position = D(e.getPosition("A")).quantize(D("1.00"))
        # print(speed, position, state.halfway, type(state.halfway))
        if state.queue[0]:
            if speed == D(0):
                state.halfway = (D("1.00") - position) / D("2.00") + position
            if position >= state.halfway and speed > ACCELERATION:
                e.speedDown("A")
            elif position >= D("1.0"):
                e.speedDown("A")
                state.queue = state.queue[1:]
                state.wait_until = e.getTime() + 20
            else:
                e.speedUp("A")
        else:
            if speed == D("0.0"):
                state.halfway = position / D("2.00")
            if position <= state.halfway and speed < -ACCELERATION:
                e.speedUp("A")
            elif position <= D("0.0"):
                e.speedUp("A")
                state.queue = state.queue[1:]
                state.wait_until = e.getTime() + 20
            else:
                e.speedDown("A")


def processDoors(e):
    position = D(e.getPosition("A")).quantize(D("1.0"))
    if position >= D("1.0"):
        if e.getDoorsPosition("A", 1) < 1.0:
            e.openDoors("A", 1)
        if e.getDoorsPosition("A", 0) > 0.01:
            e.closeDoors("A", 0)
    elif position <= D("0.0"):
        if e.getDoorsPosition("A", 0) < 1.0:
            e.openDoors("A", 0)
        if e.getDoorsPosition("A", 1) > 0.01:
            e.closeDoors("A", 1)
    else:
        if e.getDoorsPosition("A", 1) > 0.01:
            e.closeDoors("A", 1)
        if e.getDoorsPosition("A", 0) > 0.01:
            e.closeDoors("A", 0)


def elevatorSimulationStep(e):
    processEvents(e)
    processQueue(e)
    processDoors(e)
    # pos = round(e.getPosition("A"))
    # for i in range(4):
    #     if i == pos:
    #         if e.getDoorsPosition("A", i) < 0.9:
    #             e.openDoors("A", i)
    #     else:
    #         if e.getDoorsPosition("A", i) > 0.1:
    #             e.closeDoors("A", i)
    # if e.getPosition("A") >= 3.0:
    #     time.sleep(1)
    #     e.speedDown("A")
    # elif e.getPosition("A") <= 0.0:
    #     time.sleep(1)
    #     e.speedUp("A")


elevators.runSimulation("uloha 4.json", elevatorSimulationStep)
