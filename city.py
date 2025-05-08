import requests
import sqlite3
import os
import sys
import datetime as dt


def printFormat(text, end="\n"):
    print(f"\033[K[{dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {text}", end=end)


def main():
    printFormat("Start ready to create database...")
    DataBase_PATH = "./CityList.db"
    try:
        if os.path.exists(DataBase_PATH):
            os.remove(DataBase_PATH)
    except:
        print("Read Database Failed.")
        sys.exit(1)
    Database = sqlite3.connect(DataBase_PATH)
    db = Database.cursor()
    db.execute(
        """
    CREATE TABLE CityList(
                id                  int     NOT NULL    PRIMARY KEY,
                TrainName           TEXT    NOT NULL,
                TrainCode           TEXT    NOT NULL,
                CityPinyin          TEXT    NOT NULL,
                CityPinyinSimple    TEXT    NOT NULL,
                CityName            TEXT    NOT NULL
                );
    """
    )
    Database.commit()
    printFormat("Create database success.")
    printFormat("Start ready to get city list...")
    GetCity = requests.get(
        "https://www.12306.cn/index/script/core/common/station_name_new_v10079.js"
    )

    Citys = GetCity.text[int(GetCity.text.index("'") + 1) : -2]

    Citys = Citys.split("|||")
    printFormat("Get city list success.")
    printFormat("Start ready to insert data into database...")
    for i in range(len(Citys) - 1):
        data = Citys[i].split("|")
        CityData = {
            "id": data[5],
            "TrainName": data[1],
            "TrainCode": data[2],
            "CityPinyin": data[3],
            "CityPinyinSimple": data[4],
            "CityName": data[7],
        }
        db.execute(
            f"INSERT INTO CityList(id, TrainName, TrainCode, CityPinyin, CityPinyinSimple, CityName) VALUES ({CityData['id']}, '{CityData['TrainName']}', '{CityData['TrainCode']}', '{CityData['CityPinyin']}', '{CityData['CityPinyinSimple']}', '{CityData['CityName']}')",
        )
        Database.commit()
        printFormat(
            f"[{i+1}/{len(Citys)-1}] Insert data {CityData['TrainName']} into database success. ",
            end="\r",
        )
    printFormat("Insert data into database success.")

    Database.close()
    printFormat("Close database success.")
    printFormat("All done.")


if __name__ == "__main__":
    main()
