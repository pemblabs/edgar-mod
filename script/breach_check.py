import requests, yaml
from bs4 import BeautifulSoup
from . import journal
import datetime, asyncio

#  ********** Configuration Section **********

#  *** Declaring Global Variables and Headers ***
with open('config/config.yaml', 'r') as file:
        config = yaml.safe_load(file)
        
path = config['build']['path']
ext = config['build']['ext']
parsers = ["html.parser", "lxml", "html5lib"]
soup = ""
headers = {
        "sec-ch-ua":
        "\"Chromium\";v=\"122\", \"Not(A:Brand\";v=\"24\", \"Google Chrome\";v=\"122\"",
        "sec-ch-ua-mobile":
        "?0",
        "sec-ch-ua-platform":
        "\"Windows\"",
        "upgrade-insecure-requests":
        "1",
        "Referrer-Policy":
        "strict-origin-when-cross-origin",
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"
}


#  ********** Functions Sections **********

#  *** Breach Report Scan ***
async def scan(url):
    url = path + str(url) + ext
    await asyncio.gather(save_entry(url))
    response = requests.get(url, headers=headers)
    #  ** Check if the request was successful **
    if response.status_code == 200:
      for parser in parsers:
        try:
            soup = BeautifulSoup(response.content, parser)
            break
        except:
            print(f"Failed to parse: {parser}")
    # ** Extract content and check for conditions **
      sec_header_tag = soup.find("sec-header")
      try:
        sec_header_text = sec_header_tag.get_text()
        if "ITEM INFORMATION:" in sec_header_text and "1.05" in sec_header_text:
          await journal.convert_to_json(sec_header_text.strip())
        else:
          print("***** No Brech Reported *****")
      except requests.RequestException as e:
        print("An error occurred:", e)
  

#  *** Saving Today's Entry to a File  ***
async def save_entry(data): # Considering using a relational database in the future
  today = datetime.date.today()
  date_format = today.strftime("%Y-%m-%d")
  file_name = f"{date_format}.txt"
  with open(file_name, "a") as file:
    file.write(data + "\n")
  
# *** Scan Completed ***
async def complete():
  task1 = [scan(url)]
  task2 = [journal.send_slack_message("All Scan Completed")]
  await asyncio.gather(task1, task2) 


### If __name__ == __main__ ###
if __name__ == "__main__":
   asyncio.run(complete())
   
  