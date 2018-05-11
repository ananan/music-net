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

        super(MusicCrawler, self).__init__(self.driver_path, self.headless, self.ignore_exception)
        self.singer_base_url = 'https://music.163.com/artist?id='
        self.songs_base_url = 'https://music.163.com/song?id='

    @try_again
    def get_frame(self, url):
        """
            获取contentFrame，网页版的网易云音乐的内容放在contentFrame中，requests无法爬取
        :param url: source url
        :return: contentFrame
        """
        self.browser.get(url)
        # 显式等待5s，直到可以切换到conentFrame
        self.until(self.EC.frame_to_be_available_and_switch_to_it('contentFrame'))
        return self.browser

    def get_singers_by_typeID(self, type_id):
        """
            根据歌手类型ID获取对应的歌手名和id, 根据id可以获取其主页url
        :param type_id: 歌手所属类型ID
        :return: （singer_name，singer_id）的列表对象
        """
        url = 'https://music.163.com/#/discover/artist/cat?id={}'.format(type_id)
        print('get all singer by type: ', url)
        contentFrame = self.get_frame(url)
        ul = contentFrame.find_element_by_id('m-artist-box')
        a_tags = ul.find_elements_by_xpath('//a[@class="nm nm-icn f-thide s-fc0"]')
        return [(a.text, a.get_attribute('href').split('=')[1]) for a in a_tags]

    def get_songs_by_singerID(self, singer_id):
        """
            爬取歌手主页内容
        :param singer_id: 歌手id, 根据此id可以获取歌手主页内容
        :return:
            pic_url: 歌手头像
            songs_list: 歌曲id列表
            album_list: 专辑id列表 [{'title':专辑名, 'id': 专辑id, cover: 封面链接},...]
            mv_list: MV列表 [{'id': MV的id, 'title': MV名},...]
            info: 歌手详细介绍
        """
        url = 'https://music.163.com/artist?id={}'.format(singer_id)
        print('get singer page from url: ',url)
        contentFrame = self.get_frame(url)

        # 获取歌手50首热门歌曲的id
        tbody = contentFrame.find_element_by_tag_name('tbody')
        songs_list = [a.get_attribute('href').split('=')[1] for a in tbody.find_elements_by_tag_name('a')[::3]]

        # 获取歌手封面图像url
        img_tag = contentFrame.find_element_by_xpath('//div[@class="n-artist f-cb"]').find_element_by_tag_name('img')
        pic_url = img_tag.get_attribute('src').split('?')[0]

        # 获取歌手的专辑，有可能没有专辑
        album_list = []
        contentFrame.find_element_by_xpath('//ul[@id="m_tabs"]').find_elements_by_tag_name('li')[1].click()
        try:
            divs = self.until(self.EC.visibility_of_all_elements_located((self.By.XPATH,
                                                                          '//div[@class="u-cover u-cover-alb3"]')))
            for div in divs:
                album_cover = div.find_element_by_tag_name('img').get_attribute('src').split('?')[0]
                album_title = div.get_attribute('title')
                album_id = div.find_element_by_tag_name('a').get_attribute('href').split('=')[1]
                album_list.append({'cover': album_cover, 'title': album_title, 'id': album_id})
        except self.TimeoutException:
            print('No album for this singer: ', contentFrame.title)

        # 获取歌手的相关MV, 有可能没有MV
        mv_list = []
        contentFrame.find_element_by_xpath('//ul[@id="m_tabs"]').find_elements_by_tag_name('li')[2].click()
        try:
            ps = self.until(self.EC.visibility_of_all_elements_located((self.By.XPATH, '//p[@class="dec"]')), 'no MV')
            for p in ps:
                mv_id = p.find_element_by_tag_name('a').get_attribute('href').split('=')[1]
                mv_title = p.find_element_by_tag_name('a').text
                mv_list.append({'id': mv_id, 'title': mv_title})
        except self.TimeoutException:
            print('No MV for this singer: ', contentFrame.title)

        # 获取歌手简介，有可能不存在
        contentFrame.find_element_by_xpath('//ul[@id="m_tabs"]').find_elements_by_tag_name('li')[3].click()
        try:
            info = self.until(self.EC.visibility_of_element_located((self.By.XPATH, '//div[@class="n-artdesc"]'))).text
        except self.TimeoutException:
            print('No info for this singer: ', contentFrame.title)
            info = '暂无介绍'

        return pic_url, songs_list, album_list, mv_list, info


if __name__ == '__main__':
    with MusicCrawler(driver_path='/usr/local/bin/chromedriver', headless=True) as crawler:
        config = {
                  '4002':'华语女歌手',
                }
        for key, value in config.items():
            print(key, '---------------', value)
            for singer_name, singer_id in crawler.get_singers_by_typeID(key)[:2]:
                print(singer_name, singer_id)

                singer_pic, songs_list, album_list, mv_list, info = crawler.get_songs_by_singerID(singer_id)
                print('singer name: {}, singer_pic: {}, info: {}'.format(singer_name, singer_pic, info))
                print(songs_list, mv_list, album_list)

            # db.singer.insert_one({'name': res['singer'],
            #                       'url': res['url'],
            #                       'pic': pic,
            #                       'type': value,
            #                       'songs': songs,
            #                       'info': desc})







