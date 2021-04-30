import requests
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl
import re
from pathlib import Path
from .utils.SteamGroup import steamgroup
from .models import Author, Steamid

BASE_DIR = Path(__file__).resolve().parent.parent

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def make_request(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(req, context=ctx).read()
    return BeautifulSoup(html, 'html.parser')



def update_authors_steamid_table():
    # make a backup before deleting everything
    steamids = list(Steamid.objects.all())
    # delete everything from the authors_steamid table before populating it again
    Steamid.objects.all().delete()
    try:
        # use the SteamGroup.py module to fetch the SteamID64's of all the Steam group members and save them to authors_steamid table
        members = steamgroup.get_steam_ids()
        objects = [Steamid(steamid=member) for member in members]
        Steamid.objects.bulk_create(objects)
    except:
        # in case something goes wrong populate it from backup
        objects = [Steamid(steamid=item.steamid) for item in steamids]
        Steamid.objects.bulk_create(objects)



def update_authors_author_table():
    # remove everything from the authors_author table before populating it again
    Author.objects.all().delete()
    # load all steamids into a list
    steamids = list(Steamid.objects.all())
    # iterate over each item in steamids
    # and make a request using the Steam API and BeautifulSoup to get all the necessary data about each author
    for item in steamids:
        steamid = item.steamid
        # first of all find out how many followers and Portal 2 map submissions an author have
        try:
            soup = make_request('https://steamcommunity.com/profiles/' + steamid.replace('\n', '') + '/myworkshopfiles?appid=620')
            followers = int(soup.find_all('div', class_='followStat')[0].text.replace(',', '')) # in case there is a comma to separate thousands, remove it
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
        # if an author has at least 5 followers and 1 submission related to Portal 2, extract his personaname, avatar, profile_url and then make another request to find out how many coop maps he has and add him to the database
        if followers > 5 and submissions > 0:
            personaname = soup.select_one('#HeaderUserInfoName a').text
            profile_url = soup.select_one('#HeaderUserInfoName a')['href']
            avatar = soup.select_one('.playerAvatar > img')['src'] # there could be another div with an image inside this div, so we need to grab only the image which is a direct child
            # in case it's an animated gif or png image, just set it equal to default avatar
            if avatar.endswith('.gif') or avatar.endswith('.png'):
                    avatar = 'https://cdn.akamai.steamstatic.com/steamcommunity/public/images/avatars/6f/6f982210fe9a377fdb74d9a836e4d670f0fd68fc.jpg'
            else:
                avatar = avatar.replace('_medium', '')
            create_author(steamid, personaname, avatar, profile_url, followers, submissions)



def create_author(steamid, personaname, avatar, profile_url, followers, submissions):
    try:
        soup = make_request('https://steamcommunity.com/profiles/' + steamid.replace('\n', '') + '/myworkshopfiles?appid=620&requiredtags%5B%5D=Cooperative')
        coop_maps = soup.find_all('div', class_='workshopBrowsePagingInfo')
        if len(coop_maps) > 0:
            # extract all numerical characters from text
            numerical_characters = re.findall('[0-9]+', coop_maps[0].text)
            coop_maps = int(numerical_characters[-1])
        else:
            coop_maps = 0
        Author.objects.create(
            nicname=personaname,
            avatar=avatar,
            profile_url=profile_url,
            number_of_followers=followers,
            workshop_submissions=submissions,
            coop_maps=coop_maps
        )
    except:
        pass
