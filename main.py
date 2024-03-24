import requests
import re
from bs4 import BeautifulSoup
import datetime

# Defining the URL and headers
url = "https://www.sec.gov/cgi-bin/current?q1=0&q2=4&q3="
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

# Defining the regex pattern to extract the 8k filings
pattern = r"/Archives/edgar/data/\d+/\d+-\d+-\d{6}"

# Set the timeout for the request (in seconds)
timeout = 10  # Timeout value (adjust as needed)


# Main sends the GET request with the headers and timeout
def main():
  try:
    response = requests.get(url, headers=headers, timeout=timeout)

    # Check if the request was successful
    if response.status_code == 200:
      # Parse the HTML content of the response using BeautifulSoup
      soup = BeautifulSoup(response.content, "html.parser")

      # Parseing HTML content using BeautifulSoup methods to find all links pattern
      links = soup.find_all("a")
      for link in links:
        match = re.search(pattern, link.get("href"))
        if match != None:
          #print(match.group(0))
          record_filings(match.group(0))
    else:
      print("Failed to fetch data. Status code:", response.status_code)
  except requests.Timeout:
    print("Request timed out. Please try again later.")
  except requests.RequestException as e:
    print("An error occurred:", e)


def record_filings(data):
  # Get today's date
  today = datetime.date.today()

  # Extract the year, month, and day from the date
  date_format = today.strftime("%Y-%m-%d")

  # Create file name on the basis of date
  file_name = f"{date_format}.txt"

  # Write entry to file
  with open(file_name, "a") as file:
    file.write(data + "\n")
    print(data)
    file.close()


main()
