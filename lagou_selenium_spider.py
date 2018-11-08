# encoding: utf-8
"""
@author: shuxiangguo
@file: lagou_selenium.py
@time: 2018-11-07 16:32:13
"""


# 目的：爬取拉钩网python职位信息
# 思路：首先获取搜索python后的页面信息，通过该页面获取到第一页所有带
# 爬取具体职位信息的url链接，然后逐一爬取。然后依次爬取第2 3~N页信息
# 通过selenium模拟浏览器爬取，注意不要爬取太快
# 使用lxml解析网页源代码

from selenium import webdriver
from lxml import etree
import re
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class LagouSpider(object):
	def __init__(self):
		self.driver = webdriver.Chrome()
		self.url = "https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput="
		self.positions = []

	def run(self):
		self.driver.get(self.url)
		while True:
			source = self.driver.page_source
			# 放置爬取过快，页面未渲染好
			WebDriverWait(driver=self.driver, timeout=10).until(
				EC.presence_of_element_located((By.XPATH, "//div[@class='pager_container']/span[@class='pager_next ']"))
			)
			self.parse_list_page(source)
			next_btn = self.driver.find_element_by_xpath("//div[@class='pager_container']/span[@class='pager_next ']")
			if "pager_next_disabled" in next_btn.get_attribute("class"):
				break
			else:
				# print(next_btn)
				next_btn.click()

	def parse_list_page(self, source):
		html = etree.HTML(source)
		links = html.xpath("//a[@class='position_link']//@href")
		for link in links:
			self.request_detail_page(link)
			time.sleep(1)

	def request_detail_page(self, url):
		# self.driver.get(url)
		self.driver.execute_script("window.open('%s')" % url)
		self.driver.switch_to.window(self.driver.window_handles[1])

		# 放置爬取过快，页面未渲染好
		WebDriverWait(self.driver, timeout=10).until(

			# 下面的xpath不能包含text()
			EC.presence_of_element_located((By.XPATH, "//span[@class='name']"))
		)
		source = self.driver.page_source
		self.parse_detail_page(source)

		# 关闭当前这个详情页
		self.driver.close()
		# 切换回职位列表
		self.driver.switch_to.window(self.driver.window_handles[0])

	def parse_detail_page(self, source):
		html = etree.HTML(source)

		info = {}

		position_name = html.xpath("//span[@class='name']/text()")[0]
		# print(position_name)
		job_request_spans = html.xpath("//dd[@class='job_request']//span")
		salary = re.sub(r"[\s/]", "", job_request_spans[0].xpath(".//text()")[0].strip())
		city = re.sub(r"[\s/]", "", job_request_spans[1].xpath(".//text()")[0].strip())
		experience = re.sub(r"[\s/]", "", job_request_spans[2].xpath(".//text()")[0].strip())
		education = re.sub(r"[\s/]", "", job_request_spans[3].xpath(".//text()")[0].strip())
		job_desc = "".join(html.xpath(".//dd[@class='job_bt']//text()")).strip()
		company_name = html.xpath("//h2[@class='fl']//text()")[0].strip()
		info['salary'] = salary
		info['city'] = city
		info['experience'] = experience
		info['educetion'] = education
		info['job_desc'] = job_desc
		info['company_name'] = company_name
		print(info)
		self.positions.append(info)


def main():
	spider = LagouSpider()
	spider.run()


if __name__ == '__main__':
	main()
