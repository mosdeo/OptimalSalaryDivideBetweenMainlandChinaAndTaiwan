import requests
from requests.exceptions import ConnectTimeout

def get_newset_exchange_rate():
    try:
        url = 'https://api.exchangerate-api.com/v4/latest/CNY'  # 以CNY為基準
        res = requests.get(url, timeout=1)
        if 200 == res.status_code:
            data = res.json()
            # 人民幣兌台幣匯率
            exchange_rate_CNY_to_TWD = data['rates']['TWD']
        else:
            exchange_rate_CNY_to_TWD = 4.51
    except ConnectTimeout:
        exchange_rate_CNY_to_TWD = 4.51 # the rate of exchange on 2023/01/16
    except:
        exchange_rate_CNY_to_TWD = 4.51 # the rate of exchange on 2023/01/16
    return exchange_rate_CNY_to_TWD