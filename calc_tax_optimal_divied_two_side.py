import numpy as np
import requests
from requests.exceptions import ConnectTimeout
from algorithm_tax.MainlandChina import MainlandChinaTax
from algorithm_tax.Taiwan import TaiwanTax

def __main__():
    # 請輸入期望薪資
    salary = int(input('請輸入期望薪資: '))
    salary = np.array([salary])

# 期望總薪資CNY
# salary = np.array([s for s in range(30000, 60000, 100)])
# salary = salary[-1]

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

table = np.zeros(shape=(salary, 5))

for s in range(salary):
    # 期望薪資TWD部分、扣項、到手部分
    salary_TWD = s * exchange_rate_CNY_to_TWD
    deductions_TWD = salary_TWD - TaiwanTax(salary_TWD).net_salary()
    net_salary_TWD = salary_TWD - deductions_TWD

    # 期望薪資CNY部分、扣項、到手部分
    salary_CNY = salary - s
    deductions_CNY = salary_CNY - MainlandChinaTax(salary_CNY).salary_after_tax()
    salary_after_tax_CNY = salary_CNY - deductions_CNY # + MainlandChinaTax(salary_CNY).house_savings() * 2

    # 期望總薪資的到手薪資(CNY計)
    net_salary = net_salary_TWD/exchange_rate_CNY_to_TWD + salary_after_tax_CNY

    table[s, 0] = deductions_TWD
    table[s, 1] = deductions_CNY
    table[s, 2] = salary_TWD
    table[s, 3] = salary_CNY
    table[s, 4] = net_salary

# 找出最佳分配
optimal_divide_index = np.argmax(table[:, 4])

print('Optimal divided:\n\
        deductions_TWD {} CNY,\n\
        deductions_CNY {} CNY,\n\
        salary_TWD {} CNY,\n\
        salary_CNY {} CNY,\n\
        salary TWD:CNY {}:1,\n\
        net_salary {} CNY,\n\
        到手率 {}'.format(
    table[optimal_divide_index, 0]/exchange_rate_CNY_to_TWD, 
    table[optimal_divide_index, 1], 
    table[optimal_divide_index, 2]/exchange_rate_CNY_to_TWD, 
    table[optimal_divide_index, 3],
    (table[optimal_divide_index, 2]/exchange_rate_CNY_to_TWD)/table[optimal_divide_index, 3],
    table[optimal_divide_index, 4],
    table[optimal_divide_index, 4]/salary),
    )