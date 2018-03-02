import asyncio
import logging
import time

import requests
from selenium import webdriver
from selenium.webdriver.remote.remote_connection import LOGGER

from util import g_path, logger, get_extension


def download_img(url, title, idx):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
    }
    img_path = g_path("img", "{}{}{}".format(title, str(idx), get_extension(url)))
    if img_path.exists():
        return
    try:
        img = requests.get(url, headers=headers)
    except requests.exceptions.ConnectionError as err:
        logger.warning("conn_error:{}:{}".format(title, url))
        return
    if img.status_code != 200:
        logger.warning("wrong status {}:{}".format(title, url))
    else:
        with open(str(img_path), 'wb') as file:
            file.write(img.content)


class Browser:
    def __enter__(self):
        LOGGER.setLevel(logging.WARNING)
        self._browser = webdriver.Firefox()
        return self._browser

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._browser.quit()


class Roller:
    false_alarm_time = 2
    scroll_speed = 50

    def __init__(self, browser: webdriver.Firefox):
        self.last_height = 0
        self.browser = browser

    @property
    def _current_height(self):
        """
        get browser window scrollable height
        :param browser:
        :return:
        """
        length = self.browser.find_element_by_css_selector("body").get_attribute("scrollHeight")
        length = int(length)
        return length

    def _scroll_to(self):
        """
        :return: True if scroll to end and wait for self.false_alarm_time and still true
        """
        height = self._current_height
        for i in range(self.last_height, height, self.scroll_speed):
            self.browser.execute_script("window.scrollTo(0,{})".format(i))

        if self.last_height == height:
            # wait two second detect false alarm
            time.sleep(self.false_alarm_time)
            if self._current_height == self.last_height:
                # still the same
                return True

        self.last_height = height
        return False

    def scroll_to_end(self):
        while not self._scroll_to():
            continue


def download_gakki():
    url = "http://image.baidu.com/search/index?tn=baiduimage&ps=1&ct=201326592&lm=-1&cl=2&nc=1&ie=utf-8&word=gakki"

    with Browser() as browser:
        browser.get(url)
        Roller(browser).scroll_to_end()
        # browser.maximize_window()
        for idx, li in enumerate(browser.find_elements_by_css_selector("li.imgitem")):
            # noinspection PyStatementEffect
            li.location_once_scrolled_into_view
            title = li.get_attribute("data-title")  # type: str
            title = title.replace("/", "")
            title = title.replace(" ", "")
            url = li.get_attribute("data-objurl")
            if "http" in url:
                asyncio.get_event_loop().run_in_executor(None, download_img, url, title, idx)
            else:
                logger.warning("not img--------------------------------------------------------")
        browser.quit()


if __name__ == '__main__':
    download_gakki()
