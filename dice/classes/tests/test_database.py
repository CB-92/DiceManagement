import unittest
from dice.classes.database import Database


class TestDatabase(unittest.TestCase):

    def test_collection_die(self):
        db = Database()
        db.initDiceSets("dice/resources")
        db.remove_all_dice_in_set("basic")
        db.remove_all_dice_in_set("halloween")
        self.assertEqual(db.total_dice_in_set("basic"), 0)

        # Insert files in collection Die
        db.initDiceCollection("basic")
        self.assertEqual(db.total_dice_in_set("basic"), 6)
        self.assertEqual(db.total_dice_in_set("basic"), 6)

        db.initDiceCollection("halloween")
        halloween_set = db.get_all_dice_in_set("halloween")
        halloween_len = halloween_set.count()
        self.assertEqual(halloween_len, 5)

    def test_collection_dice(self):
        db = Database()
        db.initDiceSets("dice/resources")
        db.remove_all_dice_in_set("basic")
        db.remove_all_dice_in_set("halloween")
        db.initDiceCollection("basic")
        db.initDiceCollection("halloween")
        diceset = db.getAllCollection("DiceSet")
        diceset_len = diceset.count()
        self.assertEqual(diceset_len, 2)


if __name__ == '__main__':
    unittest.main()
