import codecs
import requests
from instagram_web_api import Client, ClientError
import json
import codecs
from login_cookies import get_cookies,from_json

# in this app i use web api instead of private api because web api takes longer to get blocked (for me)



user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
headers = {'User-Agent': user_agent}
username = 'saitaro.bot'
password = 'othman8462'


# i did this to replace the original function since the original one is not working
Client._extract_rhx_gis = staticmethod(lambda *args: "4f8732eb9ba7d1c8e8897a75d6474d4eb3f5279137431b2aafb71fafe2abe178")


def login(cookies_folder):
    settings_json = open(cookies_folder)
    cached_settings = json.load(settings_json, object_hook=from_json)
    api = Client(
        auto_patch=True, settings=cached_settings, user_agent=user_agent, username=username, password=password, authenticate=True)
    return api


try:
    api = login('settings.json')
except:
    get_cookies(save_path='settings.json',
                username=username, password=password)
    api = login('settings.json')





def get_post_code(post_url):
    code = post_url.split('/')[-2]
    return code


def get_media_id(url):
    req = requests.get('https://api.instagram.com/oembed/?url=' + url)
    data = req.json()
    media_id = data['media_id']
    return media_id


def get_user(username):
    url = f'https://www.instagram.com/{username}/?__a=1'
    r = requests.get(url)
    data = r.json()
    try:
        id = data['graphql']['user']['id']
        is_private = data['graphql']['user']['is_private']
    except:
        raise Exception('please check the username you entered and make sure that the account is public')
    
    return {"id": id, "is_private": is_private}


def get_user_story(username):

    user = get_user(username)
    if user['is_private']:
        raise Exception('This account is private or does not exist')
    
    stories = api.reels_feed(reel_ids=[user["id"]])['data']['reels_media']
    
    if len(stories) == 0:
        raise Exception('This account has no stories')
     
       
    for story in stories[0]['items']:
        if story['is_video']:
            # video
            print('video')
            video_url = story["video_resources"][0]['src']
            yield video_url

        else:
            # image
            print('image')
            image_url = story["display_url"]
            yield image_url


def get_post(url):
    if '?__a=1' not in url:
        url+= '?__a=1'
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
    r = requests.get(url, headers={'User-Agent': user_agent})
    data = r.json()['graphql']['shortcode_media']
    with open('data.json', 'w') as f:
        json.dump(data, f)
    if 'edge_sidecar_to_children' not in data:
        if data['is_video']:
            # video
            print('video')
            video_url = data['video_url']
            yield video_url
        else:    
            # image
            print('image')
            yield data['display_url']
        return
        
    for post in data['edge_sidecar_to_children']['edges']:
        media = post['node']
        if media['is_video']:
            # video
            print('video')
            video_url = media['video_url']
            yield video_url
        
        else:
            # image
            print('image')
            image_url = media['display_url']
            yield image_url


