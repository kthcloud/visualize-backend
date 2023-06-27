import time
import requests
import os
import env
import pymongo


def get_db_latest():
    client = pymongo.MongoClient(env.read_env("MONGO_URL"))
    db = client["deploy"]
    collection = db["jobs"]
    jobs = collection.find({"type": {"$not": {"$regex": "repair"}}}).sort(
        "createdAt", -1).limit(10)
    return list(jobs)


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
        time.sleep(1)
