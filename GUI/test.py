#new_dict = {"/Users/umanggala/Desktop/Courses/NLP/NLP-Chatbot/restaurants.txt"}
from pymongo import MongoClient

client = MongoClient()
db = client.test

restaurant = {}
name = ""
place = ""
price_range = ""
cuisine = ""
count = 1

with open("/Users/umanggala/Desktop/Courses/NLP/NLP-Chatbot/restaurants.txt") as f:

    for line in f:
        splitLine = line.split("\t")
        name = splitLine[0]
        place = splitLine[1]
        price_range = splitLine[2]
        cuisine = splitLine[3].rstrip('\n')

        restaurant[count] = [name,place,price_range,cuisine]
        count += 1
f.close()

result = db.restaurants.remove()

id = 41704620
for i in restaurant:
    result = db.restaurants.insert_one(
        {
            "address": {
                "street": restaurant.get(i)[1],
                "zipcode": "90007",
            },
            "cuisine": restaurant.get(i)[3],
            "name": restaurant.get(i)[0],
            "restaurant_id": id,
            "price_range": restaurant.get(i)[2]
        }
    )
    id += 1

def search_data(search_cuisine,search_price_range,search_location):
    cursor = db.restaurants.find({"cuisine":search_cuisine,"price_range":search_price_range,"address.street":search_location})
    name_search = {}
    count = 0
    for document in cursor:
        name_search[count] = document['name']
        count += 1
    return name_search

restaurant_names = search_data("indian","cheap","artesia")

print(restaurant_names)