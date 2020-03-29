import requests
from bs4 import BeautifulSoup
import json
import logging
import schedule
import time
from datetime import datetime
from slack_client import slacker
from telegram_client import send_notification
from tabulate import tabulate

SHORT_HEADERS = ['Sno', 'State', 'Indian', 'Foreign', 'Cured', 'Death']
FORMAT = '[%(asctime)-15s] %(message)s'
NEW_FILE_NAME = 'corona_india_data.json'

logging.basicConfig(format=FORMAT, level=logging.DEBUG, filename='bot.log', filemode='a')
current_time = datetime.now().strftime('%d/%m/%Y %H:%M')


def save_json(x):
    data = []

    for i in range(len(x)):
        state_id, state_name, indian, foreign, cured, death = x[i][0], x[i][1], x[i][2], x[i][3], x[i][4], x[i][5]
        data.append({'Data': {'Sno': state_id, 'Name': state_name, 'Indian': indian, 'Foreign': foreign, 'Cured': cured,
                              'Death': death}})
    with open(NEW_FILE_NAME, 'w+') as f:
        if len(f.read()) == 0:
            f.write(json.dumps(data))
        else:
            f.write(',\n' + json.dumps(data))


def load():
    with open(NEW_FILE_NAME, 'r') as f:
        res = json.load(f)
    return res


try:
    def main_work():
        info = []
        res = requests.get('https://www.mohfw.gov.in/')
        soup = BeautifulSoup(res.text, 'html.parser')

        stats = []

        try:
            my_data_str = ''
            last_data_updated = soup.find_all('strong')[0].get_text()
            last_data_updated = last_data_updated.replace("*", "")
            last_data_updated = last_data_updated.replace("awaited", "updated")

            for tr in soup.find_all('tbody')[9].find_all('tr'):
                my_data_str += tr.get_text()
            my_data_str = my_data_str[1:]
            stateList = my_data_str.split("\n\n")
            name_state_list = []
            # current data
            sum_ind, sum_foreign, sum_cured, sum_death, total_ind, total_foreign, total_cured, total_death = 0, 0, 0, \
                                                                                                             0, 0, 0, \
                                                                                                             0, 0

            for state in stateList[0:len(stateList) - 5]:
                data_list = state.split('\n')

                state_id, state_name, total_ind, total_foreign, total_cured, total_death = data_list[0], data_list[1], \
                                                                                           data_list[2], data_list[3], \
                                                                                           data_list[4], data_list[5]
                name_state_list.append(data_list[1])
                sum_ind += int(total_ind)
                sum_foreign += int(total_foreign)
                sum_cured += int(total_cured)
                sum_death += int(total_death)
                stats.append([state_id, state_name, total_ind, total_foreign, total_cured, total_death])
            stats.append(['', 'Total Number of Confirmed Cases in India', sum_ind, sum_foreign, sum_cured, sum_death])
            name_state_list.append('Total Number of Confirmed Cases in India')
            past_data = load()

            # past data
            count = 0
            for item in past_data:
                if item['Data']['Name'] not in name_state_list:
                    name = item['Data']['Name']
                    print(f'New State - {name} got corona virus.')
                else:
                    past_ind, past_for, past_cur, past_death = item['Data']['Indian'], item['Data']['Foreign'], \
                                                               item['Data']['Cured'], item['Data']['Death']
                    cur_ind, cur_for, cur_cur, cur_death = stats[count][2], stats[count][3], stats[count][4], \
                                                           stats[count][5]

                    state_name = item['Data']['Name']
                    past_str, cur_str = '', ''
                    if past_ind != cur_ind:
                        past_str += str(past_ind) + ','
                        cur_str += str(cur_ind) + ','
                    if past_for != cur_for:
                        past_str += str(past_for) + ','
                        cur_str += str(cur_for) + ','
                    if past_cur != cur_cur:
                        past_str += str(past_cur) + ','
                        cur_str += str(cur_cur)+ ','
                    if past_death != cur_death:
                        past_str += str(past_death)
                        cur_str += str(cur_death)
                    if len(past_str) > 0 and len(cur_str) > 0:
                        info.append(f'Change for {state_name}: [{past_str}]->[{cur_str}]')
                    count = count + 1

            save_json(stats)
            table = tabulate(stats, headers=SHORT_HEADERS, tablefmt='psql')

            # print(table1)
            events_info = ''
            for event in info:
                logging.warning(event)
                events_info += '\n - ' + event.replace("'", "")
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            print('Sent corona-virus update to the Slack App - ', dt_string)
            slack_text = f'Please find CoronaVirus Summary for India below:\n{last_data_updated}\n{events_info}\n```{table}```'
            slacker()(slack_text)
            print('Sent corona-virus update to the Telegram App - ', dt_string)
            send_notification(slack_text)
        except Exception as err:
            slacker()(f'Exception occurred: [{err}]')
            send_notification(f'Exception occurred: [{err}]')
            print(f'Exception occurred  {err}')


    main_work()
except Exception as e:
    slacker()(f'Exception occurred: [{e}]')
    send_notification(f'Exception occurred: [{e}]')
    print(f'Exception occurred {e}')

# schedule.every().day.at("10:30").do(main_work)
# schedule.every().day.at("20:00").do(main_work)
schedule.every(10).minutes.do(main_work)

while True:
    # Checks whether a scheduled task
    # is pending to run or not
    # print("Current time ran job at - ",time.time())
    schedule.run_pending()
    time.sleep(1)
