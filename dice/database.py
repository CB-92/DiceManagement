import json
import pymongo
import natsort
import os
import glob

client = pymongo.MongoClient("mongodb+srv://admin:admin@dicemanagement-6rx9o.azure.mongodb.net/test?retryWrites=true&w=majority")
db = client["DiceDB"]
die = db["Die"]
diceset = db["DiceSet"]


class Database:

    def initDiceSets(self, res_folder):
        db["DiceSet"].drop()
        subfolders = [f.name for f in os.scandir(res_folder) if f.is_dir()]
        print(subfolders)
        for f in subfolders:
            t = {
                "name": f,
                "folder": res_folder + "/" + f
            }
            diceset.insert_one(t)

    def initDiceCollection(self, dice_folder):
        folder = glob.glob(os.path.join(dice_folder, '*.json'))
        sorted(folder)
        for filename in natsort.natsorted(folder, reverse=False):
            with open(filename) as f:
                file_data = json.load(f)
            die.insert_one(file_data)

    def getAllCollection(self, collection):
        return db[collection].find({})

    def get_all_dice_in_set(self, set_name):
        return db["Die"].find({"set": set_name})
