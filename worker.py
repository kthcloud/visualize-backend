import time
import requests
import os
import env
import pymongo
import logger

def get_db_latest():
    timer = time.time()
    client = pymongo.MongoClient(env.read_env("MONGO_URL"))
    db = client["deploy"]
    collection = db["jobs"]
    jobs = collection.find({"$nor": [{"type": {"$regex": "repair"}}, {"status": {"$regex": "failed"}}]}).sort(
        "createdAt", -1).limit(10)
    logger.log("Time to fetch db: " + str(time.time() - timer))
    return list(jobs)


def get_status():
    timer = time.time()
    response = requests.get(
        f'{env.read_env("API_URL")}/landing/v2/status?n=100')
    logger.log("Time to fetch status: " + str(time.time() - timer))
    return response.json()


def get_capacities():
    timer = time.time()
    response = requests.get(
        f'{env.read_env("API_URL")}/landing/v2/capacities?n=1')
    logger.log("Time to fetch capacities: " + str(time.time() - timer))
    return response.json()


def get_stats():
    timer = time.time()
    response = requests.get(
        f'{env.read_env("API_URL")}/landing/v2/stats?n=1')
    logger.log("Time to fetch stats: " + str(time.time() - timer))
    return response.json()


def start(update_state):
    while True:
        update_state(get_status(), get_db_latest(),
                     get_capacities(), get_stats())
        logger.log("Fetched at " + time.strftime("%Y-%m-%d %H:%M:%S"))
        time.sleep(1)
