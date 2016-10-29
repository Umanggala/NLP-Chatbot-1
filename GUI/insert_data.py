from pymongo import MongoClient
from datetime import datetime

client = MongoClient()
db = client.test
'''
result = db.restaurants.insert_one(
    {
        "address": {
            "street": "1119W",
            "zipcode": "90007",
            "building": "1",
            "coord": [-73.9557413, 40.7720266]
        },
        "borough": "Manhattan",
        "cuisine": "Italian",
        "grades": [
            {
                "date": datetime.strptime("2014-10-01", "%Y-%m-%d"),
                "grade": "A",
                "score": 11
            },
            {
                "date": datetime.strptime("2014-01-16", "%Y-%m-%d"),
                "grade": "B",
                "score": 17
            }
        ],
        "name": "Vella",
        "restaurant_id": "41704620"
    }
)
'''
cursor = db.restaurants.find({"borough": "Manhattan"})
for document in cursor:
    print(document)
