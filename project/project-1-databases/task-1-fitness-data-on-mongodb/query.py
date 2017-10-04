"""
queries
"""

from pathlib import Path
import json
import re
from bson.code import Code
from pymongo import MongoClient, UpdateOne

host = "34.233.78.56"
db = "fitness_721008432"
collection = "fitness_721008432"
test_collection = "test"

dummy_fitness_file = Path('data/dummy-fitness.json')
user_1001_file = Path('data/user1001-new.json')

with dummy_fitness_file.open('r') as f:
    dummy_fitness_data = json.load(f)
with user_1001_file.open('r') as f:
    user_1001_data = json.load(f)

client = MongoClient(host)

my_db = client[db]
my_collection = my_db[test_collection]

def wq1(mongod_collection, batch_data=dummy_fitness_data):
    """
    Upserts the data from dummy_fitness data.
    """

    upserts = []
    for user in batch_data:
        query = {'uid': user['uid']}
        data = {'$setOnInsert': user}
        upserts.append(UpdateOne(query, data, upsert=True))

    return mongod_collection.bulk_write(upserts)

result_wq1 = wq1(my_collection)
# print(result.bulk_api_result)

def wq2(mongod_collection, data=user_1001_data):
    """
    Updates the data from the user1001 data.
    """

    query = {'uid': data['uid']}
    payload_data = {'$set': data}

    return mongod_collection.update_one(query, payload_data)

result_wq2 = wq2(my_collection)
# print(result_wq2.matched_count)

def rq1(mongod_collection):
    """
    Counts the number of user in the collection
    """

    # just in case we get an collection with a bad insert (without uid) into it
    query = {'uid': {'$exists': True}}

    return mongod_collection.count(query)

result_rq1 = rq1(my_collection)
# print(result_rq1)

def rq2(mongod_collection):
    """
    Retrieves the employees with the tag of active.
    """

    query = {'tags': {'$in': ['active']}}
    return mongod_collection.find(query)

#for doc in rq2(my_collection):
#   print(doc)

def _parse_goal(goal, amount):
    # https://stackoverflow.com/questions/4289331/python-extract-numbers-from-a-string
    nums = re.findall(r'\d+', goal)
    if len(nums) == 1:
        if int(nums[0]) > amount:
            return True
    return False

def rq3(mongod_collection):
    """
    Retrieves the employees that have a goal activity of over 60 min.
    """

    query = {'goal.activityGoal' : {'$exists': True}}
    all_goal_activity = mongod_collection.find(query)
    filtered_results = [doc for doc in all_goal_activity if _parse_goal(doc['goal']['activityGoal'], 60)]

    return filtered_results

# for doc in rq3(my_collection):
    # print(doc)

import pprint

def rq4(mongod_collection):
    """
    Aggregate total activity duration for all users.
    """

    pipeline = [
        {'$unwind': '$activityDuration'},
        {'$group': {'_id': None, 'duration': {'$sum': '$activityDuration'}}}
    ]

    return mongod_collection.aggregate(pipeline)

pprint.pprint(list(rq4(my_collection)))

