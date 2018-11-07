# encoding: utf-8
"""
@author: shuxiangguo
@file: lagou_selenium.py
@time: 2018-11-07 15:31:53
"""

import requests
from lxml import etree
import time
import re

headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
	'Referer': 'https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=',
	'Cookie': 'JSESSIONID=ABAAABAAAFCAAEG9493B8D684AA4F784118331596D6092A; _ga=GA1.2.2116619760.1540627605; user_trace_token=20181027160646-3fa7e102-d9bf-11e8-8232-5254005c3644; LGUID=20181027160646-3fa7e55a-d9bf-11e8-8232-5254005c3644; index_location_city=%E5%85%A8%E5%9B%BD; X_HTTP_TOKEN=5fa1c0fc3069a510b1f3b74d87bdf0f9; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22166b4c064565c8-0d315805c28162-9393265-921600-166b4c064571e9%22%2C%22%24device_id%22%3A%22166b4c064565c8-0d315805c28162-9393265-921600-166b4c064571e9%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; TG-TRACK-CODE=index_search; _gid=GA1.2.566468228.1541559981; PRE_UTM=; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1540627607,1540697568,1541560000; LGSID=20181107110642-2703e950-e23a-11e8-8eda-525400f775ce; PRE_HOST=cn.bing.com; PRE_SITE=https%3A%2F%2Fcn.bing.com%2F; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; _gat=1; LGRID=20181107111100-c0cc3de2-e23a-11e8-86f8-5254005c3644; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1541560258; SEARCH_ID=398db06e67ca4a2298c7372f07cee3f3'
}


def request_list_page():
	url = "https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false"


	data = {
		'first': False,
		'pn': 1,
		'kd': 'python'
	}

	for x in  range(1, 30):
		data['pn'] = x
		response = requests.post(url, headers=headers, data=data)
		result = response.json()

		positions = result['content']['positionResult']['result']
		for position in positions:
			positionId = position['positionId']
			position_url = "https://www.lagou.com/jobs/%s.html"%positionId
			parse_position_detail(position_url)
			break
		# 为了避免爬去太快被服务器屏蔽，可以用time模块sleep()一会
		time.sleep(1)
		break



def parse_position_detail(url):
	response = requests.get(url, headers=headers)
	text = response.text
	html = etree.HTML(text)

	info = {}

	position_name = html.xpath("//span[@class='name']/text()")[0]
	# print(position_name)
	job_request_spans = html.xpath("//dd[@class='job_request']//span")
	salary = re.sub(r"[\s/]", "", job_request_spans[0].xpath(".//text()")[0].strip())
	city = re.sub(r"[\s/]", "", job_request_spans[1].xpath(".//text()")[0].strip())
	experience = re.sub(r"[\s/]", "", job_request_spans[2].xpath(".//text()")[0].strip())
	education = re.sub(r"[\s/]", "", job_request_spans[3].xpath(".//text()")[0].strip())
	info['salary'] = salary
	info['city'] = city
	info['experience'] = experience
	info['educetion'] = education
	print(info)

	job_desc = "".join(html.xpath(".//dd[@class='job_bt']//text()")).strip()
	print(job_desc)




def main():
	request_list_page()


if __name__ == '__main__':
    main()
