from flask import Blueprint, jsonify
from dice.classes.DiceSet import DiceSet, WrongDiceNumberError
from dice.classes.DiceSet import NonExistingSetError, WrongArgumentTypeError

dice_management = Blueprint('dice_management', __name__)

@dice_management.route('/rolldice/<dicenumber>/<dicesetid>', methods=['GET'])
def _roll(dicenumber, dicesetid):
    try:
        dice = DiceSet(dicesetid)
    except NonExistingSetError as err:
        return jsonify({"message": err.value()})

    try:
        roll = dice.throw_dice(dicenumber)
    except WrongDiceNumberError as err:
        return jsonify({"message": err.value()})

    except WrongArgumentTypeError as err:
        return jsonify({"message": err.value()})

    return jsonify({
        "dice_set": dicesetid,
        "roll": roll})
