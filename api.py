from instagrapi import  Client  




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
        
        user = self.cl.user_id_from_username(username)
        stories = self.cl.user_stories(user)
        
        if len(stories) == 0:
            yield 'This account has no stories'
            return
        for story in stories:
            if story.media_type ==1:
                yield story.thumbnail_url
            else:
                yield story.video_url
    
    def get_post(self,url):
        instagram_url = 'https://www.instagram.com'
        if not ( url.startswith(instagram_url + '/p') or url.startswith(instagram_url + '/tv') or url.startswith(instagram_url + '/reel' )):
            yield 'Invalid url'
            return
        
        pk = self.cl.media_pk_from_url(url)
        media_info = self.cl.media_info(pk).dict()
        

        if media_info['media_type'] == 2 and media_info['product_type'] == 'igtv':
            yield media_info['video_url']
            return 

        if media_info['media_type'] == 1:
            yield media_info['thumbnail_url']
            return
        
        elif media_info['media_type'] == 8:
            for m in media_info['resources']:
                if m['media_type'] == 1:
                    yield m['thumbnail_url']
                else:
                    yield m['video_url']
            return 
        elif media_info['media_type'] == 2 and media_info['product_type'] == 'clips':
            yield media_info['video_url']
        else:
            yield media_info['video_url']
            return
if __name__ =='__main__':    
    downloader = InstaLink('saitaro.bot','othman8462','settings.json')
    for url in downloader.get_post('https://www.instagram.com/reel/Cb-mKq_hIbl/?igshid=YmMyMTA2M2Y='):
        print(url)





