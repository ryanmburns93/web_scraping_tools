# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 17:21:22 2021

@author: Ryan Burns
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import sys
from utilities import go_to_downloads, scroll

web_string_list = []
xpath_url_lib = {'stream_group_url': ('https://web.microsoftstream.com/group/'
                                      'ac5670a9-e1bb-4ea8-ae99-972dc94a84d0?'
                                      'view=videos'),
                 'download_button_xpath': ('/html/body/div[1]/div/div[2]/'
                                           'video-update/section/form/div[2]/'
                                           'video-edit/section/div[1]/div[3]/'
                                           'video-edit-options-pane/div/'
                                           'captions-and-subtitles/div/div[1]'
                                           '/div[1]/button'),
                 'show_more_button_xpath': ('//button[@class = "show-more '
                                            'c-hyperlink c-action-trigger '
                                            'ng-binding"]'),
                 'video_button_list_xpath': ('/html/body/div[1]/div/div[2]/'
                                             'group-page/section/section[2]/'
                                             'group-video-results/'
                                             'video-results/div[2]/items-list/'
                                             'div/div[1]/div/item/item/'
                                             'group-video-item/div/list-row/'
                                             'ng-transclude/list-cell[1]/div/'
                                             'div/ng-transclude/div[2]/h3/a'),
                 'download_video_xpath': ('/html/body/div[1]/div/div[2]/'
                                          'group-page/section/section[2]/'
                                          'group-video-results/video-results/'
                                          'div[3]/items-list/div/div[1]/div/'
                                          'item/item/group-video-item/div/'
                                          'list-row/ng-transclude/list-cell[5]'
                                          '/div/div/ng-transclude/div/'
                                          'flex-drawer/div/div/ul/li[6]/'
                                          'button'),
                 'menu_drawer_xpath': ('/html/body/div[1]/div/div[2]/group-'
                                       'page/section/section[2]/group-'
                                       'video-results/video-results/div[3]'
                                       '/items-list/div/div[1]/div/item/'
                                       'item/group-video-item/div/list-row'
                                       '/ng-transclude/list-cell[5]/div/div/'
                                       'ng-transclude/div/flex-drawer/div/div'
                                       '/span[1]/button')}


def collect_video_links(driver):
    """
    Scroll to view all videos and collect list of video links.

    Parameters
    ----------
    driver : webdriver Object
        Initialized webdriver for retrieving and manipulating web pages.

    Returns
    -------
    web_string_list : TYPE
        DESCRIPTION.

    """
    driver.get(xpath_url_lib['stream_group_url'])
    try:
        (WebDriverWait(driver, 120).
         until(EC.
               presence_of_all_elements_located((By.XPATH,
                                                 xpath_url_lib[
                                                     'show_more_button_xpath'])
                                                )))
        show_more_button = driver.find_element_by_xpath(xpath_url_lib[
            'show_more_button_xpath'])
        show_more_button.click()
    except Exception:
        pass
    try:
        scroll(driver, 3)
        scroll(driver, 5)
        video_button_list = driver.find_elements_by_xpath(xpath_url_lib[
            'video_button_list_xpath'])
        video_link_list = [video_button_list[i].get_attribute('href')
                           for i in range(len(video_button_list))]
        separator = '/'
        split_link_list = [link.split(separator) for link in video_link_list]
        web_string_list = [(separator.join(link_list[0:4])
                            + 'update/'
                            + link_list[-1])
                           for link_list in split_link_list]
        return web_string_list
    except Exception as e:
        print(e)
        return web_string_list


def download_transcripts(web_string_list, driver):
    """
    Download transcripts of listed videos.

    Parameters
    ----------
    web_string_list : list
        List of URL addresses for each individual video in the MS Stream group.
    driver : webdriver Object
        Initialized webdriver for retrieving and manipulating web pages.

    Returns
    -------
    None.

    """
    for web_string in web_string_list:
        driver.get(web_string)
        (WebDriverWait(driver, 10).
         until(EC.
               presence_of_all_elements_located((By.
                                                 XPATH,
                                                 xpath_url_lib[
                                                     'download_button_xpath']))
               ))
        download_file_button = (driver.
                                find_element_by_xpath(
                                    xpath_url_lib['download_button_xpath']))
        download_file_button.click()
    return


def download_videos(driver):
    """


    Parameters
    ----------
    driver : webdriver Object
        Initialized webdriver for retrieving and manipulating web pages.

    Returns
    -------
    menu_drawer_button_list : TYPE
        DESCRIPTION.
    download_video_button_list : TYPE
        DESCRIPTION.

    """
    driver.get(xpath_url_lib['stream_group_url'])
    try:
        (WebDriverWait(driver, 150).
         until(EC.
               presence_of_all_elements_located((By.XPATH,
                                                 xpath_url_lib[
                                                     'show_more_button_xpath'])
                                                )))
        show_more_button = driver.find_element_by_xpath(xpath_url_lib[
            'show_more_button_xpath'])
        show_more_button.click()
    except Exception as e:
        print(e)
        pass
    try:
        scroll(driver, 2)
        scroll(driver, 3)
        menu_drawer_button_list = (driver.
                                   find_elements_by_xpath(
                                       xpath_url_lib[
                                           'menu_drawer_xpath']))
        download_video_button_list = (driver.
                                      find_elements_by_xpath(
                                          xpath_url_lib[
                                              'download_video_xpath']))
    except Exception as e:
        print(e)
        pass
    for i in range(len(menu_drawer_button_list)):
        attempts = 3
        while attempts > 0:
            try:
                menu_drawer_button_list[i].click()
                (WebDriverWait(driver, 10).
                 until(EC.
                       visibility_of(
                           download_video_button_list[i])))
                download_video_button_list[i].click()
                time.sleep(5)
                print(f'Completed download of video {i+1} of '
                      f'{len(menu_drawer_button_list)}')
                attempts = 0
            except Exception as e:
                print(e)
                attempts -= 1
    return menu_drawer_button_list, download_video_button_list


if __name__ == "__main__":
    driver = launch_webdriver()
    web_string_list = collect_video_links(driver)
    download_transcripts(web_string_list)
