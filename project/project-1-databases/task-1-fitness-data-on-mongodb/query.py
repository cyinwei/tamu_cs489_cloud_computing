"""
Implements the MongoDB queries requested in Part B of Project 1 Task 1.

We first do two writes to the collection (fitness_myUIN).  See functions wq1,
w12.  Then we do some reads (and analysis with aggregations).  See functions
rq1 to rq4.
"""

import re
import pprint
from pymongo import MongoClient, UpdateOne
from config import HOST, DB, COLLECTION, DUMMY_FITNESS_DATA, USER_1001_DATA

def wq1(mongod_collection, batch_data=DUMMY_FITNESS_DATA):
    """
    Upserts the data from dummy_fitness data.
    """

    upserts = []
    for user in batch_data:
        query = {'uid': user['uid']}
        data = {'$setOnInsert': user}
        upserts.append(UpdateOne(query, data, upsert=True))

    return mongod_collection.bulk_write(upserts)


def wq2(mongod_collection, data=USER_1001_DATA):
    """
    Updates the data from the user1001 data.
    """

    query = {'uid': data['uid']}
    payload_data = {'$set': data}

    return mongod_collection.update_one(query, payload_data)

def rq1(mongod_collection):
    """
    Counts the number of user in the collection
    """

    # just in case we get an collection with a bad insert (without uid) into it
    query = {'uid': {'$exists': True}}

    return mongod_collection.count(query)

def rq2(mongod_collection):
    """
    Retrieves the employees with the tag of active.
    """

    query = {'tags': {'$in': ['active']}}
    return mongod_collection.find(query)

def _parse_goal(goal, amount):
    nums = re.findall(r'\d+', goal)

    # NOTE: just find one number.  Doesn't check for decimal numbers, or
    # advanced inputs like 50 min 30 sec.
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

def rq4(mongod_collection):
    """
    Aggregate total activity duration for all users.
    """

    pipeline = [
        {'$unwind': '$activityDuration'},
        {'$group': {'_id': '$uid', 'duration': {'$sum': '$activityDuration'}}},
        {'$sort': {'_id': 1} },
    ]

    return mongod_collection.aggregate(pipeline)

if __name__ == "__main__":
    print('CSCE 489-599 Cloud Computing: Project 1 Task 1.  Done by Charlie.')
    print('Does the queries outlined in part B.')
    print("Connecting to MongoDB at: {}".format(HOST))
    client = MongoClient(HOST)

    print("Connected.  Using db [{}] and collection [{}]".format(DB, COLLECTION))
    my_db = client[DB]
    my_collection = my_db[COLLECTION]

    print('----')
    print("Executing WQ1: Upserting data.")
    wq1_results = wq1(my_collection)
    print("Done.  Upsert bulk results:")
    pprint.pprint(wq1_results.bulk_api_result)

    print('----')
    print("Executing WQ2: Updating data.")
    wq2_results = wq2(my_collection)
    print("Done.  Update results:")
    print("Request update matched : {} documents (should be 1).".format(wq2_results.matched_count))

    print('----')
    print("Executing RQ1: Getting total employee count.")
    rq1_results = rq1(my_collection)
    print("Done.  Number of employees is {}.".format(rq1_results))

    print('----')
    print("Executing RQ2: Getting employees with the 'active' tag.")
    rq2_results = rq2(my_collection)
    print("Done.  Number of employees with the active tag is is {}.".format(rq2_results.count()))
    print("The detailed data is:")
    for employee in rq2_results:
        print('----')
        pprint.pprint(employee)

    print('----')
    print("Executing RQ3: Getting employees with a goal activity of over 60 min.")
    rq3_results = rq3(my_collection)
    print("Done.  Number of employees with is {}.".format(len(rq3_results)))
    print("The detailed data is:")
    for employee in rq3_results:
        print('----')
        pprint.pprint(employee)

    print('----')
    print("Executing RQ4: Aggregating the total activity duration of each employee.")
    rq4_results = rq4(my_collection)
    # print("Done.  Number of employees with is {}.".format(len(rq4_results)))
    print("The data is:")
    print("data types: _id is uid, duration is total activity")
    for employee in rq4_results:
        print('----')
        pprint.pprint(employee)

