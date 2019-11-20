import unittest
import json
from dice.classes.database import Database
from dice.app import create_app

_app = None


class TestDiceManagement(unittest.TestCase):

    def test_init(self):
        global _app
        if _app is None:
            tested_app = create_app(debug=True)
            _app = tested_app
        else:
            tested_app = _app

        with tested_app.test_client() as client:
            db = Database()
            db.initDiceSets("dice/resources")
            db.remove_all_dice_in_set("basic")
            db.remove_all_dice_in_set("halloween")
            db.initDiceCollection("basic")
            db.initDiceCollection("halloween")
            reply = client.get("/")
            body = json.loads(str(reply.data, 'utf8'))
            expected = {
                "message": "App started"
            }
            self.assertEqual(body, expected)

    def test_available_sets(self):
        global _app
        if _app is None:
            tested_app = create_app(debug=True)
            _app = tested_app
        else:
            tested_app = _app

        with tested_app.test_client() as client:
            db = Database()
            db.initDiceSets("dice/resources")
            db.remove_all_dice_in_set("basic")
            db.remove_all_dice_in_set("halloween")
            db.initDiceCollection("basic")
            db.initDiceCollection("halloween")
            # get available dice sets
            reply = client.get("/dicesets")
            body = json.loads(str(reply.data, 'utf8'))
            available_dicesets = body["available_dicesets"]
            self.assertEqual(len(available_dicesets), 2)
            basic = available_dicesets[0]
            self.assertEqual(basic["name"], "basic")
            halloween = available_dicesets[1]
            self.assertEqual(halloween["total_dice"], 5)

    def test_roll(self):

        global _app
        if _app is None:
            tested_app = create_app(debug=True)
            _app = tested_app
        else:
            tested_app = _app

        with tested_app.test_client() as client:
            db = Database()
            db.initDiceSets("dice/resources")
            db.remove_all_dice_in_set("basic")
            db.remove_all_dice_in_set("halloween")
            db.initDiceCollection("basic")
            db.initDiceCollection("halloween")

            # non-integer dice number
            reply = client.get('/rolldice/pippo/basic')
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(reply.status_code, 200)
            self.assertEqual(body, {
                "message": "Dice number needs to be an integer!",
                "dice_set": "",
                "roll": [],
            }
            )

            # wrong dice number (<0)
            reply = client.get('/rolldice/0/basic')
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(reply.status_code, 200)
            self.assertEqual(body, {
                "message": "Wrong dice number!",
                "dice_set": "",
                "roll": [],
            }
            )

            # wrong dice number (> len diceset)
            reply = client.get('/rolldice/12/basic')
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(reply.status_code, 200)
            self.assertEqual(body, {
                "message": "Wrong dice number!",
                "dice_set": "",
                "roll": [],
            }
            )

            # non-existing dice set
            reply = client.get('/rolldice/6/pippo')
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(reply.status_code, 200)
            self.assertEqual(body, {
                "message": "Dice set pippo doesn't exist!",
                "dice_set": "",
                "roll": [],
            })

            # correct roll
            reply = client.get('/rolldice/5/basic')
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(reply.status_code, 200)
            dice_set = body["dice_set"]
            roll = body["roll"]
            self.assertEqual(dice_set, "basic")
            self.assertEqual(len(roll), 5)


if __name__ == '__main__':
    unittest.main()
