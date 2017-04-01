#!/usr/bin/python3.4

import time
import threading

from tools import youtubetools
from tools import datatools
import settings

def main():
    video_list = get_videos_from_channels(settings.channels)
    sorted_tags = datatools.most_banned_tags(video_list)
    for tag in sorted_tags: print(*tag, sep=settings.separator)
    with open('./data/sorted_list', 'w') as f:
        for tag in sorted_tags:
            print(*tag, sep=settings.separator, file=f)

def get_videos_from_channels(channels):
    channel_data = {}
    total_time_start = time.time()

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

    total_videos = sum([len(channel_data[e][0]) for e in channel_data])
    for channel_name in channel_data:
        print("Channel:", channel_name)
        print("Videos total:", len(channel_data[channel_name][0]))
        print("Safe videos: ", len(channel_data[channel_name][1]))
        print("Restricted:  ", len(channel_data[channel_name][2]))
        print()
        #this was debug stuff

    video_list = {}
    counter = 0
    output_list = []
    for channel_name in channel_data:
        start = time.time()
        print('Getting video information')
        restricted_videos = channel_data[channel_name][2]
        def download_video_information(video, restricted, output):
            titl, tags, desc, dur = youtubetools.get_video_info(video[1], settings.case_insensitive)
            output.append({
                'title': titl,
                'description': desc,
                'tags': tags,
                'duration': dur,
                'restricted': restricted
            })
            #print("Done getting", video)
        threadpool = []
        for video in channel_data[channel_name][0]:
            restricted = video in restricted_videos
            threadpool.append(
                threading.Thread(
                    target=download_video_information,
                    args = [video, restricted, output_list],
                    name = video[0]
                )
            )
            #download_video_information(video, restricted, output_list)
        started_threads = []
        while threadpool:
            new_threads = threadpool
            while threading.active_count() <= settings.max_downloads and new_threads:
                t1 = new_threads.pop()
                started_threads.append(t1)
                t1.start()
                counter += 1
                print('{:>02}:{:>02}:{:>02} Downloading information {}/{} from:\n\t'.format(
                        int((time.time() - total_time_start)/3600),
                        int(((time.time() - total_time_start)/60)%60),
                        int(time.time() - total_time_start)%60,
                        counter,
                        total_videos
                    ), t1.name, '\n\thas started\n')
            finished_threads = []
            for thread in started_threads:
                if not thread.is_alive():
                    finished_threads.append(thread)
            for thread in finished_threads:
                if thread in threadpool:
                    threadpool.remove(thread)
            time.sleep(0.1)
        for thread in started_threads: thread.join()
        print('Done getting video information')
        print('Elapsed time:', int(time.time() - total_time_start), 'seconds')
    return output_list

if __name__ == '__main__':
    main()
