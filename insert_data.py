from pymongo import MongoClient
import csv


client = MongoClient()
db = client.test

global cuisine_search
global location_search
global price_tag_search

#Inserts the data from the file.
#Format: restaurant_name <tab> place <tab> price_range <tab> cuisine

def set_data(cuisine,location,price_tag):
    global cuisine_search
    global location_search
    global price_tag_search

    cuisine_search = cuisine
    location_search = location
    price_tag_search = price_tag

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
                "address": new_dict.get(i)[1],
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
    cursor = db.restaurants.find({"cuisine":search_cuisine,"price_range":search_price_range,"address":search_location})
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
    new_dict = {}
    i = 0
    if(db.restaurants.find({"cuisine":search_cuisine, "address":'figueroa'}).count() > 0):
        cursor1 = (db.restaurants.find({"cuisine":search_cuisine, "address":'figueroa'}))
        i = search_max(cursor1)
        new_dict[i] = 1

    if(db.restaurants.find({"cuisine":search_cuisine, "address":'hollywood'}).count() > 0):
        cursor2 = db.restaurants.find({"cuisine":search_cuisine, "address":'hollywood'})
        i = search_max(cursor2)
        new_dict[i] = 2

    if(db.restaurants.find({"cuisine":search_cuisine, "address":'beverely hills'}).count() > 0):
        cursor3 = db.restaurants.find({"cuisine": search_cuisine, "address": 'beverely hills'})
        i = search_max(cursor3)
        new_dict[i] = 3

    if(db.restaurants.find({"cuisine":search_cuisine, "address":'artesia'}).count() > 0):
        cursor4 = db.restaurants.find({"cuisine":search_cuisine, "address":'artesia'})
        i = search_max(cursor4)
        new_dict[i] = 4

    if(db.restaurants.find({"cuisine":search_cuisine, "address":'santa monica'}).count() > 0):
        cursor5 = db.restaurants.find({"cuisine":search_cuisine, "address":'santa monica'})
        i = search_max(cursor5)
        new_dict[i] = 5

    index = 0
    max_average = 0

    for i, j in new_dict.items():
        if(i>max_average):
            max_average = i
            index = j


    if(index == 1):
        cursor1 = (db.restaurants.find({"cuisine": search_cuisine, "address": 'figueroa'}))
        return max_average, cursor1

    elif(index==2):
        cursor2 = db.restaurants.find({"cuisine": search_cuisine, "address": 'hollywood'})
        return max_average, cursor2

    elif (index == 3):
        cursor3 = db.restaurants.find({"cuisine": search_cuisine, "address": 'beverely hills'})
        return max_average, cursor3

    elif (index == 4):
        cursor4 = db.restaurants.find({"cuisine": search_cuisine, "address": 'artesia'})
        return max_average, cursor4

    elif (index == 5):
        cursor5 = db.restaurants.find({"cuisine": search_cuisine, "address": 'santa monica'})
        return max_average, cursor5



def search_location_data(search_location):
    average = []
    new_dict = {}
    i = 0
    if (db.restaurants.find({"cuisine": 'indian', "address": search_location}).count() > 0):
        cursor1 = db.restaurants.find({"cuisine": 'indian', "address": search_location})
        i = search_max(cursor1)
        new_dict[i] = 1

    if (db.restaurants.find({"cuisine": 'italian', "address": search_location}).count() > 0):
        cursor2 = db.restaurants.find({"cuisine": 'italian', "address": search_location})
        i = search_max(cursor2)
        new_dict[i] = 2

    if (db.restaurants.find({"cuisine": 'pizza', "address": search_location}).count() > 0):
        cursor3 = db.restaurants.find({"cuisine": 'pizza', "address": search_location})
        i = search_max(cursor3)
        new_dict[i] = 3

    if (db.restaurants.find({"cuisine": 'mexican', "address": search_location}).count() > 0):
        cursor4 = db.restaurants.find({"cuisine": 'mexican', "address": search_location})
        i = search_max(cursor4)
        new_dict[i] = 4

    if (db.restaurants.find({"cuisine": 'chinese', "address": search_location}).count() > 0):
        cursor5 = db.restaurants.find({"cuisine": 'chinese', "address": search_location})
        i = search_max(cursor5)
        new_dict[i] = 5

    index = 0
    max_average = 0

    for i, j in new_dict.items():
        if (i > max_average):
            max_average = i
            index = j

    if (index == 1):
        cursor1 = db.restaurants.find({"cuisine": 'indian', "address": search_location})
        return max_average, cursor1

    elif (index == 2):
        cursor2 = db.restaurants.find({"cuisine": 'italian', "address": search_location})
        return max_average, cursor2

    elif (index == 3):
        cursor3 = db.restaurants.find({"cuisine": 'pizza', "address": 'beverely Hills'})
        return max_average, cursor3

    elif (index == 4):
        cursor4 = db.restaurants.find({"cuisine": 'mexican', "address": 'artesia'})
        return max_average, cursor4

    elif (index == 5):
        cursor5 = db.restaurants.find({"cuisine": 'chinese', "address": 'santa monica'})
        return max_average, cursor5


def set_data(cuisine, location, price_tag):
    global cuisine_search
    global location_search
    global price_tag_search

    cuisine_search = cuisine
    location_search = location
    price_tag_search = price_tag

    restaurant = insert_data_from_text()
    insert_into_database(restaurant)
    sum_rating = 0
    number_of_results = 0
    restaurant_names = search_data(cuisine_search,price_tag_search,location_search)
    average_rating = 0
    suggestion_dict = {}

    for i in restaurant_names:
        sum_rating = sum_rating + int(restaurant_names.get(i)[1])
        number_of_results += 1

        if(number_of_results > 0):
            average_rating = sum_rating / number_of_results
        else:
            average_rating = 0

    result = ""
    flag = 0


    if(average_rating >= 3):
        result = "Good choice. Here are few options\n"
        for i in restaurant_names:
            print(restaurant_names.get(i)[0] + "\n")
            result += restaurant_names.get(i)[0] +  "\n"
            flag = 1
        return result, suggestion_dict

    else:
        print("Locations for amazing mexican food")
        rating, cursor = search_data_cuisine(cuisine_search)

        for document in cursor:
            suggestion_dict['Location'] = document['address']
            result += document['name'] + " at " + document['address'] + "\n"


        print("Cuisine at santa monica")
        rating , cursor = search_location_data(location_search)
        for document in cursor:
            suggestion_dict['Cuisine'] = document['cuisine']
            result += document['name'] + " at " + document['address'] + "\n"
        return result,suggestion_dict




