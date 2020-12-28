import os
import re
import sys

import ffmpeg
import pytube

def fetch_video_stream(yt):
    for i in yt.streams:
        if i.resolution == "1080p":
            print("1080p:",i)
    for i in yt.streams:
        print(i)
        if i.resolution=="1080p":
            print("Video track found:",i)
            return i

def fetch_audio_stream(yt):
    best_audio_idx=0
    best_audio_rate = 0
    counter=0
    for i in yt.streams:
        # print("audiostream:",i)
        if (str(i.mime_type) == "audio/webm") or (str(i.mime_type) == "audio/mp4"):
            result = int(re.sub('[^0-9]', '', i.abr))
            if result > best_audio_rate:
                best_audio_rate=result
                best_audio_idx=counter
                best_audio_found=True
        counter=counter+1
    if best_audio_found==True:
        print("Audio track found :",yt.streams[best_audio_idx])
        return yt.streams[best_audio_idx]
    else:
        raise Exception

def print_hi(name):
    f = open("urls", "r")
    name=f.readline()
    name=name.replace(' ','')
    url_video=f.readline()
    while name:
        try:
            youtube = pytube.YouTube(url_video)
            print(youtube)
            vs=fetch_video_stream(youtube)
            original_vpath = vs.download()
            trimmed_vpath= original_vpath.replace(' ','')
            trimmed_video_path=trimmed_vpath.replace('.','_video.')
            trimmed_video_path = trimmed_video_path.replace('(', '')
            trimmed_video_path = trimmed_video_path.replace(')', '')
            trimmed_video_path = trimmed_video_path.replace(':', '')
            print("modified vpath",trimmed_video_path)
            os.rename(original_vpath,trimmed_video_path)

            audiostream=fetch_audio_stream(youtube)
            original_apath = audiostream.download()
            trimmed_apath= original_apath.replace(' ','')
            trimmed_audio_path=trimmed_apath.replace('.','_audio.')
            trimmed_audio_path = trimmed_audio_path.replace('(', '')
            trimmed_audio_path = trimmed_audio_path.replace(')', '')
            trimmed_audio_path = trimmed_audio_path.replace(':', '')
            print("modified apath",trimmed_audio_path)
            os.rename(original_apath,trimmed_audio_path)

            mkvpath=trimmed_video_path.replace('.mp4', '.mkv')
            command = "ffmpeg -i "+trimmed_video_path+" -i "+trimmed_audio_path+" -c copy "+mkvpath
            print(command)
            os.system(command)
            name = f.readline()
            name = name.replace(' ', '')
            url_video = f.readline()

        except :
            print(name,url_video)
            e = sys.exc_info()[0]
            print('stdout:', e.stdout)
            print('stderr:', e.stderr)
            raise e



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
