# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 14:03:40 2021

@author: Ryan
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
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
import sys


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


def launch_webdriver(webdriver_path=None):
    """
    Instantiate the webdriver application.

    Need to save updated webdriver application to downloads folder or
    hardcode path to webdriver. Options can also be set to run a
    headless webdriver, but this is not the given state due to login
    requirements.

    Parameters
    ----------
    webdriver_path : TYPE, optional
        DESCRIPTION. The default is None.

    Returns
    -------
    None.

    """
    options = Options()
    if webdriver_path is None:
        go_to_downloads()
    driver_filepath = (os.path.join(os.getcwd(), 'chromedriver.exe'))
    sys.path.append(driver_filepath)
    driver = webdriver.Chrome(driver_filepath,
                              options=options)
    return(driver)


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
    None.

    """
    driver.get(url)
    try:
        '''Need to allow enough time to manually
        enter WebEx login credentials.'''
        (WebDriverWait(driver, 90).
         until(EC.
               presence_of_all_elements_located((By.XPATH,
                                                 '//*[@class="icon-download"]')
                                                )))
        driver.get(api_url)
        pre = driver.find_element_by_tag_name("pre").text
        recording_data = json.loads(pre)
        return(recording_data)
    except Exception as e:
        raise e
        return


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
    return


def rename_webex_files_to_mountain_time():
    """Rename WebEx filename pattern matches to Mountain Time filename."""
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
                    x.rename(target)
                    print(f"Done renaming {filepath_string}.")
                except Exception:
                    pass
            except Exception:
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
    string
        The date and time converted from the GMT date object to local time.

    """
    local_tz = timezone(offset=-timedelta(hours=6), name="Mountain")
    fmt = '%m-%d-%Y, %I.%M %p'
    vid_dt = utc_dt.astimezone(local_tz)
    return vid_dt.strftime(fmt)


def go_to_downloads():
    """
    Navigate to downloads folder regardless of OS.

    This function is a modified version of the code from
    Michael Kropat at https://gist.github.com/mkropat/7550097.

    Returns
    -------
    string
        Path to the new working directory (which should be the
        Downloads folder).

    """
    if os.name == 'nt':
        import ctypes
        from ctypes import windll, wintypes
        from uuid import UUID

        # ctypes GUID copied from MSDN sample code
        class GUID(ctypes.Structure):
            _fields_ = [
                ("Data1", wintypes.DWORD),
                ("Data2", wintypes.WORD),
                ("Data3", wintypes.WORD),
                ("Data4", wintypes.BYTE * 8)
            ]

            def __init__(self, uuidstr):
                uuid = UUID(uuidstr)
                ctypes.Structure.__init__(self)
                self.Data1, self.Data2, self.Data3, \
                    self.Data4[0], self.Data4[1], rest = uuid.fields
                for i in range(2, 8):
                    self.Data4[i] = rest >> (8-i-1)*8 & 0xff

        SHGetKnownFolderPath = windll.shell32.SHGetKnownFolderPath
        SHGetKnownFolderPath.argtypes = [
            ctypes.POINTER(GUID), wintypes.DWORD,
            wintypes.HANDLE, ctypes.POINTER(ctypes.c_wchar_p)
        ]

        def _get_known_folder_path(uuidstr):
            pathptr = ctypes.c_wchar_p()
            guid = GUID(uuidstr)
            if SHGetKnownFolderPath(ctypes.byref(guid),
                                    0,
                                    0,
                                    ctypes.byref(pathptr)):
                raise ctypes.WinError()
            return pathptr.value

        FOLDERID_Download = '{374DE290-123F-4565-9164-39C4925E467B}'

        def get_download_folder():
            new_wd = _get_known_folder_path(FOLDERID_Download)
            os.chdir(new_wd)
            return new_wd
    else:
        def get_download_folder():
            home = os.path.expanduser("~")
            new_wd = os.path.join(home, "Downloads")
            os.chdir(new_wd)
            return new_wd
    get_download_folder()


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


if __name__ == "__main__":
    main()
