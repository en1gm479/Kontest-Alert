import os
import json
import requests
from bs4 import BeautifulSoup, SoupStrainer
import pytz
from datetime import datetime
import smtplib
import ssl
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
}

def utc_to_time(naive, timezone="Asia/Kolkata"):
    return naive.replace(tzinfo=pytz.utc).astimezone(pytz.timezone(timezone))


def codeforce_contest_scrapper():
    codeforce_contest_url = "https://codeforces.com/api/contest.list"
    res = requests.get(codeforce_contest_url,headers=headers)

    json_data = (json.loads(res.content))
    cf_contest = []
    upcoming_cf_contest = ""

    for data in json_data["result"]:
        if (data['phase'] != "BEFORE"):
            break
        cf_contest.append(data)
    upcoming_cf_contest+="###############################\n"
    upcoming_cf_contest+="# Upcoming Codeforce Contests #\n"
    upcoming_cf_contest+="###############################\n\n"
    upcoming_cf_contest+="=========================================================\n"


    for data in cf_contest:
        upcoming_cf_contest += f"Id: {data['id']}\n"
        upcoming_cf_contest += f"Name: {data['name']}\n"
        upcoming_cf_contest += f"Type: {data['type']}\n"
        upcoming_cf_contest += f"Link: https://codeforces.com/contests/{data['id']}\n"

        time_sec = data['durationSeconds']
        day = divmod(time_sec, 86_400)
        hour = divmod(day[1], 3_600)
        min = divmod(hour[1], 60)
        sec = min[1]
        upcoming_cf_contest += f"Duration: {day[0]} days, {hour[0]} hours, {min[0]} mins\n"
        start_time = (datetime.utcfromtimestamp(data['startTimeSeconds']))
        upcoming_cf_contest += f"Start time: {utc_to_time(start_time).strftime('%d-%m-%Y %H:%M:%S')}\n"
        upcoming_cf_contest += f"=========================================================\n"

    return upcoming_cf_contest

def codechef_contest_scrapper():
    ongoing_cc_contests = ""
    completed_cc_contests = ""
    upcoming_cc_contests = ""

    html = requests.get(f'https://www.codechef.com/api/list/contests/all?sort_by=START&sorting_order=asc',headers=headers).text
    soup = BeautifulSoup(html, 'html.parser')
    all_cc_contests = json.loads(soup.text)

    upcoming_cc_contests+="##############################\n"
    upcoming_cc_contests+="# Upcoming Codechef Contests #\n"
    upcoming_cc_contests+="##############################\n\n"
    upcoming_cc_contests+="=========================================================\n"
    # print(all_cc_contests)
    for contest in all_cc_contests['present_contests']:
        ongoing_cc_contests+=f"Code: {contest['contest_code']}\n"
        ongoing_cc_contests+=f"Name: {contest['contest_name']}\n"
        ongoing_cc_contests+=f"Status: Currently Running\n"
        ongoing_cc_contests+=f"Start time: {contest['contest_start_date']}\n"
        ongoing_cc_contests+=f"Link: https://www.codechef.com/{contest['contest_code']}\n"
        ongoing_cc_contests+="=========================================================\n"

    for contest in all_cc_contests['future_contests']:
        upcoming_cc_contests+=f"Code: {contest['contest_code']}\n"
        upcoming_cc_contests+=f"Name: {contest['contest_name']}\n"
        upcoming_cc_contests+=f"Start time: {contest['contest_start_date']}\n"
        time_sec = int(contest['contest_duration'])
        day = divmod(time_sec, 1440)
        hour = divmod(day[1], 60)
        min = hour[1]
        upcoming_cc_contests+=f"Duration: {day[0]} days, {hour[0]} hours, {min} mins\n"
        upcoming_cc_contests+=f"Link: https://www.codechef.com/{contest['contest_code']}\n"
        upcoming_cc_contests+="=========================================================\n"
        
    # for contest in all_cc_contests['past_contests']:
    #     completed_cc_contests+=f"Code: {contest['contest_code']}\n"
    #     completed_cc_contests+=f"Name: {contest['contest_name']}\n"
    #     completed_cc_contests+=f"Start time: {contest['contest_start_date']}\n"
    #     time_sec = int(contest['contest_duration'])
    #     day = divmod(time_sec, 1440)
    #     hour = divmod(day[1], 60)
    #     min = hour[1]
    #     completed_cc_contests+=f"Duration: {day[0]} days, {hour[0]} hours, {min} mins\n"
    #     completed_cc_contests+=f"Link: https://www.codechef.com/{contest['contest_code']}\n"
    #     completed_cc_contests+="=================================\n"

    return {
        'ongoing_cc_contests': ongoing_cc_contests,
        'upcoming_cc_contests': upcoming_cc_contests,
        'completed_cc_contests': completed_cc_contests
    }


def leetcode_contest_scrapper():
    html = requests.get(f'https://leetcode.com/contest/',headers=headers)
    soup = BeautifulSoup(html.content, 'html.parser')

    # all_lc_contests = json.loads(soup.text)
    # print(all_lc_contests)
    # top2contest = all_lc_contests["pageProps"]["dehydratedState"]["queries"][4]["state"]["data"]["topTwoContests"]
    # print(top2contest)
    
    future_lc_contests = ""
    future_lc_contests+="##############################\n"
    future_lc_contests+="# Upcoming Leetcode Contests #\n"
    future_lc_contests+="##############################\n\n"
    future_lc_contests+="=========================================================\n"
    # future_lc_contests+="~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n"

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
        future_lc_contests += f"=========================================================\n"

    return future_lc_contests


# print(codeforce_contest_scrapper())
# print(codechef_contest_scrapper()['upcoming_cc_contests'])
# print(leetcode_contest_scrapper())
def sendmail():
    email_sender = os.getenv("email_sender")
    email_password = os.getenv("email_password")
    email_receiver = os.getenv("email_receiver")

    subject = 'Check out the Upcoming Codeforce contests'
    body = f"{codeforce_contest_scrapper()}\n{codechef_contest_scrapper()['upcoming_cc_contests']}\n{leetcode_contest_scrapper()}"

    # print(body)

    # file2write=open("sample.txt",'w')
    # file2write.write(body)
    # file2write.close()

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())


if __name__ == "__main__":
    sendmail()
