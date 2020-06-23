#!/usr/bin/env python
# coding: utf-8

# # 思路：模拟进入>点击查看详情>判断是否需要下一位审批>模拟审批通过>返回目录>循环直至待审批人数为零跳出循环>结束

# # 提取名字函数

# In[1]:


def _extract_names(html):
    """提取名字"""
    reobj = re.compile(r'</td><td class=""><div title="[\s\S]*?" class="ivu-table-cell ivu-table-cell-ellipsis"><!----> <!----> <!----> <!----> <!----> <a title="([\s\S]*?)"><span>[\s\S]*?</span></a></div></td>', re.MULTILINE)
    names = [match.group(1) for match in reobj.finditer(html)]
    return names


# # 自动批改函数

# In[2]:


def _shenpi():
    list1 = []
    html = driver.page_source
    #判断是否需要选择下一位审批人，请假详情有需要选择下一位审批人和不需要两种情况
    reobj = re.compile(r'<div data-v-6dc7dd24="" class="form-group mb-10"><label data-v-6dc7dd24="" class="label">下一级([\s\S]*?)人：</label> <div data-v-6dc7dd24="" class="ivu-select ivu-select-single" style="width: 200px;"><div class="ivu-select-selection"><input type="hidden">  <span class="ivu-select-placeholder">请([\s\S]*?)择', re.MULTILINE)
    list1 = [match.group(1) for match in reobj.finditer(html)]
    if len(list1)>0:    
        driver.find_element_by_xpath("//span[contains(text(),'请选择')]").click()
        driver.find_element_by_xpath("//li[6]").click()
        time.sleep(1)
        driver.find_element_by_xpath("//button[@type='button']").click()
        time.sleep(1)
        driver.find_element_by_xpath("//button[@class='ivu-btn ivu-btn-primary ivu-btn-large']").click()
    else:
        time.sleep(1)
        driver.find_element_by_xpath("//button[@type='button']").click()
        time.sleep(1)
        driver.find_element_by_xpath("//button[@class='ivu-btn ivu-btn-primary ivu-btn-large']").click()


# In[3]:


def pg_qingjia():
    while True:
        html = driver.page_source
        names = _extract_names(html)
        if len(names) == 0:
            print('请假批改完毕')
            break 
        time.sleep(2)
        #模拟点击查看详情
        driver.find_element_by_xpath("/html/body/div[4]/div[2]/div[2]/div/div[2]/div[1]/div/div[3]/div/div/div[5]/div[2]/table/tbody/tr[1]/td[1]/div").click()
        time.sleep(1)
        _shenpi()
        time.sleep(1)
        driver.back()
# driver.back()在此处功能相当于driver.get("https://zjiet.cpdaily.com/wec-counselor-leave-apps/leaveadmin/pcAdmin/index.html#/list")
        time.sleep(1)


# # 进入网址

# In[4]:


from selenium import webdriver
import re,time
driver = webdriver.Chrome()
driver.get("https://zjiet.cpdaily.com/portal/index.html")


# # 登录

# In[5]:


time.sleep(1)
driver.find_element_by_xpath("//div[@id='ampHasNoLogin']/span").click()
time.sleep(1)
driver.find_element_by_xpath("//input[@type='text']").send_keys("2018000013")
driver.find_element_by_xpath("//input[@type='password']").click()
driver.find_element_by_xpath("//input[@type='password']").clear()
driver.find_element_by_xpath("//input[@type='password']").send_keys("qw123456")
time.sleep(1)
driver.find_element_by_xpath("//div[@id='app']/div/div/div/div/div[2]/div/div[2]/div/div/div[4]/div/span").click()
time.sleep(1)


# # 请假页面

# In[6]:


driver.get("https://zjiet.cpdaily.com/wec-counselor-leave-apps/leaveadmin/pcAdmin/index.html#/list")
time.sleep(1)


# In[7]:


#已审批页面（用于测试名称的提取）
#driver.find_element_by_xpath("//div[2]/div[2]/div/div/div/div/div/div/div[3]").click()


# # 任务一最后一步：知道当前班主任，有多少个请假

# In[8]:


html = driver.page_source
li = _extract_names(html)
print(li)
print("人数：",len(li))


# # 任务二：给定学生名字，自动完成批准请假工作

# In[9]:


pg_qingjia()


# # 任务三

# In[10]:


#暂时搁置

