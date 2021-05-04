import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl
import re
from datetime import datetime
from authors.utils.SteamGroup import SteamGroup
from authors.models import Author, AuthorTemp, Steamid, NoGroupAuthor, SteamGroupName, UpdateDate


ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def return_soup(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req, context=ctx).read()
        return BeautifulSoup(html, 'html.parser')
    except:
        return None



def update_authors_steamid_table():
    # make a backup before deleting everything
    steamids_backup = list(Steamid.objects.all())
    # first of all get SteamID64's of those authors who don't belong to any group
    all_steamids = [item.steamid for item in NoGroupAuthor.objects.all()]
    # delete everything from the authors_steamid table before populating it again
    Steamid.objects.all().delete()
    # get all groups from the authors_steamgroup table and iterate over them
    steam_groups = SteamGroupName.objects.all()
    try:
        for group in steam_groups:
            # use the SteamGroup.py module to fetch the SteamID64's of all the Steam group members
            # and add them to all_steamids list
            steamgroup = SteamGroup(group.group_name)
            all_steamids.extend(steamgroup.get_steam_ids())
        all_steamids = list(set(all_steamids))  # remove duplicates
        objects = [Steamid(steamid=steamid) for steamid in all_steamids]
        Steamid.objects.bulk_create(objects)
        UpdateDate.objects.create(model_name='Steamid', timestamp=datetime.utcnow())
        print('All steamids have been successfully updated!')
    except:
        # in case something goes wrong populate it from backup
        objects = [Steamid(steamid=item.steamid) for item in steamids_backup]
        Steamid.objects.bulk_create(objects)
        print('All steamids have been restored from backup!')



def update_authors_authortemp_table():
    # remove everything from the AuthorTemp model before populating it again
    AuthorTemp.objects.all().delete()
    # load all steamids into a list
    steamids = list(Steamid.objects.all())
    # iterate over each item in steamids
    # and make a request using the Steam API and BeautifulSoup to get all the necessary data about each author
    for item in steamids:
        steamid = item.steamid
        soup = return_soup('https://steamcommunity.com/profiles/' + steamid + '/myworkshopfiles?appid=620')
        if soup:
            # first of all find out how many followers and Portal 2 map submissions an author have
            followers = soup.find_all('div', class_='followStat')
            if len(followers) > 0:
                followers = int(followers[0].text.replace(',', '')) # in case there is a comma to separate thousands, remove it
            else:
                followers = 0
            submissions = soup.find_all('div', class_='workshopBrowsePagingInfo')
            if len(submissions) > 0:
                # extract all numerical characters from text
                numerical_characters = re.findall('[0-9]+', submissions[0].text)
                submissions = int(numerical_characters[-1])
            else:
                submissions = 0
        else:
            # if something goes wrong with the request just skip it by setting the followers variable to 0
            followers = 0
        # if an author has at least 5 followers and 1 submission related to Portal 2, extract his personaname, avatar, profile_url
        # and then make another request to find out how many coop maps he has and add him to the database
        if followers > 5 and submissions > 0:
            personaname = soup.select_one('#HeaderUserInfoName a').text
            profile_url = soup.select_one('#HeaderUserInfoName a')['href']
            avatar = soup.select_one('.playerAvatar > img')['src'] # there could be another div with an image inside this div, so we need to grab only the image which is a direct child
            # in case it's an animated gif or png image, just set it equal to default avatar
            if avatar.endswith('.gif') or avatar.endswith('.png'):
                avatar = 'https://cdn.akamai.steamstatic.com/steamcommunity/public/images/avatars/6f/6f982210fe9a377fdb74d9a836e4d670f0fd68fc.jpg'
            else:
                avatar = avatar.replace('_medium', '')
            soup = return_soup('https://steamcommunity.com/profiles/' + steamid + '/myworkshopfiles?appid=620&requiredtags%5B%5D=Cooperative')
            if soup:
                coop_maps = soup.find_all('div', class_='workshopBrowsePagingInfo')
                if len(coop_maps) > 0:
                    # extract all numerical characters from text
                    numerical_characters = re.findall('[0-9]+', coop_maps[0].text)
                    coop_maps = int(numerical_characters[-1])
                else:
                    coop_maps = 0
                create_author(personaname, avatar, profile_url, followers, submissions, coop_maps)
    else:
        # after all the data has been collected and stored in the AuthorTemp model, update the Author model
        update_authors_author_table()



def create_author(personaname, avatar, profile_url, followers, submissions, coop_maps):
    try:
        AuthorTemp.objects.create(
            nicname=personaname,
            avatar=avatar,
            profile_url=profile_url,
            number_of_followers=followers,
            workshop_submissions=submissions,
            coop_maps=coop_maps
        )
    except:
        pass


def update_authors_author_table():
    Author.objects.all().delete()
    authors_temp = AuthorTemp.objects.all()
    authors = [Author(
        nicname=item.nicname,
        profile_url=item.profile_url,
        avatar=item.avatar,
        number_of_followers=item.number_of_followers,
        workshop_submissions=item.workshop_submissions,
        coop_maps=item.coop_maps
    ) for item in authors_temp]
    Author.objects.bulk_create(authors)
    UpdateDate.objects.create(model_name='Author', timestamp=datetime.utcnow())
    print('All the authors have been successfully updated!')
