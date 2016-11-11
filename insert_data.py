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
    name_search = {}
    count = 0
    for document in cursor:
        name_search[count] = [document['name'],document['rating']]
        count += 1
    return name_search

def search_max(cursor):
    count = 0
    sum = 0
    temp = 0
    for document in cursor:
        sum += int(document['rating'])
        count += 1
    temp = sum / count
    return temp

def search_data_cuisine(search_cuisine):
    average = []
    if(db.restaurants.find({"cuisine":search_cuisine, "address.street":'figueroa'}).count() > 0):
        cursor1 = (db.restaurants.find({"cuisine":search_cuisine, "address.street":'figueroa'}))
        average.append(search_max(cursor1))

    if(db.restaurants.find({"cuisine":search_cuisine, "address.street":'hollywood'}).count() > 0):
        cursor2 = db.restaurants.find({"cuisine":search_cuisine, "address.street":'hollywood'})
        average.append(search_max(cursor2))

    if(db.restaurants.find({"cuisine":search_cuisine, "address.street":'beverely hills'}).count() > 0):
        cursor3 = db.restaurants.find({"cuisine": search_cuisine, "address.street": 'beverely hills'})
        average.append(search_max(cursor3))

    if(db.restaurants.find({"cuisine":search_cuisine, "address.street":'artesia'}).count() > 0):
        cursor4 = db.restaurants.find({"cuisine":search_cuisine, "address.street":'artesia'})
        average.append(search_max(cursor4))

    if(db.restaurants.find({"cuisine":search_cuisine, "address.street":'santa monica'}).count() > 0):
        cursor5 = db.restaurants.find({"cuisine":search_cuisine, "address.street":'santa monica'})
        average.append(search_max(cursor5))

    average_cuisine = max(average)
    index = average.index(max(average))

    if(index == 0):
        cursor1 = (db.restaurants.find({"cuisine": search_cuisine, "address.street": 'figueroa'}))
        return average_cuisine, cursor1

    elif(index==1):
        cursor2 = db.restaurants.find({"cuisine": search_cuisine, "address.street": 'hollywood'})
        return average_cuisine, cursor2

    elif (index == 2):
        cursor3 = db.restaurants.find({"cuisine": search_cuisine, "address.street": 'beverely hills'})
        return average_cuisine, cursor3

    elif (index == 3):
        cursor4 = db.restaurants.find({"cuisine": search_cuisine, "address.street": 'artesia'})
        return average_cuisine, cursor4

    elif (index == 4):
        cursor5 = db.restaurants.find({"cuisine": search_cuisine, "address.street": 'santa monica'})
        return average_cuisine, cursor5



def search_location_data(search_location):
    average = []
    if (db.restaurants.find({"cuisine": 'indian', "address.street": search_location}).count() > 0):
        cursor = db.restaurants.find({"cuisine": 'indian', "address.street": search_location})
        average.append(search_max(cursor))

    if (db.restaurants.find({"cuisine": 'italian', "address.street": search_location}).count() > 0):
        cursor1 = db.restaurants.find({"cuisine": 'italian', "address.street": search_location})
        average.append(search_max(cursor1))

    if (db.restaurants.find({"cuisine": 'pizza', "address.street": search_location}).count() > 0):
        cursor2 = db.restaurants.find({"cuisine": 'pizza', "address.street": search_location})
        average.append(search_max(cursor2))

    if (db.restaurants.find({"cuisine": 'mexican', "address.street": search_location}).count() > 0):
        cursor3 = db.restaurants.find({"cuisine": 'mexican', "address.street": search_location})
        average.append(search_max(cursor3))

    if (db.restaurants.find({"cuisine": 'chinese', "address.street": search_location}).count() > 0):
        cursor4 = db.restaurants.find({"cuisine": 'chinese', "address.street": search_location})
        average.append(search_max(cursor4))

    average_location = max(average)
    index = average.index(max(average))

    if (index == 0):
        cursor1 = db.restaurants.find({"cuisine": 'indian', "address.street": search_location})
        return average_location, cursor1

    elif (index == 1):
        cursor2 = db.restaurants.find({"cuisine": 'italian', "address.street": search_location})
        return average_location, cursor2

    elif (index == 2):
        cursor3 = db.restaurants.find({"cuisine": 'pizza', "address.street": 'beverely Hills'})
        return average_location, cursor3

    elif (index == 3):
        cursor4 = db.restaurants.find({"cuisine": 'mexican', "address.street": 'artesia'})
        return average_location, cursor4

    elif (index == 4):
        cursor5 = db.restaurants.find({"cuisine": 'chinese', "address.street": 'santa monica'})
        return average_location, cursor5



restaurant = insert_data_from_text()
insert_into_database(restaurant)
sum_rating = 0
number_of_results = 0
restaurant_names = search_data("pizza","cheap","figueroa")


for i in restaurant_names:
    sum_rating = sum_rating + int(restaurant_names.get(i)[1])
    number_of_results += 1

average_rating = sum_rating / number_of_results

if(average_rating >= 3):
    
    print(restaurant_names)
else:
    average_location_rating, cursor = search_data_cuisine("pizza")
    for document in cursor:
        print(document['name'])

    average_cuisine_rating, cursor1 = search_location_data("figueroa")
    for documents in cursor1:
        print(documents['name'])


