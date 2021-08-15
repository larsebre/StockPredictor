import requests
import putenv
import os

def send_slack_message(message):
    payload = '{"text":"%s"}' % message
    URL = putenv.os.getenv('SLACK_URL')
    response = requests.post(URL, data=payload)

if __name__ == "__main__":
    send_slack_message("Hello!!")