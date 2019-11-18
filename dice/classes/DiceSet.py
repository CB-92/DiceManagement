import random as rnd
import re
from dice.database import Database

db = Database()


class Die:

    def __init__(self, diejson):
        self.faces = []
        self.pip = None

        self.faces.append(diejson["face0"])
        self.faces.append(diejson["face1"])
        self.faces.append(diejson["face2"])
        self.faces.append(diejson["face3"])
        self.faces.append(diejson["face4"])
        self.faces.append(diejson["face5"])
        self.throw_die()

    def throw_die(self):
        if self.faces:  # pythonic for list is not empty
            self.pip = rnd.choice(self.faces)
            return self.pip
        else:
            raise IndexError("throw_die(): empty die error.")


class DiceSet:

    def __init__(self, set_name):
        self.dice = []
        self.pips = []

        ds = db.get_all_dice_in_set(set_name)

        # TODO: check if diceset exists!

        for e in ds:
            die = Die(e)
            self.dice.append(die)

    def throw_dice(self, dicenumber):
        pattern = re.compile("^[0-9]*$")

        if(pattern.match(dicenumber)):
            dicenumber = int(dicenumber)
            if(dicenumber <= 0 or dicenumber > len(self.dice)):
                raise WrongDiceNumberError("Wrong dice number!")
            else:
                for i in range(dicenumber):
                    self.pips.append(self.dice[i].throw_die())
        else:
            raise WrongArgumentTypeError("Dice number needs to be an integer!")

        return self.pips


class NonExistingSetError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class WrongArgumentTypeError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class WrongDiceNumberError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
