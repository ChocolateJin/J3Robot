from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
driver = webdriver.Edge()
 
driver.get('https://portal.sysu.edu.cn/')
sleep(5)
driver.add_cookie({
    'name':'JSESSIONID',
    'value':'58E8C1D05848368E3CA203F88CCFC8A2',
    'domain':'https://cas.sysu.edu.cn'
    })
A=driver.find_element_by_class_name('ant-btn.index-submit-3jXSy.ant-btn-primary.ant-btn-lg')
A.click()


