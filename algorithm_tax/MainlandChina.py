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
    def __init__(self, salary):
        self.salary = salary

    def five_insurances(self):
        retirement = self.salary * 0.08 # 退休金
        medical_insurance = self.salary * 0.02 # 醫療保險
        unemployment_insurance = self.salary * 0.005 # 失業保險
        maternity_insurance = 0 # 生育保險

        # 工傷保險
        # 工伤保险的参险费率叫什么？ - 愿醉的回答 - 知乎
        # https://www.zhihu.com/question/366265079/answer/976702720
        work_injury_insurance = self.salary * 0.002
        return np.sum([
            retirement, 
            medical_insurance, 
            unemployment_insurance, 
            maternity_insurance, 
            work_injury_insurance])

    def house_savings(self, rate=0.12):
        return self.salary * rate

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