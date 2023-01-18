import requests
import csv
from requests.exceptions import ConnectTimeout

def get_newset_exchange_rate():
    try:
        url = 'https://api.exchangerate-api.com/v4/latest/CNY'  # 以CNY為基準
        res = requests.get(url, timeout=1)
        if 200 == res.status_code:
            data = res.json()
            # 人民幣兌台幣匯率
            exchange_rate_CNY_to_TWD = data['rates']['TWD']
            date = data['date']
        else:
           raise Exception('get_newset_exchange_rate() failed')
    # except ConnectTimeout:
    #     exchange_rate_CNY_to_TWD = 4.51 # the rate of exchange on 2023/01/16
    except:
        exchange_rate_CNY_to_TWD = 4.51
        date = '2023/01/16'
    return date, exchange_rate_CNY_to_TWD

# 存下所有結果的表格
def output_csv(table):
        fields = [
            "總薪資(CNY)", 
            "人民幣兌台幣匯率",
            "匯率時間",

            "在台領薪資(TWD)",
            "個人繳勞保費",
            "個人繳健保費",
            "台灣税金",

            "在陸領薪資(CNY)",
            "個人繳醫保費",
            "個人繳生育保險費",
            "個人繳失業保險費",
            "個人繳工傷保險費",
            "個人繳養老金",
            "個人繳公積金",
            "大陸税金",

            "到手總和(CNY)(計入勞資雙方公積金)",
            "到手比率(%)",
            "是否為最佳分配"
            ]
        
        # 輸出結果
        f = open("{}.csv".format("兩岸不同比例領薪計算結果"), "w", newline='', encoding='utf-8')
        try:
            writer = csv.writer(f)
            # writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            writer.writerow(fields)
            for row in table:
                writer.writerow(row)
        finally:
            f.close()