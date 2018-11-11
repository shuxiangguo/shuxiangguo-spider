#爬虫未完成等待进一步完善！！！！！！！！！！！！！！！！！！！！

# encoding: utf-8
"""
@author: shuxiangguo
@file: spider.py
@time: 2018-11-08 17:32:23
"""

# 使用selenium和chromedriver来实现12306抢票功能

# 1.让浏览器打开12306登录界面，然后手动进行登录
# 2.登录完成后让浏览器跳转到购票的界面
# 3.手动输入出发地、目的地、出发日期	，检测到以上三个信息都输入完成后，然后找到
# 查询按钮，执行点击事件，进行车次查询。
# 4.查找我们需要的车次，然后看对应的席位是否还有余票，（有、数字），找到这个车次的预定按钮
# 然后执行点击事件，如果没有出现以上俩个（有、数字），那么我们就循环这个查询工作
# 5.一旦检测到有票（有、数字），那么执行预定按钮的点击事件，来到预定的界面后，找到对应的乘客，
# 然后执行这个乘客的CheckBox，然后执行点击事件，再找到提交订单的按钮，执行点击事件
# 6.点击提交订单按钮后，会弹出一个确认的对话框，然后找到确认按钮，执行点击事件，这样就完成了抢票

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



class QiangPiao(object):
	def __init__(self):
		self.driver = webdriver.Chrome()
		self.login_url = "https://kyfw.12306.cn/otn/resources/login.html"
		self.initmy_url = "https://kyfw.12306.cn/otn/view/index.html"
		self.search_url = "https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc"
		self.passenger_url = "https://kyfw.12306.cn/otn/confirmPassenger/initDc"

	def wait_input(self):
		self.from_station = input("出发地：")
		self.dest_station = input("目的地：")
		self.depart_time = input("出发时间: ")
		self.passengers = input("乘客姓名:(如有多个乘客，用英文都好隔开)".split(","))
		self.trains = input("车次:(如有多个车次，用英文逗号隔开)".split(","))

	def _login(self):
		self.driver.get(self.login_url)
		# 显示等待
		WebDriverWait(self.driver, 1000).until(
			EC.url_to_be(self.initmy_url)
		)
		print('Login success!')


	# 需要分析具体页面信息
	def _order_ticket(self):
		# 跳转到车票查询页面
		self.driver.get(self.search_url)

		# 等待出发地是否正确
		WebDriverWait(self.driver, 1000).until(
			EC.text_to_be_present_in_element_value((By.ID, "fromStationText"), self.from_station)
		)

		# 等待目的地是否正确
		WebDriverWait(self.driver, 1000).until(
			EC.text_to_be_present_in_element_value((By.ID, "toStationText"), self.dest_station)
		)

		# 等待日期是否正确
		WebDriverWait(self.driver, 1000).until(
			EC.text_to_be_present_in_element_value((By.ID, "train_date"), self.depart_time)
		)

		# 等待查询按钮是否可用
		WebDriverWait(self.driver, 1000).until(
			EC.element_to_be_clickable((By.ID, "query_ticket"))
		)

		# 如果能被点击，则找到这个查询按钮，执行点击事件
		searchBtn = self.driver.find_element_by_id("query_ticket")
		searchBtn.click()

		# 点击完之后并不能立刻执行下一步，得确认列车信息加载出来了
		WebDriverWait(self.driver, 1000).until(
			EC.presence_of_element_located((By.XPATH, ".//tbody[@id='queryLeftTable']/tr"))
		)

		# 找到所有没有datatran属性的tr标签，这些标签存储了车次信息
		tr_list = self.driver.find_elements_by_xpath(".//tbody[@id='queryLeftTable']/tr[not (@datatran)]")

		# 遍历所有满足条件的tr标签
		for tr in tr_list:
			train_number = tr.find_element_by_class_name("number").text
			print(train_number)
			if train_number in self.trains:
				left_ticket = tr.find_element_by_xpath("./td[4]").text
				if left_ticket == "有" or left_ticket.isdigit():
					order_btn = tr.find_element_by_class_name("btn72")
					order_btn.click()

					# 等待是否来到确认乘客的页面
					WebDriverWait(self.driver, 1000).until(
						EC.url_to_be(self.passenger_url)
					)

					# users_li = self.driver.find_elements_by_xpath(".//ul[@id='nomal_passenger_id']//li")
					# for user in users_li:
					# 	print(user.text)
					# 	if user.text in self.passengers:
					# 		user.find_element_by_xpath("./label").__setattr__("class", "colorA")
					# submit_btn = self.driver.find_element_by_xpath(".//div[@class='lay-btn']/a[@id='submitOrder_id']")
					# submit_btn.click()
					#爬虫未完成等待进一步完善！！！！！！！！！！！！！！！！！！！！

	def run(self):
		self.wait_input()
		self._login()
		self._order_ticket()

def main():
	spider = QiangPiao()
	spider.run()

if __name__ == '__main__':
	main()
