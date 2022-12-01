import time
import pytz
import datetime
import requests
import json
from dotenv import dotenv_values

CONFIG = {}

local = None
finished = False

ACCESS_TOKEN = dotenv_values(".env")["ACCESS_TOKEN"]
BASE_URL = dotenv_values(".env")["BASE_URL"]

CHALLENGES_PATH = "/challenges"
SCORE_PATH = "/scoreboard"

schedules = []

def loadSettings():
    global local
    try:
        with open("config.json", "r") as f:
            CONFIG.update(json.load(f))
    except:
        # prompt user to create config file and exit
        print("Error: config.json file not found")
        exit()
    
    local = pytz.timezone(CONFIG["timezone"])

def get_schedule():
    global schedules

    now = datetime.datetime.now(local)
    schedules = CONFIG["schedules"]
    
    for schedule in schedules:
        release_time = datetime.datetime.strptime(schedule["release_time"], "%Y-%m-%dT%H:%M:%S%z")
        if release_time <= now:
            if "released" not in schedule:
                schedule["released"] = False

            if not schedule["released"]:
                return schedule
    return None


def release_challenges():
    start_time = datetime.datetime.strptime(CONFIG["start_time"], "%Y-%m-%dT%H:%M:%S%z")
    end_time = datetime.datetime.strptime(CONFIG["end_time"], "%Y-%m-%dT%H:%M:%S%z")

    # if not between start and end time, return
    now = datetime.datetime.now(local)
    if now < start_time:
        return

    if now > end_time:
        global finished
        if not finished:
            print("== Competition has ended ==")
            finished = True

            for schedule in CONFIG["schedules"]:
                set_challenges_visibility(schedule, False)
        return

    schedule = get_schedule()
    if schedule:
        max_score = get_max_score()
        if max_score >= schedule["minimum_score"]:
            schedule["released"] = True
            set_challenges_visibility(schedule, True)


def set_challenges_visibility(schedule, is_visible):
    for challenge in schedule["challenges"]:
        try:
            now = datetime.datetime.now(local)
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

            response = set_challenge_visibility(challenge, is_visible)

            chall_name = response.json()['data']['name']
            if is_visible:
                print(f"[+][{dt_string}] Released {chall_name}")
            else:
                print(f"[-][{dt_string}] Hid {chall_name}")
        except Exception as e:
            print(e)
            print(f"Failed to release challenge {challenge}")

def set_challenge_visibility(challenge, is_visible):
    visibility = "visible" if is_visible else "hidden"
    response = requests.patch(
        BASE_URL + CHALLENGES_PATH + f"/{challenge}", 
        json = {"state": f"{visibility}"},
        headers={"Authorization": f"Bearer {ACCESS_TOKEN}"}
    )
    return response

def get_max_score():
    response = requests.get(
        BASE_URL + SCORE_PATH,
        json={},
        headers={"Authorization": "Bearer " + ACCESS_TOKEN}
    )
    max_score = 0
    scoreboards = response.json()["data"]
    for scoreboard in scoreboards:
        if scoreboard["score"] > max_score:
            max_score = scoreboard["score"]
    return max_score

def main():
    print("== CTFd Challenge Release Time Script ==")
    loadSettings()
    while True:
        release_challenges()
        time.sleep(60)

if __name__ == "__main__":
    main()
