import json
import os  # 导入 os 模块，用于操作文件路径等
import re  # 导入 re 模块，用于正则表达式操作

import pandas as pd  # 导入 pandas 库，用于数据处理和分析
from bs4 import BeautifulSoup  # 导入 BeautifulSoup 类，用于解析 HTML
from lxml import etree  # 导入 etree 模块，用于解析 XML
from selenium import webdriver  # 导入 webdriver 类，用于控制浏览器
from selenium.webdriver.chrome.options import Options  # 导入 Options 类，用于设置 Chrome 浏览器选项
from selenium.webdriver.common.by import By  # 导入 By 类，用于定位元素
import time  # 导入 time 模块，用于操作时间
# 导入PDF模块
from fpdf import FPDF
# 导入翻译模块
from googletrans import Translator


def get_json_str_from_script(script):
    json_text = script.text
    start = json_text.find('__APOLLO_STATE__')
    end = json_text.rfind('}')
    return json_text[start:end + 1]


class Demo(object):

    def __init__(self):
        self.driver = {}  # 创建一个空字典，用于存储 WebDriver 实例
        self.data_list = []   # 创建一个空列表，用于存储解析的数据

    def run(self):
        option = webdriver.ChromeOptions()  # 创建 ChromeOptions 实例
        # 设置 ChromeOptions 的一些选项
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        option.add_experimental_option('detach', True)
        option.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(options=option)

        script = 'Object.defineProperty(navigator, "webdriver", {get: () => false,});'
        self.driver.execute_script(script)   # 执行 JavaScript 代码，禁用 WebDriver 检测

        url = 'https://medium.com/?tag=software-engineerin'  #禁用 WebDriver 检测
        self.driver.get(url)   # 打开网页

        count = 10*1  # 当前数量×页
        start = time.time()  # 记录开始时间
        # TODO 多线程分批次加载
        while True:
            soup = BeautifulSoup(self.driver.page_source, 'lxml')   # 使用 BeautifulSoup 解析页
            soup_item = soup.select('.pw-homefeed-item')   # 通过 CSS 选择器获取文章元素列表
            # 使用len函数获取列表的长度，即筛选出的元素的个数
            print('current num：', len(soup_item))
            if len(soup_item) >= count:  # 加载10页,超过100就不加了
                break

            js = "window.scrollBy(0, 2000)"  # 向下滑动2000个像素 刚好10条
            self.driver.execute_script(js)

        print('load finish...')
        end = time.time()  # 记录结束时间
        print("耗时: {:.2f}秒".format(end - start))  # 打印耗时

        # 解析数据  TODO 又要加载
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        soup_item = soup.select('.pw-homefeed-item')   # 通过 CSS 选择器获取文章元素列表

        first_item = soup_item[0]
        data = {}

        # TODO 图片
        url = first_item.select('h2')[0].parent['href']  # 找到H2的父节点 获取文章链接
        if 'https://' not in url:
            data['url'] = 'https://medium.com' + url  # 如果链接不是完整的 URL，则补全
        else:
            data['url'] = url  # 详情链接

        self.get_detail(data)  # 调用 get_detail 方法，获取文章的详细信息

        for si in soup_item:
            data = {}

            # TODO 图片
            url = si.select('h2')[0].parent['href']   # 找到H2的父节点 获取文章链接
            if 'https://' not in url:
                data['url'] = 'https://medium.com' + url   # 如果链接不是完整的 URL，则补全
            else:
                data['url'] = url  # 详情链接

            self.get_detail(data)   # 调用 get_detail 方法，获取文章的详细信息


    def get_detail(self, data):
        option = webdriver.ChromeOptions()
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        option.add_experimental_option('detach', True)
        option.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(options=option)

        script = 'Object.defineProperty(navigator, "webdriver", {get: () => false,});'
        self.driver.execute_script(script)

        try:
            print(data['url'])
            self.driver.get(data['url'])  # 获取详情页

            soup = BeautifulSoup(self.driver.page_source, 'lxml')

            data['title'] = soup.select('h1')[0].text  # 标题
            data['like_count'] = soup.select('.bl .be.b.du.z.dt')[0].text  # 点赞数
            content = soup.select('article')[0].text

            data['content'] = content[content.index('ListenShare')+11:]  # 文章内容
            print(data)
            self.data_list.append(data)
        except:
            pass

    def get_detail_url(self, url):
        like_count = -1  # 初始化 like_count
        paragraph = []  # 初始化 paragraph
        try:
            option = webdriver.ChromeOptions()
            option.add_experimental_option('excludeSwitches', ['enable-automation'])
            option.add_experimental_option('detach', True)
            option.add_argument('--no-sandbox')
            self.driver = webdriver.Chrome(options=option)
            script = 'Object.defineProperty(navigator, "webdriver", {get: () => false,});'
            self.driver.execute_script(script)   # 执行 JavaScript 代码，禁用 WebDriver 检测
            print('url', url)
            # TODO 耗时
            self.driver.get(url)  # 获取详情页
            soup = BeautifulSoup(self.driver.page_source, 'lxml')
            title = soup.select('h1')[0].text  # 标题
            print('title', title)
            subtitle = soup.select('.pw-subtitle-paragraph')[0].text  # 子标题
            # print('subtitle', subtitle)
            like_count = soup.select('.bl .be.b.du.z.dt')[0].text  # 点赞数
            content = soup.select('article')[0].text   # 文章内容
            # print('content', content)
            # print('like_count', like_count)
            scripts = soup.find_all('script')
            scripts1 = soup.select('.pw-post-body-paragraph')
            # 定义一个paragraph数组循环存储script中的内容
            paragraph = []
            for script in scripts1:
                # print(script.text)
                paragraph.append(script.text)
        except:
            pass
        finally:
            self.driver.quit()
        return paragraph, like_count


        # # TODO 遍历太慢了
        # for script in scripts1:
        #     script_content = script.string
        #     if 'window.__APOLLO_STATE__' in script_content:
        #         # 提取 window.__APOLLO_STATE__ 的值
        #         start_index = script_content.find('{')
        #         end_index = script_content.rfind('}') + 1
        #         json_str = script_content[start_index:end_index]
        #         data = json.loads(json_str)
        #         # 在 data 中可以访问 window.__APOLLO_STATE__ 的内容
        #         # 例如：data['window']['__APOLLO_STATE__']
        #         # 查找所有以 "Paragraph" 开头的对象
        #         paragraph_objects = []
        #         for key, value in data.items():
        #             if key.startswith('Paragraph'):
        #                 paragraph_objects.append(value['text'])
        #         # 打印符合条件的对象
        #         for obj in paragraph_objects:
        #             print(obj)



    # 定义翻译函数
    def translate(self, text, dest='zh-cn'):
        # 创建翻译器对象
        translator = Translator()
        # 调用翻译方法
        result = translator.translate(text, dest=dest)
        # 返回翻译后的文本
        return result.text





if __name__ == '__main__':
    d = Demo()
    d.run()
    # d.get_top10()
    # d.get_detail_url('https://medium.com/@yuriminamide0509/earthquakes-in-japan-we-are-always-prepared-0957c25ecf37')

