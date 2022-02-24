# Author: Hayley Leavitt
# Title: Weather Scraper
# Description: Weather Scraper is a simple web scraper that collects weather data from Google
#       - I have the location set to Corvallis, Oregon as a default, but you can do a google search for a different
#         location and change it to whatever you'd like by copying and pasting the google search URL into the
#         URL variable.
# Dependencies: In order to run Weather Scraper, you will need to install Beautiful Soup and requests
#       - If you are using the PyCharm IDE, you can simply click on the red squiggle and select "install package"
#         to resolve the issue.
#       - Otherwise, you'll need to run these through pip in a terminal, likely best to use a virtual environment

from bs4 import BeautifulSoup as bs
import requests
import argparse

# Browser info
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " \
             "AppleWebKit/537.36 (KHTML, like Gecko) " \
             "Chrome/94.0.4606.81 Safari/537.36"
# US english
LANGUAGE = "en-US,en;q=0.5"


def get_weather_data(url):
    """
    get_weather_data() is the weather scraping portion of Weather Scraper. It takes in "url" as its variable to go
    scrape the web with and stores it in a dictionary named "result"
    :param url:
    :return result:
    """
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    html = session.get(url)

    # create a new soup
    soup = bs(html.text, "html.parser")

    # store all results to this dictionary
    result = {'region': soup.find("div", attrs={"id": "wob_loc"}).text,
              'temp_now': soup.find("span", attrs={"id": "wob_tm"}).text,
              'dayhour': soup.find("div", attrs={"id": "wob_dts"}).text,
              'weather_now': soup.find("span", attrs={"id": "wob_dc"}).text,
              'precipitation': soup.find("span", attrs={"id": "wob_pp"}).text,
              'humidity': soup.find("span", attrs={"id": "wob_hm"}).text,
              'wind': soup.find("span", attrs={"id": "wob_ws"}).text}

    return result


def convertToText(dict):
    location = "Current Weather for: " + str(dict["region"])
    time = "Time: " + str(dict["dayhour"])
    temperature = f"Temperature now: {dict['temp_now']}°F"
    description = "Description: " + str(dict['weather_now'])
    precipitation = "Precipitation: " + str(dict["precipitation"])
    humidity = "Humidity: " + str(dict["humidity"])
    wind = "Wind: " + str(dict["wind"])

    message = [location, time, temperature, description, precipitation, humidity, wind]
    with open('WeatherData.txt', 'w') as f:
        for line in message:
            f.write(line)
            f.write('\n')


if __name__ == "__main__":
    # URL for Corvallis Oregon
    URL = "https://www.google.com/search?q=corvallis+oregon+weather&rlz=1C5CHFA_enUS983US983&oq=corvallis+oregon+" \
          "weather&aqs=chrome..69i57j0i512l2j0i457i512j0i512l6.3864j1j15&sourceid=chrome&ie=UTF-8"

    parser = argparse.ArgumentParser(description="Quick Script for Extracting Weather data using Google Weather")
    parser.add_argument("region", nargs="?", help="""Region to get weather for, must be available region.
                                        Default is your current location determined by your IP Address""", default="")
    # parse arguments
    args = parser.parse_args()
    region = args.region
    URL += region

    # get data
    data = get_weather_data(URL)
    convertToText(data)
