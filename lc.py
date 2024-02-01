import json
import requests
from bs4 import BeautifulSoup, SoupStrainer
import pytz
from datetime import datetime


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
}

def leetcode_contest_scrapper():
    html = requests.get(f'https://leetcode.com/contest/',headers=headers)
    soup = BeautifulSoup(html.content, 'html.parser')

    future_lc_contests = ""
    future_lc_contests+="##############################\n"
    future_lc_contests+="# Upcoming Leetcode Contests #\n"
    future_lc_contests+="##############################\n\n"
    future_lc_contests+="=====================================\n"

    top2contest = soup.findAll('div', attrs = {'class':'swiper-wrapper'})

    for ele in top2contest[0]:
        contest = [list(el.findChildren()) for el in ele.div.a]
        contest_name = contest[1][3].text
        contest_date = contest[1][4].text
        future_lc_contests += f"Code: {contest_name.split()[-1]}\n"
        future_lc_contests += f"Name: {contest_name}\n"
        future_lc_contests += f"Start time: {contest_date}\n"
        future_lc_contests += f"Duration: 1 hours, 30 mins\n"
        future_lc_contests += f"Link: https://leetcode.com/contest/{'-'.join((contest_name.lower().split()))}\n"
        future_lc_contests += f"=====================================\n"

    return future_lc_contests
    # all_lc_contests = json.loads(soup.text)
    # print(all_lc_contests)
    # top2contest = all_lc_contests["pageProps"]["dehydratedState"]["queries"][4]["state"]["data"]["topTwoContests"]
    # print(top2contest)


print(leetcode_contest_scrapper())
# time = int("2:30 AM UTC")
# start_time = (datetime.utcfromtimestamp(time))
# print(start_time)