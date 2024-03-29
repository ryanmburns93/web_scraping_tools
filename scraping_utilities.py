# -*- coding: utf-8 -*-
"""
Created on Wed Sep 15 08:55:11 2021

@author: Ryan
"""
import time
import os
import ctypes
from ctypes import windll, wintypes
from uuid import UUID
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager


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


def launch_webdriver(headless=False):
    """
    Instantiate the webdriver application with explicitly defined options.
    Helper function.

    Options set webdriver to maximized window at start, loads and saves into the specified
    chromedriver user profile, removes automation warning from screen, and disables excessive
    error and warning logging.

    Parameters
    ----------
    headless : bool, optional
        Boolean indicator for whether to launch the chromedriver instance as headless.
        The default is False.

    Returns
    -------
    driver : webdriver
        Initialized webdriver for retrieving and manipulating web pages.

    """
    options = ChromeOptions()
    options.add_argument("--log-level=3")  # disable Info/Error/Warning in Chrome Driver
    if headless:
        options.headless = True # run driver as invisible to user
    else:
        options.add_argument("start-maximized")
    options.add_experimental_option('excludeSwitches', ['load-extension',
                                                        'enable-automation', # remove automated-browser warning on top of browser
                                                        'enable-logging']) # disable logging
    capabilities = webdriver.DesiredCapabilities.CHROME.copy()
    # capabilities['goog:loggingPrefs'] = {'performance': 'ALL'} # enable ability to log network traffic
    s = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s, options=options, desired_capabilities=capabilities)
    return driver
