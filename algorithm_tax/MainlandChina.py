import numpy as np

tax_rate_mainlandchina = [
    # https://www.toutiao.com/article/7185763443599819320/
    # 稅率, (最低, 最高), 速算扣除數
    (0.03, (0, 36000), 0),
    (0.10, (36000, 144000), 2520),
    (0.20, (144000, 300000), 16920),
    (0.25, (300000, 420000), 31920),
    (0.30, (420000, 660000), 52920),
    (0.35, (660000, 960000), 85920),
    (0.45, (960000, np.finfo(np.float32).max), 181920),
]

class MainlandChinaTax:
    normal_lowest_salary = 3500 # 常規最低薪資
    def __init__(self, salary, house_savings_rate=0.05, is_retirement=True, is_unemployment_insurance=True):
        self.salary = salary
        self.house_savings_rate = house_savings_rate
        self.is_retirement = is_retirement
        self.is_unemployment_insurance = is_unemployment_insurance

    # 工傷保險費
    def work_injury_insurance(self):
        # 工伤保险的参险费率叫什么？ - 愿醉的回答 - 知乎
        # https://www.zhihu.com/question/366265079/answer/976702720
        return self.salary * 0.002

    # 生育保險費
    def maternity_insurance(self):
        return self.salary * 0

    # 醫療保險費
    def medical_insurance(self):
        return self.salary * 0.02

    # 養老金
    def retirement(self):
        return self.salary * 0.08 if self.is_retirement else 0

    # 失業保險費
    def unemployment_insurance(self):
        return self.salary * 0.005 if self.is_unemployment_insurance else 0

    def five_insurances(self):
        return np.sum([
            self.retirement(), 
            self.unemployment_insurance(), 
            self.medical_insurance(),
            self.maternity_insurance(), 
            self.work_injury_insurance()])

    def house_savings(self):
        return self.salary * self.house_savings_rate

    def tax(self):
        # 參考
        # 社保缴费怎么计算，医保看病能报多少？3分钟带你读懂社保 - 塞涅卡的文章 - 知乎
        # https://zhuanlan.zhihu.com/p/43131487

        start_tax_level = 5000 # 起徵點

        tax_free_item = [
            start_tax_level,
            self.five_insurances(),
            self.house_savings(),
        ]

        tax_salary = self.salary - np.sum(tax_free_item) # 稅前薪資 - 免稅項目

        tax = 0
        for rate, (min_, max_), base in tax_rate_mainlandchina:
            (min_, max_), base = (min_/12, max_/12), base/12 # 每月
            if min_ < tax_salary <= max_:
                tax = tax_salary * rate - base
                break
        return tax

    def salary_after_tax(self):
        return self.salary - self.tax() - self.five_insurances() - self.house_savings()