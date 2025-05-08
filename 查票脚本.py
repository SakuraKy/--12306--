import requests
import city
import sys
import sqlite3
import datetime
import urllib.parse

for i in sys.argv:
    if i == "--sync" or i == "-s":
        city.main()

# 连接数据库
conn = sqlite3.connect("./CityList.db")
cursor = conn.cursor()


# 示例1: 根据城市名查询车站代码
def get_station_code(city_name):
    cursor.execute(f"SELECT TrainCode FROM CityList WHERE CityName='{city_name}'")
    result = cursor.fetchone()
    return result[0] if result else None


# 添加高级查询功能
def search_city(keyword):
    """根据关键词模糊搜索城市"""
    cursor.execute(
        f"SELECT TrainName, TrainCode FROM CityList WHERE CityName LIKE '%{keyword}%' OR CityPinyin LIKE '%{keyword}%'"
    )
    return cursor.fetchall()


def query_tickets(from_code, to_code, from_trainname, to_trainname, date):
    """查询指定日期从出发地到目的地的车票信息"""
    url = f"https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={date}&leftTicketDTO.from_station={from_code}&leftTicketDTO.to_station={to_code}&purpose_codes=ADULT"

    cookie = {
        "_jc_save_fromStation": urllib.parse.quote(
            str(from_trainname + "," + from_code)
        ),
        "_jc_save_toStation": urllib.parse.quote(str(to_trainname + "," + to_code)),
        "_jc_save_fromDate": date,
        "_jc_save_toDate": date,
        "_jc_save_wfdc_flag": "dc",
    }
    try:
        res = requests.get(url, cookies=cookie)
        res.raise_for_status()

        json_data = res.json()
        data = json_data["data"]["result"]

        result_list = []
        for i in data:
            index = i.split("|")
            ticket_info = {
                "车次": index[3],
                "出发时间": index[8],
                "到站时间": index[9],
                "用时": index[10],
                "商务座": index[32] or "无",
                "一等座": index[31] or "无",
                "二等座": index[30] or "无",
            }
            result_list.append(ticket_info)

        return result_list
    except Exception as e:
        print(f"查询失败: {e}")
        return []


def interactive_query():
    """交互式查询车票"""
    # 查询出发地
    from_keyword = input("请输入出发地(城市名或拼音): ")
    from_results = search_city(from_keyword)

    if not from_results:
        print(f"未找到与'{from_keyword}'相关的城市")
        return

    print("\n找到以下出发地:")
    for idx, (city, code) in enumerate(from_results):
        print(f"{idx+1}. {city} ({code})")

    try:
        from_idx = int(input("\n请选择出发地编号: ")) - 1
        from_city, from_code = from_results[from_idx]
    except (ValueError, IndexError):
        print("无效的选择!")
        return

    # 查询目的地
    to_keyword = input("\n请输入目的地(城市名或拼音): ")
    to_results = search_city(to_keyword)

    if not to_results:
        print(f"未找到与'{to_keyword}'相关的城市")
        return

    print("\n找到以下目的地:")
    for idx, (city, code) in enumerate(to_results):
        print(f"{idx+1}. {city} ({code})")

    try:
        to_idx = int(input("\n请选择目的地编号: ")) - 1
        to_city, to_code = to_results[to_idx]
    except (ValueError, IndexError):
        print("无效的选择!")
        return

    # 查询日期
    today = datetime.date.today()
    default_date = today.strftime("%Y-%m-%d")
    date_input = input(f"\n请输入查询日期(格式:YYYY-MM-DD, 默认今天{default_date}): ")
    query_date = date_input if date_input else default_date

    print(f"\n正在查询从 {from_city} 到 {to_city} 的 {query_date} 火车票信息...\n")

    # 执行查询
    ticket_list = query_tickets(from_code, to_code, from_city, to_city, query_date)

    if not ticket_list:
        print("未查询到符合条件的车次!")
        return

    print(f"共找到 {len(ticket_list)} 个车次:\n")
    for ticket in ticket_list:
        print(
            f"车次: {ticket['车次']}, 出发: {ticket['出发时间']}, 到达: {ticket['到站时间']}, 耗时: {ticket['用时']}"
        )
        print(
            f"座位: 商务座 {ticket['商务座']}, 一等座 {ticket['一等座']}, 二等座 {ticket['二等座']}\n"
        )


# 使用交互式查询
if __name__ == "__main__":
    interactive_query()
