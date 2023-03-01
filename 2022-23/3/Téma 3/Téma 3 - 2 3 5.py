from ElevatorSimulator import elevators

speedStep = 0.1

# Dělím dvaceti, protože rychlost je udávána jako vzdálenost uražená za
# deset kol a ještě dělím dvěmi, protože někde používám neostré rovnosti
ODCHYLKA = speedStep / 20

# ========== Úloha 2 ============

def closeAllDoors(e, idVytahu):
    all_closed = True
    for door, opened in enumerate(e.getDoors(idVytahu)):
        if -ODCHYLKA < opened < ODCHYLKA:
            continue
        else:
            e.closeDoors(idVytahu, door)
            all_closed = False
    return all_closed

# ========== Úloha 3 ============

# Abychom mohli používat krok změny rychlosti jako fyzikální velčinu zrychlení,
# musíme jí vynásobit deseti, protože rychlost výtahu udává vzdálenost uraženou
# za deset kol
a = speedStep * 10

def goToFloor(e, idVytahu, floorNumber):
    pos = e.getPosition(idVytahu)
    v = e.getSpeed(idVytahu)
    if floorNumber - ODCHYLKA < pos < floorNumber + ODCHYLKA:
        if -ODCHYLKA >= v:
            e.speedUp(idVytahu)
        elif ODCHYLKA <= v:
            e.speedDown(idVytahu)
        return True
    if pos < floorNumber:
        # Odvozeno od s = 1 / 2 * a * (t ** 2) a v = a * t
        if (v ** 2) / (2 * a) > floorNumber - pos + ODCHYLKA:
            e.speedDown(idVytahu)
        else:
            e.speedUp(idVytahu)
    elif pos > floorNumber:
        if (v ** 2) / (2 * a) > pos - floorNumber + ODCHYLKA:
            e.speedUp(idVytahu)
        else:
            e.speedDown(idVytahu)
    return False
    
# ========== Úloha 5 ============

def openDoors(e, idVytahu, floorNumber):
    closed = e.getDoorsPosition(idVytahu, floorNumber) < 1 - ODCHYLKA
    if closed:
        e.openDoors(idVytahu, floorNumber)
    return not closed

class GD: # zkráceně GlobalData
    id = 'Vytah1'
    stav = 'otevirani'
    cilovePatro = 0

def prechodovaFunkce(e):
    if GD.stav == 'jede':
        if goToFloor(e, GD.id, GD.cilovePatro):
            print('Vytah dorazil do ' + str(GD.cilovePatro) + '. patra.')
            GD.stav = 'otevirani'
    elif GD.stav == 'otevirani':
        if openDoors(e, GD.id, GD.cilovePatro):
            GD.stav = 'ceka'
    elif GD.stav == 'zavirani':
        if closeAllDoors(e, GD.id):
            GD.stav = 'jede'
    elif GD.stav == 'ceka' and e.numEvents() > 0:
        event = e.getNextEvent()
        if event == 'prizemi':
            GD.cilovePatro = 0
            GD.stav = 'zavirani'
        elif event == '1.patro':
            GD.cilovePatro = 1
            GD.stav = 'zavirani'
        elif event == '2.patro':
            GD.cilovePatro = 2
            GD.stav = 'zavirani'
        else:
            print('Stisknuto nezname tlacitko.')

elevators.runSimulation("elevators.json", prechodovaFunkce)
