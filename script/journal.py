import json, logging
import requests, yaml
import asyncio
from datetime import datetime

#  ********** Configuration Section **********

#  *** Slack Configuration ***
with open('config/config.yaml', 'r') as file:
        config = yaml.safe_load(file)
slack_webhook = config['slack']['webhook']

#  *** Logging Configuration ***
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


#  ********** Functions Sections **********

#  *** Text to JSON Function ***
async def convert_to_json(input_string):
    lines = input_string.strip().split('\n')
    data = {}
    for line in lines:
        parts = line.split(':', 1)
        if len(parts) == 2:
            key = parts[0].strip()
            value = parts[1].strip()
            if key in data:
                if isinstance(data[key], list):
                    data[key].append(value)
                else:
                    data[key] = [data[key], value]
            else:
                data[key] = value

    # ** Convert the dictionary to JSON format and extract profile **
    json_data = json.dumps(data, indent=4)
    data = json.loads(json_data)
    org = data['COMPANY CONFORMED NAME']
    date = data['FILED AS OF DATE']
    datetime_object = datetime.strptime(date, "%Y%m%d")
    payload = f"On {date}, {org} reported cybersecutiy breach to SEC"
    await send_slack_message(payload)

#  *** Asynchronous function to send a message to Slack using a webhook ***
async def send_slack_message(text):
    payload = {"text": text}
    try:
        response = requests.post(slack_webhook, json=payload)
        response.raise_for_status()
        logger.info(f"Message sent successfully to Slack")
    except requests.RequestException as e:
        logger.error(f"Error sending message to Slack: {e}")


### If __name__ == __main__ ###
if __name__ == "__main__":
   asyncio.run(convert_to_json())
   
