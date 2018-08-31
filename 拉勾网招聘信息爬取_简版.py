import json
import random
import requests
import time
#encoding=utf-8
#获取json数据
def get_json_data(city,position,page):
    #请求拉勾的职位查询接口，返回的是json格式数据
    url = 'https://www.lagou.com/jobs/positionAjax.json?px=default&city={}&needAddtionalResult=false'.format(city)
    data = {
        'first': 'false',
        'pn': page,
        'kd': position
    }
    # header 里面加cookie就可以防止被ban
    headers = {'Host': 'www.lagou.com',
          'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0',
          'Accept': 'application/json, text/javascript, */*; q=0.01',
          'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
          'Accept-Encoding': 'gzip, deflate, br',
          'Referer': 'https://www.lagou.com/jobs/list_Java?city=%E5%85%A8%E5%9B%BD&cl=false&fromSearch=true&labelWords=&suginput=',
          'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
          'X-Requested-With': 'XMLHttpRequest',
          'X-Anit-Forge-Token': 'None',
          'X-Anit-Forge-Code': '0',
          'Content-Length': '24',
          'Cookie': 'Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1526999483,1527172516,1527509897,1527509901; _ga=GA1.2.1119628386.1522855105; user_trace_token=20180404231902-8182e3f5-381b-11e8-b413-525400f775ce; LGUID=20180404231902-8182e714-381b-11e8-b413-525400f775ce; index_location_city=%E5%8C%97%E4%BA%AC; WEBTJ-ID=20180528201816-163a6af4d221f9-08a294f453ba4f-46514133-1049088-163a6af4d23123; LGSID=20180528201913-5552632f-6271-11e8-adad-525400f775ce; PRE_UTM=; PRE_HOST=www.baidu.com; PRE_SITE=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DuHLK65HE50JshAG6GtlWwY16UdLnvezTfaaTEMtBX2PvTV1HsliPzAGQdRxuUiEE%26wd%3D%26eqid%3Ded4adeb900000fca000000065b0bf3b8; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fzhaopin%2F; LGRID=20180528203532-9c6e6941-6273-11e8-adae-525400f775ce; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1527510879; _gid=GA1.2.145013823.1527509897; JSESSIONID=ABAAABAACEBACDGE429A300E6A8DC217E51550B216A36D9; SEARCH_ID=663116997067435388edb230276acce7; TG-TRACK-CODE=search_code; _gat=1',
          'Connection': 'keep-alive',
          'Pragma': 'no-cache',
          'Cache-Control': 'no-cache'}

    response = requests.post(url, headers=headers, data=data)  # 发送给服务器的内容,不要修改伪装头,找了很久才找到可用的
    return response.text


#从json数据里面获取想要的字段
def get_positon_results(json_data):
    data = json.loads(json_data)
    #状态是成功的再处理
    if data['success'] == True:
        position_results = []
        positions = data['content']['positionResult']['result']
        for item in positions:
            companyShortName = item['companyShortName']
            companyFullName = item['companyFullName']
            companySize = item['companySize']
            positionName = item['positionName']
            workYear = item['workYear']
            salary = item['salary']
            industryField = item['industryField']
            financeStage = item['financeStage']
            createTime = item['createTime']
            education = item['education']
            district = item['district']
            positionId = item['positionId']
            jobNature = item['jobNature']
            positionAdvantage = item['positionAdvantage']
            positionUrl = 'https://www.lagou.com/jobs/' + str(positionId) + '.html'
            position_results.append([companyFullName,positionName,workYear,salary,industryField,financeStage,
                                     companyShortName,companySize,createTime,education,district,jobNature,
                                     positionAdvantage,positionId,positionUrl])
        return position_results
    else:
        print('数据出错了...')


def writetxt(file, data_list):
    with open(file, 'a+') as f:
        f.write(str(data_list))  # 写入到本地文件中


def main():
    city = input('请输入城市').strip()
    position = input('请输入职位名称').strip()
    fileName = input('请输入文件名(无需后缀)')
    filePath = './' + fileName + '.txt'
    positions = []
    for i in range(1, 31):
        time.sleep(random.random())  # 加了随机睡眠时长0-1秒之间,减小被发现几率
        print('开始爬第{}页...'.format(i))
        page_data = get_json_data(city, position, str(i))
        page_result = get_positon_results(page_data)
        # print(page_result)
        positions.append(page_result)
    writetxt(filePath, positions)

if __name__ == '__main__':
    main()
