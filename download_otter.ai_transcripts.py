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
from utilities import go_to_downloads, scroll


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
