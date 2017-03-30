#!/usr/bin/python3.4

import time
from tools import youtubetools
from tools import datatools

def main():
    channels = [
        ['TL;DR', 'https://www.youtube.com/channel/UCMIj-wEiKIcGAcLoBO2ciQQ'],
        ['thunderf00t', 'https://www.youtube.com/channel/UCmb8hO2ilV9vRa8cilis88A'],
        ['Steve Shives', 'https://www.youtube.com/user/stevelikes2curse'],
        ['Creationist Cat', 'https://www.youtube.com/channel/UCQpltQMhYFvyeS5M6P0Zg-Q'],
        ['Sargon of Akkad', 'https://www.youtube.com/user/SargonofAkkad100'],
        ['Computerphile', 'https://www.youtube.com/channel/UC9-y-6csu5WGm29I7JiwpnA'],
        ['David Firth', 'https://www.youtube.com/channel/UCLhtZqdkjshgq8TqwIjMdCQ'],
        ['Gryffix', 'https://www.youtube.com/channel/UCUMEY7WqI66LhMuAC_V7tAw'],
        ['LastWeekTonight', 'https://www.youtube.com/channel/UC3XTzVzaHQEd30rQbuvCtTQ'],
        ['Roaming Millennial', 'https://www.youtube.com/channel/UCLUrVTVTA3PnUFpYvpfMcpg'],
        ['Tom Scott', 'https://www.youtube.com/channel/UCBa659QWEk1AI4Tg--mrJ2A'],
        ['Gazi Kodzo', 'https://www.youtube.com/user/smiletone'],
        ['feministfrequency', 'https://www.youtube.com/user/feministfrequency'],
        ['Kristi Winters', 'https://www.youtube.com/user/drkmwinters'],
        ['VICE', 'https://www.youtube.com/channel/UCn8zNIfYAQNdrFRrr8oibKw'],
        ['logicked', 'https://www.youtube.com/user/logicked'],
        
    ]
    get_videos_from_channels(channels)

def get_videos_from_channels(channels):
    channel_data = {}

    for channel in channels:
        start = time.time()
        print("Getting video list for channel:", channel[0])
        videos = youtubetools.get_channel_videos(channel[1])
        safe_videos = youtubetools.get_channel_videos(channel[1], True)
        restricted_videos = []

        for vid in videos:
            if vid not in safe_videos: restricted_videos.append(vid)

        channel_data[channel[0]] = [
            videos,
            safe_videos,
            restricted_videos
        ]
        print("Finished getting data for channel", channel[0], end='')
        print(" - Duration:", int(time.time() - start), 'seconds')

    for channel_name in channel_data:
        print("Channel:", channel_name)
        print("Videos total:", len(channel_data[channel_name][0]))
        print("Safe videos: ", len(channel_data[channel_name][1]))
        print("Restricted:  ", len(channel_data[channel_name][2]))
        print()
        #this was debug stuff

    video_list = {}
    for channel_name in channel_data:
        start = time.time()
        print('Getting video information')
        restricted_videos = channel_data[channel_name][2]
        counter = 0
        for video in channel_data[channel_name][0]:
            titl, tags, desc, dur = youtubetools.get_video_info(video[1])
            video_list[titl] = {
                'title': titl,
                'description': desc,
                'tags': tags,
                'duration': dur,
                'restricted': video in channel_data[channel_name][2]
            }
            counter += 1
            print('{}/{}: Got information from'.format(counter,
                len(channel_data[channel_name][0])), video[0])
        print('Done getting video information')
        print('Elapsed time:', int(time.time() - start), 'seconds')

    sorted_tags = datatools.most_banned_tags(video_list)
    print(*sorted_tags, sep='\n')
    with open('sorted_list', 'w') as f:
        print(*sorted_tags, sep='\n', file=f)
    return video_list



if __name__ == '__main__':
    main()
