import requests
import city

city.main()
url = "https://kyfw.12306.cn/otn/leftTicket/queryG?leftTicketDTO.train_date=2025-05-08&leftTicketDTO.from_station=VXK&leftTicketDTO.to_station=ZBK&purpose_codes=ADULT"

headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Mobile Safari/537.36 Edg/136.0.0.0",
    "Cookie": "_uab_collina=174668551883019545524786; JSESSIONID=440BF4646E438E3BC49E301E898CAC88; BIGipServerotn=1540948234.64545.0000; BIGipServerpassport=786956554.50215.0000; guidesStatus=off; highContrastMode=defaltMode; cursorStatus=off; route=495c805987d0f5c8c84b14f60212447d; _jc_save_fromStation=%u804A%u57CE%u897F%2CVXK; _jc_save_toStation=%u6DC4%u535A%2CZBK; _jc_save_fromDate=2025-05-08; _jc_save_toDate=2025-05-08; _jc_save_wfdc_flag=dc",
    "Referer": "https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc&fs=%E8%81%8A%E5%9F%8E%E8%A5%BF,VXK&ts=%E6%B7%84%E5%8D%9A,ZBK&date=2025-05-08&flag=N,N,Y",
}

# 向目标网址发送请求
res = requests.get(url, headers=headers)
# 发送解析后获得的数据是json数据，所以需要解析才可以使用

JSON = res.json()
data = JSON["data"]["result"]
for i in data:
    index = i.split("|")
    checi = index[3]
    go_time = index[8]
    arrive_time = index[9]
    time = index[10]
    vip = index[32]  # 商务座
    ydz = index[31]  # 一等座
    edz = index[30]  # 二等座

    dit = {
        "车次": checi,
        "出发时间": go_time,
        "到站时间": arrive_time,
        "用时": time,
        "商务座": vip,
        "一等座": ydz,
        "二等座": edz,
    }
    print(dit)
