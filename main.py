import requests, yaml
from bs4 import BeautifulSoup
from script import breach_check
import asyncio, re

#  ********** Configuration Section **********

#  *** Defining the URL and headers ***
with open('config/config.yaml', 'r') as file:
        config = yaml.safe_load(file)

url = config['endpoint']['query']
headers = {
    "sec-ch-ua":
    "\"Chromium\";v=\"122\", \"Not(A:Brand\";v=\"24\", \"Google Chrome\";v=\"122\"",
    "sec-ch-ua-mobile":
    "?0",
    "sec-ch-ua-platform":
    "\"Windows\"",
    "upgrade-insecure-requests":
    "1",
    "Referer":
    "https://www.sec.gov/edgar/searchedgar/currentevents",
    "Referrer-Policy":
    "strict-origin-when-cross-origin",
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"
}

#  *** Defining Pattern and Global Variable ***
pattern = config['regex']['pattern']
filings = [""]


#  ********** Functions Sections **********

#  *** Main function sends the GET request ***
def main() -> None:
  try:
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
      soup = BeautifulSoup(response.content, "html.parser")
      links = soup.find_all("a")
      # ** Retrieves links to all fillings and appends to a list **
      for link in links:
        match = re.search(pattern, link.get("href"))
        if match != None:
          filings.append((match.group(0)))
    else:
      print("Failed to fetch data. Status code:", response.status_code)
  except requests.Timeout:
    print("Request timed out. Please try again later.")
  except requests.RequestException as e:
    print("An error occurred:", e)
  # ** Calls breach_check.scan **
  [asyncio.run(breach_check.scan(line)) for line in filings]


main()
