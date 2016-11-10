from pymongo import MongoClient


client = MongoClient()
db = client.test

#Inserts the data from the file.
#Format: restaurant_name <tab> place <tab> price_range <tab> cuisine

def insert_data_from_text():

    new_dict = {}
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
            cuisine = splitLine[3]

            new_dict[count] = [name, place, price_range, cuisine]
            count += 1
    f.close()

    return new_dict

#Inserts the data in the database
def insert_into_database(new_dict):

    result = db.restaurants.remove()

    id = 41704620
    for i in new_dict:
        result = db.restaurants.insert_one(
            {
                "address": {
                    "street": new_dict.get(i)[1],
                    "zipcode": "90007",
                },
                "cuisine": new_dict.get(i)[3].rstrip('\n'),
                "name": new_dict.get(i)[0],
                "restaurant_id": id,
                "price_range": new_dict.get(i)[2]
            }
        )
        id += 1

#Searches the name of the restaurants. Returns a dictionary containing the names of the restaurants.

def search_data(search_cuisine,search_price_range,search_location):
    cursor = db.restaurants.find({"cuisine":search_cuisine,"price_range":search_price_range,"address.street":search_location})
    #cursor = db.restaurants.find({})
    name_search = {}
    count = 0
    for document in cursor:
        name_search[count] = document['name']
        count += 1
    return name_search


restaurant = insert_data_from_text()
insert_into_database(restaurant)

restaurant_names = search_data("indian","cheap","artesia")
print(restaurant_names)
