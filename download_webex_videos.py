# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 14:03:40 2021

@author: Ryan Burns
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import time
import json
from datetime import date
from datetime import timezone, timedelta
from pathlib import Path
import os
from scraping_utilities import go_to_downloads, launch_webdriver


url_xpath_dict = {'url': ('https://gartner.webex.com/webappng/sites'
                          '/gartner/recording/home'),
                  'api_url': ('https://gartner.webex.com/webappng/api/v1/'
                              'recordings?filterType=RecordingName&startDate'
                              '=&endDate=&keyword=&orderBy=createTime&'
                              'orderType=DESC&offset=0&limit=150'),
                  'download_button_loc0': ('/html/body/div[1]/div[4]/'
                                           'div/div/div/div[3]/div/div[2]'
                                           '/div/button[2]'),
                  'download_button_loc1': ('/html/body/div[1]/div[4]/'
                                           'div/div[1]/i[1]'),
                  'download_button_loc2': ('/html/body/div[1]/div[4]/div/div/'
                                           'div/div[1]/i[1]')}


def get_webex_video_list(url, api_url, driver):
    """
    Download metadata for all available WebEx videos.

    Parameters
    ----------
    url : string
        URL for WebEx homepage to permit manual login.
    api_url : string
        WebEx API URL for retrieving metadata for all available recordings.
    driver : webdriver
        Initialized webdriver for retrieving and manipulating web pages.

    Returns
    -------
    recording_data : dict
        Dictionary of the WebEx metadata for a single video.

    """
    driver.get(url)
    try:
        # Need to allow enough time to manually enter WebEx login credentials.
        (WebDriverWait(driver, 90).
         until(EC.
               presence_of_all_elements_located((By.XPATH,
                                                 '//*[@class="icon-download"]')
                                                )))
        driver.get(api_url)
        pre = driver.find_element_by_tag_name("pre").text
        recording_data = json.loads(pre)
        return recording_data
    except NoSuchElementException:
        return None


def download_webex_recordings(recording_data, date_val, driver):
    """
    Download WebEx recording files.

    Parameters
    ----------
    recording_data : Dict
        Recording video metadata dictionary from WebEx API url.
    date_val : date
        Oldest date for which videos should be downloaded as specified
        by the user.
    driver : webdriver
        Active webdriver for retrieving and manipulating web pages.

    Returns
    -------
    None.

    """
    for x in recording_data['recordings']:
        if (date.fromisoformat(x['createTime'][0:10]) < date_val):
            continue
        else:
            driver.get(x['playBackUrl'])
            driver.implicitly_wait(12)
            try:
                download_button = (driver.
                                   find_element_by_xpath(
                                       url_xpath_dict[
                                           'download_button_loc1']))
                download_button.click()
                # checks for downloadable .mp4 AND .vtt files
                try:
                    download_all_button = (driver.
                                           find_element_by_xpath(
                                               url_xpath_dict[
                                                   'download_button_loc0']))
                    download_all_button.click()
                except NoSuchElementException:
                    pass
            except NoSuchElementException:
                try:
                    download_button = (driver.
                                       find_element_by_xpath(
                                           url_xpath_dict[
                                               'download_button_loc2']))
                    download_button.click()
                    # checks for downloadable .mp4 AND .vtt files
                    try:
                        download_all_button = (driver.
                                               find_element_by_xpath(
                                                   url_xpath_dict[
                                                       'download_button_loc0'])
                                               )
                        download_all_button.click()
                    except NoSuchElementException:
                        pass
                except NoSuchElementException:
                    print(f'Exception-based skip: {x["playBackUrl"]}')
                    continue
            time.sleep(5)
            print('Completed scraping of recording ' +
                  str(recording_data['recordings'].index(x)+1))
    return None


def rename_webex_files_to_mountain_time():
    """
    Rename WebEx filename pattern matches to Mountain Time filename.

    Return
    ------
    None.

    """
    go_to_downloads()
    path = Path('.')
    video_list = list(path.glob('**/*.mp4'))
    captions_list = list(path.glob('**/*.vtt'))
    files_list = video_list + captions_list
    for x in files_list:
        if "Personal Room" in x.name:
            try:
                fname = x.name
                fname = fname.split('-', 1)[1][0:13]
                try:
                    utc_dt = pd.to_datetime(fname,
                                            infer_datetime_format=True,
                                            utc=True)
                    local_dt = utc_to_local(utc_dt)
                    filepath_string = os.path.join(path,
                                                   local_dt + x.name[-4:])
                    target = Path(filepath_string)
                    try:
                        x.rename(target)
                    except FileExistsError:
                        filepath_string = (filepath_string[:-4] + '_dupe' +
                                           x.name[-4:])
                        target = Path(filepath_string)
                        x.rename(target)
                    print(f"Done renaming {filepath_string}.")
                except FileNotFoundError:
                    pass
            except FileNotFoundError:
                pass
    print('Completed renaming video files.')
    return


def utc_to_local(utc_dt):
    """
    Return the UTC-0 time converted to Mountain Daylight Time.

    This will need updating when daylight savings switches,
    as it is hard-coded to MDT (UTC-6) right now, while MST will be (UTC-7).

    Parameters
    ----------
    utc_dt : datetime object
        The UTC-0 datetime object generated from the string filename containing
        date and time metadata for the recording file.

    Returns
    -------
    vid_dt_string : str
        The date and time converted from the GMT date object to local time.

    """
    local_tz = timezone(offset=-timedelta(hours=6), name="Mountain")
    fmt = '%m-%d-%Y, %I.%M %p'
    vid_dt = utc_dt.astimezone(local_tz)
    vid_dt_string = vid_dt.strftime(fmt)
    return vid_dt_string


def get_date_val():
    """
    Prompt for the oldest date of videos to download.

    Prompt the user to provide the oldest date from
    which they would like to download videos and return
    the value.

    Returns
    -------
    date_val : date
        Date object converted from string input provided by
        user in iso format.

    """
    date_val = ''
    i = 0
    while i == 0:
        try:
            date_val = date.fromisoformat(input('Please input the oldest date '
                                                'you would like to download '
                                                'videos from (YYYY-MM-DD): '))
            i = 1
        except ValueError:
            print('That date will not work, please try again.')
            continue
    return date_val


def main():
    driver = launch_webdriver()
    date_val = get_date_val()
    recording_data = get_webex_video_list(url_xpath_dict['url'],
                                          url_xpath_dict['api_url'],
                                          driver)
    download_webex_recordings(recording_data, date_val, driver)
    rename_webex_files_to_mountain_time()
    return


if __name__ == "__main__":
    main()
