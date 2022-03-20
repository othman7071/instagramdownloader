import codecs
import requests
from instagram_web_api import Client, ClientError
import json
import codecs
from login_cookies import get_cookies
# get user story


# save cookies to file
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
headers = {'User-Agent': user_agent}

username = 'saitaro.bot'
password = 'othman8462'
Client._extract_rhx_gis = lambda self, * \
    args, **kwargs: "4f8732eb9ba7d1c8e8897a75d6474d4eb3f5279137431b2aafb71fafe2abe178"


def from_json(json_object):
    if '__class__' in json_object and json_object['__class__'] == 'bytes':
        return codecs.decode(json_object['__value__'].encode(), 'base64')
    return json_object


def login(cookies_folder):
    settings_json = open(cookies_folder)
    cached_settings = json.load(settings_json, object_hook=from_json)
    stories_api = Client(
        auto_patch=True, settings=cached_settings, user_agent=user_agent, username=username, password=password, authenticate=True)
    return stories_api


try:
    stories_api = login('settings.json')

except:
    get_cookies(settings_path='settings.json',
                username=username, password=password)
    stories_api = login('settings.json')

posts_api = Client(user_agent=user_agent)


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
    id = data['graphql']['user']['id']
    is_private = data['graphql']['user']['is_private']
    return {"id": id, "is_private": is_private}


def get_user_story(username):

    user = get_user(username)
    if user['is_private']:
        return [0, 'user is private']

    stories = stories_api.reels_feed(reel_ids=[user["id"]])
    story_files = []
    for story in stories['data']['reels_media'][0]['items']:
        if story['is_video']:
            # video
            print('video')
            video_url = story["video_resources"][0]['src']
            req = requests.get(video_url)
            with open(f'{story["id"]}.mp4', 'wb') as f:
                f.write(req.content)
            story_files.append(f'{story["id"]}.mp4')

        else:
            # image
            print('image')
            media_url = story["display_url"]
            r = requests.get(media_url, headers=headers)
            with open(f'{story["id"]}.jpg', 'wb') as f:
                f.write(r.content)
            story_files.append(f'{story["id"]}.jpg')
    return [1, story_files]


def get_post_media(url):
    code = get_post_code(url)
    try:
        post = posts_api.media_info2(code)
    except ClientError:
        return [0, 'error, please check the url you entered and make sure that the account is public']

        # save post to json file
    with open('post.json', 'w') as f:
        json.dump(post, f)
    file_name = ''
    if post['is_video']:
        # video
        print('video')
        video_url = post['video_url']
        req = requests.get(video_url)
        with open(f'{post["id"]}.mp4', 'wb') as f:
            f.write(req.content)
        file_name = f'{post["id"]}.mp4'
    else:
        # image
        print('image')
        media_url = post['images']['standard_resolution']['url']
        r = requests.get(media_url, headers=headers)
        with open(f'{post["id"]}.jpg', 'wb') as f:
            f.write(r.content)
        file_name = f'{post["id"]}.jpg'
    return [1, file_name]


get_user_story('pain.memess')
