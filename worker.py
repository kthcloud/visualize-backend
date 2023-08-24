import time
import requests
import os
import env
import pymongo
import logger

def get_db_latest():
    client = pymongo.MongoClient(env.read_env("MONGO_URL"))
    db = client["deploy"]
    collection = db["jobs"]
    # all the jobs that are not repair or failed or pending, sorted by createdAt, descending, limit 10
    jobs = collection.find({"$nor": [{"type": {"$regex": "repair"}}, {"status": {"$regex": "failed"}}, {"status": {"$regex": "terminated"}}, {"status": {"$regex": "pending"}}]}).sort(
        "createdAt", -1).limit(10)
    jobsList = list(jobs)
    client.close()
    return list(jobsList)


def get_status():
    response = requests.get(
        f'{env.read_env("API_URL")}/landing/v2/status?n=100')
    return response.json()


def get_capacities():
    response = requests.get(
        f'{env.read_env("API_URL")}/landing/v2/capacities?n=1')
    return response.json()


def get_stats():
    response = requests.get(
        f'{env.read_env("API_URL")}/landing/v2/stats?n=1')
    return response.json()


def start(update_state):
    while True:
        update_state(get_status(), get_db_latest(),
                     get_capacities(), get_stats())
        logger.log("Fetched at " + time.strftime("%Y-%m-%d %H:%M:%S"))
        time.sleep(0.1)
