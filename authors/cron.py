import requests
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl
import re
from pathlib import Path
from .utils.SteamGroup import steamgroup
from .models import Author

BASE_DIR = Path(__file__).resolve().parent.parent

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def update_steamids():
    # use the SteamGroup.py module to fetch the SteamID64's of all the Steam group members and save them to steamids.txt
    members = steamgroup.get_steam_ids()
    fhand = open(BASE_DIR / 'authors/steamids.txt', 'w')
    for member in members:
        fhand.write(str(member) + '\n')
    fhand.close()


def update_author_table():
    # remove everything from the Author table before populating it again
    Author.objects.all().delete()
    # iterate over each line in steamids.txt file
    # and make a request using the Steam API and BeautifulSoup to get all the necessary data about each author
    fhand = open(BASE_DIR / 'authors/steamids.txt', 'r')
    for steamid in fhand:
        # first of all find out how many followers and Portal 2 map submissions an author have
        try:
            url = 'https://steamcommunity.com/profiles/' + steamid.replace('\n', '') + '/myworkshopfiles?appid=620'
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'}) # trick the server into thinking that the request is made from a genuine browser
            html = urllib.request.urlopen(req, context=ctx).read()
            soup = BeautifulSoup(html, 'html.parser')
            followers = int(soup.find_all('div', class_='followStat')[0].text.replace(',', '')) # in case there is a comma remove it
            submissions = soup.find_all('div', class_='workshopBrowsePagingInfo')
            if len(submissions) > 0:
                # extract all numerical characters from text
                numerical_characters = re.findall('[0-9]+', submissions[0].text)
                submissions = int(numerical_characters[-1])
            else:
                submissions = 0
        except:
            # if something goes wrong with the request just skip it by setting the followers variable to 0
            followers = 0
        # if an author has at least 5 followers and 1 submission related to Portal 2, extract additional info using the Steam api and add them to the database
        if followers > 5 and submissions > 0:
            create_author(steamid, followers, submissions)


def create_author(steamid, followers, submissions):
    try:
        author = requests.get('https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key=0E167006C0EE4A1C3CD518D4944D47B1&steamids=' + steamid).json()['response']['players'][0]
        Author.objects.create(
            nicname=author['personaname'],
            avatar=author['avatar'],
            profile_url=author['profileurl'],
            loc_country_code=author.get('loccountrycode', '-'),
            number_of_followers=followers,
            workshop_submissions=submissions
        )
    except:
        pass
