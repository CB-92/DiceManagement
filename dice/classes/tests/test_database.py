import unittest
from dice.classes.database import Database


class TestDatabase(unittest.TestCase):

    def test_collection_die(self):
        db = Database()

        db.remove_all_dice_in_set("basic")
        self.assertEqual(db.total_dice_in_set("basic"), 0)

        # Insert files in collection Die
        db.initDiceCollection("basic")
        self.assertEqual(db.total_dice_in_set("basic"), 6)
        self.assertEqual(db.total_dice_in_set("basic"), 6)

    def test_collection_dice(self):
        db = Database()
        db.initDiceCollection("dice/resources")
        diceset = db.getAllCollection("DiceSet")
        diceset_len = diceset.count()
        self.assertEqual(diceset_len, 2)


if __name__ == '__main__':
    unittest.main()
