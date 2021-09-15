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


def launch_webdriver(webdriver_path=None):
    """
    Instantiate the webdriver application.

    Need to save updated webdriver application to downloads folder or
    hardcode path to webdriver. Options can also be set to run a
    headless webdriver, but this is not the given state due to login
    requirements.

    Parameters
    ----------
    webdriver_path : string, optional
        Alternate filepath to directory containing chromedriver.exe.
        The default is None.

    Returns
    -------
    driver : webdriver
        Initialized webdriver for retrieving and manipulating web pages.
    """
    options = Options()
    if webdriver_path is None:
        go_to_downloads()
    driver_filepath = (os.path.join(os.getcwd(), 'chromedriver.exe'))
    sys.path.append(driver_filepath)
    driver = webdriver.Chrome(driver_filepath,
                              options=options)
    return driver


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


def scroll(driver, timeout):
    """
    Scroll down webpage with infinite scroll.

    This function is a slightly modified version of the code from
    artjomb at https://gist.github.com/artjomb/07209e859f9bf0206f76.

    Parameters
    ----------
    driver : webdriver Object
        Initialized webdriver for retrieving and manipulating web pages.
    timeout : int
        The number of seconds to put the driver to sleep before continuing
        to scroll. This can be modified depending on connectivity and webpage
        update speeds, so long as the page is given time to load before
        scrolling further.

    Returns
    -------
    None.

    """
    scroll_pause_time = timeout

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        (driver.
         execute_script("window.scrollTo(0, document.body.scrollHeight);"))

        # Wait to load page
        time.sleep(scroll_pause_time)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            # If heights are the same it will exit the function
            break
        last_height = new_height
    return


def go_to_downloads():
    """
    Navigate to downloads folder regardless of OS.

    This function is a modified version of the code from
    Michael Kropat at https://gist.github.com/mkropat/7550097.

    Returns
    -------
    new_wd : string
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


if __name__ == "__main__":
    driver = launch_webdriver()
    web_string_list = collect_video_links(driver)
    download_transcripts(web_string_list)
