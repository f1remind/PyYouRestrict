import json
import requests
from bs4 import BeautifulSoup as bs

youtube = 'https://www.youtube.com'

#Channel link needs to be the full link
def get_channel_videos(channel_link, restricted = False):
    #This is where the content will be buffered in
    content = ''
    #This will store all the video titles and links
    videos = []
    session = requests.session()

    if not channel_link.endswith('/videos'): channel_link += '/videos'
    token = session.get(channel_link).text.split('\'XSRF_TOKEN\': "')[-1]
    token = token.split('"')[0]


    if restricted:
        data = {
            'safety_mode':'true',
            'next_url': channel_link,
            'session_token': token
        }
        session.post('https://www.youtube.com/set_safety_mode', data=data)

    site = session.get(channel_link)
        
    soup = bs(site.content, 'html.parser')

    next_link = soup.select('.yt-uix-load-more')
    if next_link:
        next_link = youtube + next_link[0].get('data-uix-load-more-href')
            
        content += site.text
        
        site = session.get(next_link)
        response = json.loads(site.text)

        while response:
            if not 'content_html' in response:
                print("Unexpected response")
                for key in response: print(key)
                break
            content += response['content_html']
            soup = bs(response['load_more_widget_html'], 'html.parser')
            next_link = soup.select('.yt-uix-load-more')
            if next_link:
                site = session.get(youtube + next_link[0].get(
                    'data-uix-load-more-href'))
                response = json.loads(site.text)
            else:
                response = ''
    soup = bs(content, 'html.parser')
    for video in soup.select('.yt-uix-tile-link'):
        videos.append([video.get_text(), video.get('href')])
    return videos

def get_video_info(videolink, case_insensitive = True):
    if not youtube in videolink: videolink = youtube + videolink
    tags = []
    title = ''
    description = ''
    length = -1

    site = requests.get(videolink)
    soup = bs(site.content, 'html.parser')
    for tag in soup.select('meta'):
        if tag.get('property') == 'og:video:tag':
            tagvalue = tag.get('content')
            if case_insensitive: tagvalue = tagvalue.upper()
            tags.append(tagvalue)
        if tag.get('property') == 'og:title':
            if case_insensitive:
                title = tag.get('content').upper()
            else:
                title = tag.get('content')
        if tag.get('itemprop') == 'duration':
            length = tag.get('content').upper()
            length = length[2:-1].split('M')
            length = int(length[0])*60 + int(length[1])
        if tag.get('name') == 'description':
            if case_insensitive:
                description = tag.get('content').upper()
            else:
                description = tag.get('content')
    return title, tags, description, length

def get_channel_info(channellink):
    pass
