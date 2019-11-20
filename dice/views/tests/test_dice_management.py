import unittest
import json
from dice.app import create_app

_app = None


class TestDiceManagement(unittest.TestCase):

    def test_available_tests(self):
        global _app
        if _app is None:
            tested_app = create_app(debug=True)
            _app = tested_app
        else:
            tested_app = _app

        with tested_app.test_client() as client:
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

            # wrong dice number
            reply = client.get('/rolldice/12/basic')
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(reply.status_code, 200)
            self.assertEqual(body, {
                "message": "Wrong dice number!"
            }
            )

            # non-existing dice set
            reply = client.get('/rolldice/6/pippo')
            body = json.loads(str(reply.data, 'utf8'))
            self.assertEqual(reply.status_code, 200)
            self.assertEqual(body, {
                "message": "Dice set pippo doesn't exist!"
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
