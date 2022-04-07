from instagrapi import  Client  
from ig_downloader import get_user 


class InstaLink:
    def __init__(self,username,password,settings_path):
        self.username = username
        self.password = password
        
        cl = Client()
        cl.load_settings(settings_path)
        cl.login(self.username,self.password)
        self.cl = cl
        print('Logged in')

        
    def get_user_stories(self,username:str)->str:
        
        user = get_user(username)
        if user['is_private']:
            yield 'This account is private or does not exist'
            return
        stories = self.cl.user_stories(user['id'])
        if len(stories) == 0:
            yield 'This account has no stories'
            return
        for story in stories:
            if story.media_type ==1:
                yield story.thumbnail_url
            else:
                yield story.video_url

        





