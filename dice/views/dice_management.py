from flask import Blueprint, jsonify
from dice.classes.database import Database
from dice.classes.DiceSet import DiceSet, WrongDiceNumberError
from dice.classes.DiceSet import NonExistingSetError, WrongArgumentTypeError

dice_management = Blueprint('dice_management', __name__)

db = Database()


@dice_management.route('/', methods=['GET'])
def _index():
    print("App init")
    return jsonify({"message": "App started"})


@dice_management.route('/rolldice/<dicenumber>/<dicesetid>', methods=['GET'])
def _roll(dicenumber, dicesetid):
    try:
        dice = DiceSet(dicesetid)
    except NonExistingSetError as err:
        return jsonify({
            "message": err.value,
            "dice_set": "",
            "roll": [],
        })

    try:
        roll = dice.throw_dice(dicenumber)
    except WrongDiceNumberError as err:
        return jsonify({
            "message": err.value,
            "dice_set": "",
            "roll": [],
            })

    except WrongArgumentTypeError as err:
        return jsonify({
            "message": err.value,
            "dice_set": "",
            "roll": [],
            })

    return jsonify({
        "message": "Correct roll",
        "dice_set": dicesetid,
        "roll": roll})


@dice_management.route('/dicesets', methods=['GET'])
def get_dicesets():
    ds = db.getAllCollection("DiceSet")
    dicesets = []
    for e in ds:
        a = {
            "name": e["name"],
            "total_dice": db.total_dice_in_set(e["name"])
        }
        dicesets.append(a)
    return jsonify({"available_dicesets": dicesets})
