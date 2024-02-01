import requests
import json
from bs4 import BeautifulSoup, SoupStrainer
import pytz
from datetime import datetime


def utc_to_time(naive, timezone="Asia/Kolkata"):
    return naive.replace(tzinfo=pytz.utc).astimezone(pytz.timezone(timezone))

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
}


html = requests.get(f'https://leetcode.com/_next/data/1OUy1uaI_fNDMZpVCXpR_/contest.json',headers=headers).text
soup = BeautifulSoup(html, 'html.parser')

all_contests = json.loads(soup.text)
top2contest = all_contests["pageProps"]["dehydratedState"]["queries"][4]["state"]["data"]["topTwoContests"]

future_contests = ""
for contest in top2contest:
    future_contests+=f"Name: {contest['title']}\n"
    start_time = (datetime.utcfromtimestamp(contest['startTime']))
    future_contests+=f"Start time: {utc_to_time(start_time).strftime('%d-%m-%Y %H:%M:%S')}\n"
    # future_contests+=f"Start time: {contest['startTime']}\n"
    time_sec = int(contest['duration'])
    day = divmod(time_sec, 86_400)
    hour = divmod(day[1], 3_600)
    min = divmod(hour[1], 60)
    sec = min[1]
    future_contests+=f"Duration: {day[0]} days, {hour[0]} hours, {min[0]} mins\n"
    future_contests+=f"Link: https://leetcode.com/contest/{contest['titleSlug']}\n"
    future_contests+="=================================\n"

print(future_contests)