from pymongo import MongoClient
import csv


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

    with open("/Users/umanggala/Desktop/Courses/NLP/NLP-Chatbot/restaurants.csv", 'r', errors='replace') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            name = row[0]
            place = row[1]
            price_range = row[2]
            cuisine = row[3]
            rating = row[4]

            new_dict[count] = [name, place, price_range, cuisine,rating]
            count += 1

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
                "price_range": new_dict.get(i)[2],
                "rating":new_dict.get(i)[4]
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
        name_search[count] = [document['name'],document['rating']]
        count += 1
    return name_search


restaurant = insert_data_from_text()
insert_into_database(restaurant)

sum_rating = 0
number_of_results = 0
restaurant_names = search_data("pizza","cheap","Figueroa")
for i in restaurant_names:
    sum_rating = sum_rating + int(restaurant_names.get(i)[1])
    number_of_results += 1


average_rating = sum_rating / number_of_results
print(average_rating)

if(average_rating >= 3):
    print("results are good")
else:
    print("fetch new results")
