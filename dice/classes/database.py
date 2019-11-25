import json
import pymongo
import natsort
import os
import glob

client = pymongo.MongoClient("mongodb://mongo:27017/")
db = client["DiceDB"]
die = db["Die"]
diceset = db["DiceSet"]


class Database:

    def initDiceSets(self, res_folder):
        if("DiceSet" not in db.list_collection_names()):
            subfolders = [f.name for f in os.scandir(res_folder) if f.is_dir()]
            for f in subfolders:
                name = f.replace("_set", "")
                t = {
                    "name": name,
                    "folder": res_folder + "/" + f
                }
                diceset.insert_one(t)

    def initDiceCollection(self, dice_set_name):
        dice_folder = diceset.find({"name": dice_set_name})

        for e in dice_folder:
            folder = glob.glob(os.path.join(e["folder"], '*.json'))
            sorted(folder)
            for filename in natsort.natsorted(folder, reverse=False):
                with open(filename) as f:
                    file_data = json.load(f)
                die.insert_one(file_data)

    def getAllCollection(self, collection):
        return db[collection].find({})

    def get_all_dice_in_set(self, set_name):
        return db["Die"].find({"set": set_name})

    def remove_all_dice_in_set(self, set_name):
        myquery = {"set": set_name}
        db["Die"].delete_many(myquery)

    def total_dice_in_set(self, set_name):
        myquery = {"set": set_name}
        return db["Die"].count_documents(myquery)
