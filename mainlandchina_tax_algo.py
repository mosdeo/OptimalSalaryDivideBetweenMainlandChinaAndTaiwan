import numpy as np

tax_rate_mainlandchina = [
    # 稅率, (最低, 最高), 速算扣除數
    (0.03, (0, 36000), 0),
    (0.10, (36000, 144000), 2520),
    (0.20, (144000, 300000), 16920),
    (0.25, (300000, 420000), 31920),
    (0.30, (420000, 660000), 52920),
    (0.35, (660000, 960000), 85920),
    (0.45, (960000, np.finfo(np.float32).max), 181920),
]

def compute_tax_mainlandchina(salary, start_tax_level=5000):
    # 參考
    # 社保缴费怎么计算，医保看病能报多少？3分钟带你读懂社保 - 塞涅卡的文章 - 知乎
    # https://zhuanlan.zhihu.com/p/43131487

    retirement = salary * 0.08 # 退休金
    medical_insurance = salary * 0.02 # 醫療保險
    unemployment_insurance = salary * 0.005 # 失業保險
    maternity_insurance = 0 # 生育保險

    # 工傷保險
    # 工伤保险的参险费率叫什么？ - 愿醉的回答 - 知乎
    # https://www.zhihu.com/question/366265079/answer/976702720
    work_injury_insurance = salary * 0.002

    house_savings = salary * 0.12 # 住房公積金

    tax_free_item = [
        start_tax_level,
        retirement,
        medical_insurance,
        unemployment_insurance,
        maternity_insurance,
        work_injury_insurance,
        house_savings,
    ]

    tax_salary = salary - np.sum(tax_free_item) # 稅前薪資 - 免稅項目

    tax = 0
    for rate, (min_, max_), base in tax_rate_mainlandchina:
        if min_/12 <= tax_salary < max_/12:
            tax = (tax_salary - min_/12) * rate + base/12
            break

    return tax