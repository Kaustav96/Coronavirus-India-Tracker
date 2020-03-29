# Coronavirus Slackbot+Telegram App
A Slackbot+Telegram bot that gives latest updates about confirmed COVID-19 cases in India, pulling the information from the website of the Indian Ministry of Health and Family Welfare (https://www.mohfw.gov.in/)

## Features
- Sit back and relax - the coronavirus updates will come to you.
- Get Slack notifications (picture below)
  -  New Corona Virus cases happening in India
  -  How many Indian nationals have Corona Virus per State?
  -  How many deaths happened per State?
  -  The new States entering the corona zone like Kerala
- Its reliable - the source of data is official Government site ([here](https://mohfw.gov.in/))
- Its ROBUST! 
  - What if script fails? What if the Govt website changes format?
  - You get Slack notifications about the exceptions too.
  - You have log files (check `bot.log`) too, to evaluate what went wrong
  
 
 ## Installation
- You need Python
- You need a Slack account + Slack Webhook to send slack notifications to your account
- You need a new bot in telegram to send notifications cross telegram also.
- Use the instructions here to generate the bot token and get the group id: https://dev.to/mddanishyusuf/build-telegram-bot-to-send-daily-notification-4i00
- Install dependencies by running
```bash
pip install tabulate
pip install requests
pip install python-telegram-bot
pip install beautifulsoup4
```
- Clone this repo and create auth.py
```bash
git clone https://github.com/Kaustav96/Coronavirus-India-Tracker.git
cd Coronavirus-India-Tracker
touch auth.py
```
- Write your Slack Webhook into auth.py
```python
DEFAULT_SLACK_WEBHOOK = 'https://hooks.slack.com/services/<your custome webhook url>'
```
- To schedule a job use Crontab or python schedule library.
