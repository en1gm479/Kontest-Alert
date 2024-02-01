import requests
import json
from bs4 import BeautifulSoup, SoupStrainer

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
}

present_cf_contest = ""
past_contests = ""
future_contests = ""

html = requests.get(f'https://www.codechef.com/api/list/contests/all?sort_by=START&sorting_order=asc',headers=headers).text
soup = BeautifulSoup(html, 'html.parser')

all_contests = json.loads(soup.text)
print("\t\t\t\t\t\tUpcoming Codechef Contests:")
print("\t\t\t\t\t~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

# print(all_contests['future_contests'][0])

for contest in all_contests['present_contests']:
    present_cf_contest+=f"Code: {contest['contest_code']}\n"
    present_cf_contest+=f"Name: {contest['contest_name']}\n"
    present_cf_contest+=f"Status: Currently Running\n"
    present_cf_contest+=f"Start time: {contest['contest_start_date']}\n"
    present_cf_contest+=f"Link: https://www.codechef.com/{contest['contest_code']}\n"
    present_cf_contest+="=================================\n"

for contest in all_contests['future_contests']:
    # print(contest['contest_code'])
    future_contests+=f"Code: {contest['contest_code']}\n"
    future_contests+=f"Name: {contest['contest_name']}\n"
    future_contests+=f"Start time: {contest['contest_start_date']}\n"
    time_sec = int(contest['contest_duration'])
    day = divmod(time_sec, 1440)
    hour = divmod(day[1], 60)
    min = hour[1]
    future_contests+=f"Duration: {day[0]} days, {hour[0]} hours, {min} mins\n"
    future_contests+=f"Link: https://www.codechef.com/{contest['contest_code']}\n"
    future_contests+="=================================\n"
    
for contest in all_contests['past_contests']:
    past_contests+=f"Code: {contest['contest_code']}\n"
    past_contests+=f"Name: {contest['contest_name']}\n"
    past_contests+=f"Start time: {contest['contest_start_date']}\n"
    time_sec = int(contest['contest_duration'])
    day = divmod(time_sec, 1440)
    hour = divmod(day[1], 60)
    min = hour[1]
    past_contests+=f"Duration: {day[0]} days, {hour[0]} hours, {min} mins\n"
    past_contests+=f"Link: https://www.codechef.com/{contest['contest_code']}\n"
    past_contests+="=================================\n"

print("*****************\nPresent Contests\n*****************\n\n=================================")
print(present_cf_contest)
print("****************\nFuture Contests\n****************\n\n=================================")
print(future_contests)
print("***************\nPast Contest\n***************\n\n=================================")
print(past_contests)