# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 13:29:19 2021

@author: Ryan
"""

import webvtt
from pathlib import Path
import os
from scraping_utilities import go_to_downloads


def read_caption(webvtt_file):
    """
    Create list of every line in .vtt file.

    Parameters
    ----------
    webvtt_file : string
        File name for .vtt file being read.

    Returns
    -------
    text_lst : list
        List of each line in .vtt file.

    """
    text_lst = []
    for caption in webvtt.read(webvtt_file):
        text_lst.append(caption.text)
    return text_lst


def get_vtt_file_list(vtt_dir=None):
    """
    Gather all .vtt file names from specified directory.

    Parameters
    ----------
    vtt_dir : string, optional
        File path to directory containing .vtt files, or will search the current
        working directory if value is None.. The default is None.

    Returns
    -------
    vtt_list : list
        List of .vtt file names found in specified directory.

    """
    if vtt_dir is None:
        go_to_downloads()
        vtt_dir = os.getcwd()
    path = Path('.')
    vtt_list = list(path.glob('**/*.vtt'))
    return vtt_list


def main():
    """
    Parse list of .vtt caption files into transcript .txt files.

    Return
    ------
    None.

    """
    vtt_list = get_vtt_file_list()
    print(f'Found {len(vtt_list)} caption files. Beginning parsing.')
    i = 0
    num_vids = len(vtt_list)
    for video in vtt_list:
        transcript = read_caption(video)
        text = ' '.join(transcript).replace('\n', ' ')
        filestring = video.name[:-4] + '.txt'
        with open(filestring, "w+", encoding='utf-8') as file:
            file.write(text)
        i += 1
        print(f'{round(i/num_vids*100, 2)}% complete')
    return


if __name__ == "__main__":
    main()
