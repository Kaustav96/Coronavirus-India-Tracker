import requests
import json
from auth import DEFAULT_SLACK_WEBHOOK

HEADERS = {
    'Content-type': 'application/json'
}


def slacker(webhook_url=DEFAULT_SLACK_WEBHOOK):
    def slackit(msg):
        payload = {'text': msg}

        return requests.post(webhook_url, headers=HEADERS, data=json.dumps(payload))
    return slackit
