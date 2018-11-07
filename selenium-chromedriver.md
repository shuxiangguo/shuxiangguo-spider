# Selenium和ChromeDriver模拟浏览器
> 教程地址：http://selenium-python.readthedocs.io/installation.html#introducti

模拟浏览器
用selenium和ChromeDriver可以模拟浏览器的功能，发起请求。

例：

from selenium import webdriver

driver = webdriver.Chrome()
driver.get('https://www.baidu.com')
运行 上面的代码，会出现一个Chrome页面，并打开百度首页www.baidu.com。

若想要模拟在输入框中输入关键字，则应先通过获取元素的方法获取输入框元素，然后发送请求的关键字。

获取节点的方法有很多，具体可以通过输入driver. 之后会给出提示，如find_element_by_class_name()、find_element_by_id()等

如：input_tags = driver.find_element_by_class_name('s_ipt')
通过方法send_keys()向输入框输入关键字：

input_keys.send_keys('python')
完整代码：

from selenium import webdrive
driver = webdriver.Chrome()
driver.get('https://www.baidu.com')
input_tags = driver.find_element_by_class_name('s_ipt')
input_tags.send_keys('python'
Tips:

1.如果只是想要解析网页中的数据，那么推荐将网页源代码扔给lxml来解析，因为lxml底层用的是C语言，所以解释效率会更高

2.如果想要对元素进行一些操作，如给文本框输入值，或者是点击某个按钮，那么必须使用selenium给我们提供的查找元素的方法，因为方法send_keys()只在这些下面可用。代码如下：

from selenium import webdriver
from lxml import etree

driver = webdriver.Chrome()

# html = etree.HTML(driver.page_source)
# html.xpath("")
操作表单元素：

操作输入框：分为两步：

第一步：找到这个元素。

使用send_keys(value)，将数据填充进去。示例代码如下：

        input_tag = driver.find_element_by_class_name('s_ipt')
        # 使用send_keys()方法向表单发送数据
        input_tag.send_keys('hello world')
操作CheckBox：因为要选中checkbox标签，在网页中是通过鼠标点击的。所以要选中CheckBox，首先获取到这个标签，然后执行click事件，代码如下：
from selenium import webdriver

driver = webdriver.Chrome()
driver.get("https://www.douban.com/")

remberme = driver.find_element_by_id('form_remember')
remberme.click()
3.选择select ：select元素不能直接点击因为点击后还需要选中元素。这时候selenium就专门为select标签提供了一个类

selenium.webdriver.support.ui.Select

将获取到的元素当成参数传到这个类中，创建这个对象。以后就可以使用这个对象进行选择了。示例代码如下：

from selenium.webdriver.support.ui import Select
 # 选中这个标签，然后使用Select创建对象
 selectTag = Select(driver.find_element_by_name("jumpMenu"))
 # 根据索引选择
 selectTag.select_by_index(1)
 # 根据值选择
 selectTag.select_by_value("http://www.95yueba.com")
 # 根据可视的文本选择
 selectTag.select_by_visible_text("95秀客户端")
 # 取消选中所有选项
 selectTag.deselect_all()
4，操作按钮：操作按钮有很多种方式。比如单击、右击、双击等。这里讲一个最常用的。就是点击。直接调用

click函数就可以了。示例代码如下：

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

driver = webdriver.Chrome()
driver.get("https://www.baidu.com")


input_tag = driver.find_element_by_id('kw')
submit_tag = driver.find_element_by_id('su')

action = ActionChains(driver)
action.move_to_element(input_tag)
action.send_keys_to_element(input_tag, "python")
action.move_to_element(submit_tag)
action.click(submit_tag)
action.perform()
操作Cookie
获取所有的cookie：
for cookie in driver.get_cookies():
     print(cookie)
2.根据cookie的key获取value

value = driver.get_cookie(key)
删除所有的cookie
driver.delete_all_cookie()
删除某个cookie
 driver.delete_cookie(key
页面等待
现在的网页越来越多采用了 Ajax 技术，这样程序便不能确定何时某个元素完全加载出来了。如果实际页面等待时间过长导致某个dom元素还没出来，但是你的代码直接使用了这个WebElement，那么就会抛出NullPointer的异常。为了解决这个问题。所以 Selenium 提供了两种等待方式：一种是隐式等待、一种是显式等待。

隐式等待：调用driver.implicitly_wait。那么在获取不可用的元素之前，会先等待10秒中的时间。示例代码如下：
from selenium import webdriver

driver = webdriver.Chrome()
driver.get("https://www.douban.com")

# driver.implicitly_wait(10)
显示等待：显示等待是表明某个条件成立后才执行获取元素的操作。也可以在等待的时候指定一个最大的时间，如果超过这个时间那么就抛出一个异常。显示等待应该使用selenium.webdriver.support.excepted_conditions期望的条件selenium.webdriver.support.ui.WebDriverWait来配合完成。示例代码如下：
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("https://www.douban.com")

element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, 'form_email'))
)
print(element)
3.一些其他的等待条件：

presence_of_element_located：某个元素已经加载完毕了。
presence_of_all_emement_located：网页中所有满足条件的元素都加载完毕了。
element_to_be_cliable：某个元素是可以点击了。

更多条件请参考：http://selenium-python.readthedocs.io/waits.html

切换页面
可以通过execute_script()函数执行js代码，例：

driver.execute_script("window.open('https://www.douban.com')")
有时候窗口中有很多子tab页面。这时候肯定是需要进行切换的。selenium提供了一个叫做switch_to_window来进行切换，具体切换到哪个页面，可以从driver.window_handles中找到。示例代码如下：

设置代理IP
有时候频繁爬取一些网页。服务器发现你是爬虫后会封掉你的ip地址。这时候我们可以更改代理ip。更改代理ip，不同的浏览器有不同的实现方式。这里以Chrome浏览器为例来讲解：

from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument("--proxy-server=http://117.191.11.71:80")
driver = webdriver.Chrome(chrome_options=options)

driver.get('http://httpbin.org/ip')
WebElement元素

from selenium.webdriver.remote.webelement import WebElement类是每个获取出来的元素的所属类。 有一些常用的属性：

get_attribute：这个标签的某个属性的值。
screentshot：获取当前页面的截图。这个方法只能在driver上使用。driver的对象类，也是继承自WebElement。更多请阅读相关源代码。
