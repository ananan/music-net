#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/9 14:42
# @Author  : Peter Yang
# @Contact : 13yhyang1@gmail.com
# @File    : music_crawler.py

from music_net.utils.crawler import Crawler, try_again


class MusicCrawler(Crawler):
    """
    NetEase Music Crawler:

    """
    def __init__(self, driver_path='/usr/bin/chromedriver', headless=False, ignore_exception=False):
        self.driver_path = driver_path
        self.headless = headless
        self.ignore_exception = ignore_exception
        super(Crawler, self).__init__(self.driver_path, self.headless, self.ignore_exception)
        self.singer_base_url = 'https://music.163.com/artist?id='
        self.songs_base_url = 'https://music.163.com/song?id='

    @try_again
    def get_singers(self, url):
        """
            this function get the most popular singer
        :param url: singer type url
        :return: singers, urls
        """
        self.browser.get(url)
        self.until(self.EC.frame_to_be_available_and_switch_to_it('contentFrame'))

        ul = self.browser.find_element_by_id('m-artist-box')
        a_tags = ul.find_elements_by_xpath('//a[@class="nm nm-icn f-thide s-fc0"]')
        return [{'singer': a.text, 'url': a.get_attribute('href')} for a in a_tags]

    def get_songs_by_singer(self, url):
        self.browser.get(url)
        self.browser.switch_to.frame('contentFrame')
        tbody = self.browser.find_element_by_tag_name('tbody')
        songs = [a.get_attribute('href').split('=')[1] for a in tbody.find_elements_by_tag_name('a')[::3]]
        pic = self.browser.find_element_by_xpath('//div[@class="n-artist f-cb"]').find_element_by_tag_name('img').get_attribute('src')
        self.browser.find_element_by_xpath('//ul[@id="m_tabs"]').find_elements_by_tag_name('li')[-1].click()
        self.browser.implicitly_wait(1)
        try:
            desc = self.browser.find_element_by_class_name('n-artdesc').text
        except Exception as e:
            print(e)
            desc = 'no info !'
        return pic,songs, desc


if __name__ == '__main__':
    crawler = Crawler()
    config = {
              '4001':'其他男歌手',
              '4002':'其他女歌手',
              '4003':'其他组合/乐队'
            }
    for key, value in config.items():
        print(key, '---------------', value)
        for res in crawler.get_singers('https://music.163.com/#/discover/artist/cat?id={}'.format(key)):
            print(res['singer'], res['url'])
            try:
                pic, songs, desc = crawler.get_songs_by_singer(res['url'])
            except Exception as e:
                print(e)
                continue
            print(res['singer'], desc)
            # db.singer.insert_one({'name': res['singer'],
            #                       'url': res['url'],
            #                       'pic': pic,
            #                       'type': value,
            #                       'songs': songs,
            #                       'info': desc})







