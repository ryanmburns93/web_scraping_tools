# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 13:29:19 2021

@author: Ryan
"""

import webvtt
from pathlib import Path
import os
from utilities import go_to_downloads

text_lst = []
transcript = []


def read_caption(webvtt_file):
    text_lst = []
    for caption in webvtt.read(webvtt_file):
        text_lst.append(caption.text)
    return text_lst


def get_vtt_file_list(vtt_dir=None):
    if vtt_dir is None:
        go_to_downloads()
        vtt_dir = os.getcwd()
    path = Path('.')
    video_list = list(path.glob('**/*.vtt'))
    return video_list


def main():
    video_list = get_vtt_file_list()
    print(f'Found {len(video_list) videos. Beginning parsing.}')
    i = 0
    num_vids = len(video_list)
    for video in video_list:
        transcript = read_caption(video)
        text = ' '.join(transcript).replace('\n', ' ')
        filestring = video.name[:-4] + '.txt'
        with open(filestring, "w+", encoding='utf-8') as file:
            file.write(text)
        i += 1
        print(f'{round(i/num_vids*100, 2)}% complete')


if __name__ == "__main__":
    main()
