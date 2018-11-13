# encoding: utf-8
"""
@author: shuxiangguo
@file: boss_spider.py
@time: 2018-11-12 23:44:30
"""


# 爬取boss直聘网站搜索python关键字的职位信息，保存到csv文件
import time
import re
import csv
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from lxml import etree


class bossSpider(object):
	def __init__(self, url, writer):
		self.url = url
		self.driver = webdriver.Chrome()
		self.writer = writer

	def run(self):
		self.driver.get(self.url)
		while True:
			page_source = self.driver.page_source
			# 等待页面加载完成
			WebDriverWait(self.driver, 1000).until(
				EC.presence_of_element_located((By.XPATH, "//div[@class='page']//a[@class='next']"))
			)
			self.parse_list_page(page_source)

			# break 测试用
			next_btn = self.driver.find_element_by_xpath("//div[@class='page']//a[@class='next']")
			if "disabled" in next_btn.get_attribute('class'):
				break
			else:
				next_btn.click()

	def parse_list_page(self, page_source):
		html = etree.HTML(page_source)
		link_urls = html.xpath(".//ul//li//div[@class='info-primary']/h3/a/@href")
		for link_url in link_urls:
			link_url = "https://www.zhipin.com" + link_url
			self.request_detail_page(link_url)
			# break 测试用
			time.sleep(1)

	def request_detail_page(self, url):
		# 打开新的职位详情页
		self.driver.execute_script("window.open('%s')" % url)
		print(url)

		# 跳转到职位详情页
		self.driver.switch_to_window(self.driver.window_handles[1])

		# 防止爬取过快，页面未渲染好，所以执行等待
		WebDriverWait(self.driver, 1000).until(
			EC.presence_of_element_located((By.XPATH, ".//div[@class='info-primary']//div[@class='name']"))
		)

		# 获取该页面源代码
		source_page = self.driver.page_source
		self.parse_detail_page(source_page, self.writer)

		# 关闭当前页
		self.driver.close()
		# 返回到职位搜索页
		self.driver.switch_to.window(self.driver.window_handles[0])

	def parse_detail_page(self, source_page, writer):
		html = etree.HTML(source_page)

		job_info = {}
		url = self.driver.current_url
		position_name = html.xpath(".//div[@class='job-banner']//div[@class='info-primary']//div[@class='name']/h1/text()")[0]
		# print(position_name)
		salary = re.sub(r"[\s/]", "", html.xpath(".//div[@class='job-banner']//div[@class='info-primary']//div[@class='name']/span/text()")[0].strip())
		# print(salary)
		city_exp_edu_info = html.xpath(".//div[@class='job-banner']//div[@class='info-primary']//p//text()")
		# print(city_exp_edu_info)
		city = re.sub(r"[城市：\s]", "", str(city_exp_edu_info[0]))
		experience = re.sub(r"[经验：]", "", str(city_exp_edu_info[1]))
		education = re.sub(r"[学历：]", "", str(city_exp_edu_info[2]))
		# print(city, experience, education)
		job_dec = ",".join(html.xpath(".//div[@class='job-box']//div[@class='job-sec'][1]/div//text()")).strip(	)
		print(job_dec)
		print("#"*20)
		job_info['url'] = url
		job_info['positin_name'] = position_name
		job_info['salary'] = salary
		job_info['city'] = city
		job_info['experience'] = experience
		job_info['education'] = education
		job_info['job_dec'] = job_dec
		writer.writerow((url, position_name, salary, city, experience, education,job_dec))



def main():

	fp = open('job_info.csv', 'a', newline='', encoding='utf-8')
	writer = csv.writer(fp)
	writer.writerow(("url", 'position_name', 'salary', 'city', 'experience', 'education', 'job_dec'))
	url = "https://www.zhipin.com/job_detail/?query=python&scity=101190400&industry=&position="
	spider = bossSpider(url, writer)
	spider.run()


if __name__ == '__main__':
	main()
