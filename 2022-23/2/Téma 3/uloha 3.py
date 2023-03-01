from ElevatorSimulator import elevators
from dataclasses import dataclass


@dataclass
class State:
    wait_until: int


state = State(0)


def elevatorSimulationStep(e):
    pos = round(e.getPosition("A"))
    for i in range(4):
        if i == pos:
            if e.getDoorsPosition("A", i) < 0.9:
                e.openDoors("A", i)
        else:
            if e.getDoorsPosition("A", i) > 0.1:
                e.closeDoors("A", i)
    if e.getTime() < state.wait_until:
        return
    if e.getPosition("A") >= 3.0:
        state.wait_until = e.getTime() + 30
        e.speedDown("A")
    elif e.getPosition("A") <= 0.0:
        state.wait_until = e.getTime() + 30
        e.speedUp("A")


elevators.runSimulation("uloha 3.json", elevatorSimulationStep)
