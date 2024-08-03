

import requests
import urllib.request
import os
from PIL import Image
from dotenv import load_dotenv
from termcolor import colored

load_dotenv()

def authToken():
    """
        Fetches Auth Token from Kitsu API
    """
    url = "https://kitsu.io/api/oauth/token"
    data = {
        "grant_type": "password",
        "username": os.getenv("EMAIL"),
        "password": os.getenv("PASSWORD")
    }
    response = requests.post(url, data=data)
    return response.json()

def get_anime_data(anime_name):
    """
        Fetches Anime data from Kitsu API
    """
    tokenData = authToken()
    url = f"https://kitsu.io/api/edge/anime?filter[text]={anime_name}"
    response = requests.get(url, headers={
        "Authorization": f"Bearer {tokenData['access_token']}"
    })
    if(response.ok):
        responseJson = response.json()
        if (len(responseJson["data"]) <= 0): return {
            "error": "Anime not found. Please try again."
        }  
        data = responseJson["data"][0]
        return {
            "name": {
                "en_jp": data["attributes"]["titles"]["en_jp"],
                "ja_jp": data["attributes"]["titles"]["ja_jp"]
            },
            "description": "\n".join(data["attributes"]["description"].split("\n")[:-1]),
            "poster": data["attributes"]["posterImage"]["original"] if data["attributes"]["posterImage"] else None,
            "cover": data["attributes"]["coverImage"]["original"] if data["attributes"]["coverImage"] else None,
            "episodes": data["attributes"]["episodeCount"],
            "status": data["attributes"]["status"],
            "rating": data["attributes"]["averageRating"],
            "age_rating": data["attributes"]["ageRatingGuide"],
            "nsfw": "Yes" if data["attributes"]["nsfw"] else "No",
            "link": data["links"]["self"]
        }
    else:
        return {
            "error": "Something went wrong. Please try again."
        }

animeName = input("Enter Anime Name: ")
animeData = get_anime_data(animeName)

posterImage = False
coverImage = False

if (animeData["poster"] != None or animeData["cover"] != None):
    openImage = input("Open Image? (y/n): ")
    if (animeData["poster"] != None and openImage == "y"):
        posterImage = True
    if (animeData["cover"] != None and openImage == "y"):
        coverImage = True
else:
    openImage = "n"

if animeData.get("error"):
    print(animeData["error"])
else:
    print("\n")
    print(f"{colored('Name (English):', 'blue')} {animeData['name']['en_jp']}")
    print(f"{colored('Name (Japanese):', 'blue')} {animeData['name']['ja_jp']}")
    print(f"{colored('Description:', 'blue')}\n{animeData['description']}")
    print(f"{colored('Episodes:', 'blue')} {animeData['episodes']}")
    print(f"{colored('Status:', 'blue')} {animeData['status'].capitalize()}")
    print(f"{colored('Rating:', 'blue')} {animeData['rating']}")
    print(f"{colored('Age Rating:', 'blue')} {animeData['age_rating']}")
    print(f"{colored('NSFW:', 'blue')} {animeData['nsfw']}")
    print(f"{colored('Link:', 'blue')} {animeData['link']}")
    print(f"{colored('Poster Link:', 'blue')} {animeData['poster']}")
    print(f"{colored('Cover Link:', 'blue')} {animeData['cover']}")

    if openImage.lower() == "y" or openImage.lower() == "yes":
        print("\n")
        opener = urllib.request.URLopener()
        opener.addheader('User-Agent', 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Mobile Safari/537.36')

        if posterImage == True:
            print(colored("Loading Poster Image...", "yellow"))
            opener.retrieve(animeData["poster"], "poster.jpg")

            poster = Image.open("poster.jpg")
            poster.show()
            print(colored("Poster Image Loaded!", "green"))
        else:
            print(colored("No Poster Image for this Anime!", "red"))

        if coverImage == True:
            print(colored("Loading Cover Image...", "yellow"))
            opener.retrieve(animeData["cover"], "cover.jpg")

            cover = Image.open("cover.jpg")
            cover.show()
            print(colored("Cover Image Loaded!", "green"))
        else:
            print(colored("No Cover Image for this Anime!", "red"))
