import pymongo as pymongo
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId


####  CHANGE CONNECTION STRING TO YOUR DATABASE   ###
client = pymongo.MongoClient(
    "Enter your Database link here ",
    server_api=ServerApi('1'))
db = client.test

countries = db.countries
continents = db.continents

###   Get all the countries where the letter or the word is in the name   ###
def search_by_query(name):
    for con in countries.find({'name': {"$regex": name, "$options": 'i'}}):
        print(con['name'])


###   Send list of continents with their number of countries   ###
def all_continents_and_countries():
    agg_pipeline = [
        {
            '$project': {
                'name': "$name",
                'countries': {'$size': "$countries"}}
        }
    ]
    cont = continents.aggregate(agg_pipeline)
    for continent in cont:
        print(continent)


###   Send back the fourth countries of a continent by alphabetical order   ###
def fourth_country():
    for continent in continents.find():
        for country_id in continent['countries']:
           countr = countries.find({'_id': ObjectId(country_id)}).sort("name")
           print(continent['name'],':',countr[0]['name'])

###   Get all countries ordered by the number of people   ###
def order_by_population():
    for con in countries.find({}).sort("population"):
        print("The country name is", con['name'], con['population'])



###   Get countries which have 'u' in their name and population greater than 100 000   ###
def search_by_name_and_order_by_population():
    for con in countries.find(
            {
                'name':
                    {'$regex': 'u', '$options': 'i'}, 'population': {'$gt': 100000}
            }
            ).sort("population"):
        print("The country name is", con['name'], con['population'])

if __name__ == '__main__:':
    search_by_query('Fr')  
    all_continents_and_countries()
    order_by_population()
    fourth_country()
    search_by_name_and_order_by_population()
