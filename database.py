import pymongo

client = pymongo.MongoClient("mongodb+srv://admin:admin@dicemanagement-6rx9o.azure.mongodb.net/test?retryWrites=true&w=majority")
db = client["DiceDB"]
die = db["Die"] 
diceset = db["DiceSet"] 

print(db.list_collection_names())

