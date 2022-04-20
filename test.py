
url = 'https://www.instagram.com/tv/CImdRHRhs2f/'
instagram_url = 'https://www.instagram.com'

if not ( url.startswith(instagram_url + '/p') or url.startswith(instagram_url + '/tv') ):
            print('Invalid url')