import threading
import time
import re

from selenium import webdriver
# url=['https://weibo.com/p/1005051881797917/info?mod=pedit_more','https://weibo.com/p/1005051774676624/info?mod=pedit_more','https://weibo.com/p/1005051881797917/info?mod=pedit_more','https://weibo.com/p/1005051774676624/info?mod=pedit_more','https://weibo.com/p/1005051881797917/info?mod=pedit_more','https://weibo.com/p/1005051774676624/info?mod=pedit_more','https://weibo.com/p/1005051881797917/info?mod=pedit_more','https://weibo.com/p/1005051774676624/info?mod=pedit_more','https://weibo.com/p/1005051881797917/info?mod=pedit_more','https://weibo.com/p/1005051774676624/info?mod=pedit_more','https://weibo.com/p/1005051881797917/info?mod=pedit_more','https://weibo.com/p/1005051774676624/info?mod=pedit_more','https://weibo.com/p/1005051881797917/info?mod=pedit_more','https://weibo.com/p/1005051774676624/info?mod=pedit_more','https://weibo.com/p/1005051881797917/info?mod=pedit_more','https://weibo.com/p/1005051774676624/info?mod=pedit_more','https://weibo.com/p/1005051881797917/info?mod=pedit_more','https://weibo.com/p/1005051774676624/info?mod=pedit_more']
from selenium.common.exceptions import NoSuchElementException

urlString="//weibo.com/u/5620193879?refer_flag=1001030103_,//weibo.com/u/6511167221?refer_flag=1001030103_,//weibo.com/u/6320164045?refer_flag=1001030103_,//weibo.com/shandonglaiwuqishikong?refer_flag=1001030103_,//weibo.com/tianhuizixun?refer_flag=1001030103_,//weibo.com/u/3922193372?refer_flag=1001030103_,//weibo.com/302789756?refer_flag=1001030103_"
url=urlString.split(',')
print(url)

#初始化线程浏览器
def initBrowser():
    username = '66394638@qq.com'
    password = ''
    browser = webdriver.Firefox()
    browser = login_weibo(browser,username, password)
    print("浏览器初始化完成："+time.ctime())
    while len(url):
        threadUserInfo(browser)
    browser.close()


#该线程执行
def threadUserInfo(browser):
    userInfoURL = urlUserToUserInfo(browser)
    if userInfoURL is None:
        return
    browser.get(userInfoURL)
    time.sleep(3)
    try:
        getUserInfo(browser)
    except NoSuchElementException:
        print("获取详细信息异常，延长休眠时间1秒")
        time.sleep(1)


#获取用户信息
def getUserInfo(driver):
    xpath = driver.find_element_by_xpath("/html/head/title")
    print(xpath.parent.title)
    # 爬取关注数，粉丝数，微博数

    userInfoString={}
    userInfoString['title']=xpath.parent.title

    #关注数
    userInfoString['follow'] = driver.find_elements_by_class_name('W_f18')[0].text
    print("关注数： "+userInfoString['follow'])

    #粉丝数
    userInfoString['fans'] = driver.find_elements_by_class_name('W_f18')[1].text
    print("粉丝数： "+userInfoString['fans'])

    #微博数
    userInfoString['weibonum'] = driver.find_elements_by_class_name('W_f18')[2].text
    print("微博数： "+userInfoString['weibonum'])


    # 获取等级信息
    # by_xpath = driver.find_element_by_xpath('//p[@class="level_info"]/span[@class="info"]/span[@class="S_txt1"]/text()')
    # strip = by_xpath.xpath('string(.)').encode('utf-8').strip()
    # userInfoString['grading '] = by_xpath.text
    # print("等级： " + userInfoString['grading'])
    # 获取基本信息


    # print(person_info_dict)
    # return person_info_dict

# 设置代理，登录
def login_weibo(driver,username,password):
    # driver = webdriver.Firefox()
    driver.get("https://weibo.com/")

    time.sleep(10)
    # 定位用户名密码文本框
    username_field = driver.find_element_by_xpath('//*[@id="loginname"]')
    password_field = driver.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[2]/div/input')

    #清空input数据
    username_field.clear()
    # 输入用户名密码:
    username_field.send_keys(username)

    password_field.clear()
    password_field.send_keys(password)
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[6]/a').click()
    time.sleep(3)
    return driver


def urlUserToUserInfo(browser):
    try:
        browser.get("https://"+url.pop())
        while True:
            try:
                result = browser.find_element_by_xpath('//div[@class="PCD_person_info"]/a[@class="WB_cardmore S_txt1 S_line1 clearfix"]').get_attribute("href")
                break
            except NoSuchElementException:
                print("延长休眠时间1秒")
                time.sleep(1)
        print(result)
    except IndexError:
        print("IndexError: url列表为空")
    return result



if __name__ == '__main__':
    threads = []
    #线程数
    threadsNum=1
    for i in range(0,threadsNum):
        t1 = threading.Thread(target=initBrowser, args=())
        threads.append(t1)

    print(time.ctime())
    for t in threads:
        t.setDaemon(True)
        t.start()
        time.sleep(1)
        # t.join()
    t.join()
    print(time.ctime())