text = 'Cheap Restraunts in Marina Del Ray.'
#Prepare your text. Remove "." (and other unnecessary marks).
#Then split it into a list of words.
text = text.replace('.','').split(' ')

#Insert the cities you want to search for.
cities =  {"Los Angeles":["Los","Angeles"],"Santa Monica":["Santa","Monica"],"Marina Del Ray":["Marina","Del","Ray"]}

found_match = False
for word in text:
    if found_match:
        cityTest = cityTest
    else:
        cityTest = ''
    found_match = False
    for city in cities.keys():
        if word in cities[city]:
            cityTest += word + ' '
            found_match = True
        if cityTest.split(' ')[0:-1] == city.split(' '):
            print (city)    #Print if it found a city.