import pymongo

my_client = pymongo.MongoClient(
    'mongodb+srv://alice:myPassword@mylittlecluster-qsart.gcp.mongodb.net/test?retryWrites=true'
)

try:
    print("MongoDB version is %s" % 
            my_client.server_info()['version'])
except pymongo.errors.OperationFailure as error:
    print(error)
    quit(1)

my_database = my_client.test

my_collection = my_database.foods

try:
    my_collection.insert_one({
        "_id": 1,
        "name": "pizza",
        "calories": 266,
        "fats": {
            "saturated": 4.5,
            "trans": 0.2
        },
        "protein": 11
    })

    my_collection.insert_many([
        {
            "_id": 2,
            "name": "hamburger",
            "calories": 295, "protein": 17,
            "fats": { "saturated": 5.0, "trans": 0.8 },
        },
        {
            "_id": 3,
            "name": "taco",
            "calories": 226, "protein": 9,
            "fats": { "saturated": 4.4, "trans": 0.5 },
        }
    ])
except:
    print("Documents exist already")

my_cursor = my_collection.find()

for item in my_cursor:
    print(item["name"])

# Result is:
#   pizza
#   hamburger
#   taco

my_cursor = my_collection.find({
	"name": "pizza"
})

my_cursor = my_collection.find({
    "calories": { "$lt": 280 }
})

for item in my_cursor:
    print("Name: %s, Calories: %d" % 
        (item["name"], item["calories"]))

# Result is:
#   Name: pizza, Calories: 266
#   Name: taco, Calories: 226

my_cursor = my_collection.find({
    "fats.trans": { "$gte": 0.5 }
})

for item in my_cursor:
    print("Name: %s, Trans fats: %.2f" % 
        (item["name"], item["fats"]["trans"]))

# Result is:
#	Name: hamburger, Trans fats: 0.80
#	Name: taco, Trans fats: 0.50


my_collection.update_one(
    { "name": "taco" }, # query
    {
        "$set": {       # new data
            "fiber": 3.95,
            "sugar": 0.9
        }
    }
)

my_cursor = my_collection.find({"name": "taco"})

for item in my_cursor:
    print("Name: %s, Sugar: %.2f, Fiber: %.2f" % 
        (item["name"], item["sugar"], item["fiber"]))

my_collection.delete_many({
    "calories": {
        "$lt": 300
    }
})
