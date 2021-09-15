# -*- coding: utf-8 -*-
"""
Created on Fri Jun 25 23:40:49 2021

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


xpath_dict = {'all_convo_page': ('//*[@class='
                                 '"otter_my_conversation_group__content"]'),
              'call_page_links': ('/html/body/app-root/app-fastboot/'
                                  'app-dashboard/div[5]/div[1]/'
                                  'app-my-conversation/div/div/ul/li/'
                                  'app-conversation-list-item/div/a'),
              'more_details_button': ('/html/body/app-root/app-fastboot/'
                                      'app-dashboard/div[5]/div[1]/'
                                      'app-conversation-detail/div/div/div[1]/'
                                      'div/div/div[1]/div[3]/button'),
              'export_text_button': ('/html/body/div[6]/div/div/'
                                     'app-local-options-menu/div/ul/'
                                     'li[2]/button'),
              'continue_button': ('/html/body/div[6]/div[3]/div/'
                                  'app-export-transcript-overlay/div/div[1]/'
                                  'button[2]')}


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


def scroll(driver, timeout):
    """
    Scroll down webpage with infinite scroll.

    This function is a slightly modified version of the code from
    artjomb at https://gist.github.com/artjomb/07209e859f9bf0206f76.

    Parameters
    ----------
    driver : webdriver
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


def collect_video_links(driver, url):
    """
    Collect list of Otter.ai video page links.

    Parameters
    ----------
    driver : webdriver object
        Instantiated webdriver object for page navigation.
    url : string
        URL address for the Otter.ai page with all video conversations.

    Returns
    -------
    link_list : list
        List of url addresses to each individual video page on Otter.ai.

    """
    driver.get(url)
    (WebDriverWait(driver, 120).
     until(EC.
           presence_of_all_elements_located((By.XPATH,
                                             xpath_dict['all_convo_page']))))
    scroll(driver, 2)
    scroll(driver, 2)
    scroll(driver, 2)
    scroll(driver, 2)
    scroll(driver, 2)
    link_webelement_list = (driver.
                            find_elements_by_xpath(
                                xpath_dict['call_page_links']))
    link_list = [link_webelement_list[j].get_attribute('href')
                 for j in range(len(link_webelement_list))]
    i = 0
    while i < 1:
        try:
            scroll(driver, 2)
            scroll(driver, 2)
            scroll(driver, 2)
            scroll(driver, 2)
            scroll(driver, 2)
            last_len = len(link_list)
            link_webelement_list = (driver.
                                    find_elements_by_xpath(
                                        xpath_dict['call_page_links']))
            link_list = [link_webelement_list[j].get_attribute('href')
                         for j in range(len(link_webelement_list))]
            if last_len >= len(link_list):
                i = 1
        except Exception:
            print(Exception)
            i = 1
    return link_list


def download_transcripts(driver, link_list):
    """
    Download transcripts for each video as .txt files.

    Parameters
    ----------
    driver : webdriver object
        Instantiated webdriver object for page navigation.
    link_list : TYPE
        List of url addresses to each individual video page on Otter.ai.

    Returns
    -------
    None.

    """
    for link in link_list:
        driver.get(link)
        (WebDriverWait(driver, 10).
         until(EC.
               presence_of_all_elements_located((By.
                                                 XPATH,
                                                 xpath_dict[
                                                     'more_details_button'])
                                                )))
        more_details_button = (driver.
                               find_element_by_xpath(
                                   xpath_dict['more_details_button']))
        more_details_button.click()
        (WebDriverWait(driver, 10).
         until(EC.
               element_to_be_clickable((By.XPATH,
                                        xpath_dict['export_text_button']))))
        export_text_button = (driver.
                              find_element_by_xpath(
                                  xpath_dict['export_text_button']))
        export_text_button.click()
        (WebDriverWait(driver, 10).
         until(EC.
               element_to_be_clickable((By.XPATH,
                                        xpath_dict['continue_button']))))
        continue_button = (driver.
                           find_element_by_xpath(xpath_dict['continue_button']))
        continue_button.click()
        time.sleep(5)
        print(f'Completed with link: {link}')
    return


def main():
    driver = launch_webdriver()
    url = 'https://otter.ai/all-notes'
    link_list = collect_video_links(driver, url)
    download_transcripts(driver, link_list)


if __name__ == "__main__":
    main(driver)
