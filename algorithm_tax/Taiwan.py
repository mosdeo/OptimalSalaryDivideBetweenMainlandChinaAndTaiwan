import numpy as np

# 參考
# https://www.518.com.tw/article/1945
# https://www.bli.gov.tw/0014162.html
# https://data.gov.tw/dataset/20251

# 台灣健保費用級距表
health_insurance_mapping_table = [
[(0, 26400), 26400],
[(26401, 27600), 27600],
[(27601, 28800), 28800],
[(28801, 30300), 30300],
[(30301, 31800), 31800],
[(31801, 33300), 33300],
[(33301, 34800), 34800],
[(34801, 36300), 36300],
[(36301, 38200), 38200],
[(38201, 40100), 40100],
[(40101, 42000), 42000],
[(42001, 43900), 43900],
[(43901, 45800), 45800],
[(45801, 48200), 48200],
[(48201, 50600), 50600],
[(50601, 53000), 53000],
[(53001, 55400), 55400],
[(55401, 57800), 57800],
[(57801, 60800), 60800],
[(60801, 63800), 63800],
[(63801, 66800), 66800],
[(66801, 69800), 69800],
[(69801, 72800), 72800],
[(72801, 76500), 76500],
[(76501, 80200), 80200],
[(80201, 83900), 83900],
[(83901, 87600), 87600],
[(87601, 92100), 92100],
[(92101, 96600), 96600],
[(96601, 101100), 101100],
[(101101, 105600), 105600],
[(105601, 110100), 110100],
[(110101, 115500), 115500],
[(115501, 120900), 120900],
[(120901, 126300), 126300],
[(126301, 131700), 131700],
[(131701, 137100), 137100],
[(137101, 142500), 142500],
[(142501, 147900), 147900],
[(147901, 150000), 150000],
[(150001, 156400), 156400],
[(156401, 162800), 162800],
[(162801, 169200), 169200],
[(169201, 175600), 175600],
[(175601, 182000), 182000],
[(182001, 189500), 189500],
[(189501, 197000), 197000],
[(197001, 204500), 204500],
[(204501, 212000), 212000],
[(212001, np.inf), 219500],
]

# 台灣勞工保險費用級距表
labor_insurance_mapping_table = [
    [(0, 26400), 26400],
    [(26401, 27600), 27600],
    [(27601, 28800), 28800],
    [(28801, 30300), 30300],
    [(30301, 31800), 31800],
    [(31801, 33300), 33300],
    [(33301, 34800), 34800],
    [(34801, 36300), 36300],
    [(36301, 38200), 38200],
    [(38201, 40100), 40100],
    [(40101, 42000), 42000],
    [(42001, 43900), 43900],
    [(43901, np.inf), 45800],
]

# 台灣所得稅級距表
tax_mapping_table = [
    # 綜合所得淨額(最低, 最高), 稅率, 累進差額 
    [(      0, 560000), 0.05, 0],
    [(560001, 1260000), 0.12, 39200],
    [(1260001, 2520000), 0.2, 140000],
    [(2520001, 4720000), 0.3, 392000],
    [(4720001, np.inf), 0.4, 864000],
]

class TaiwanTax:
    basic_salary = 26400 # 基本工資
    def __init__(self, salary):
        self.salary = salary

    def __salary_level_mapping(self, mapping_table):
        for (min_, max_), level in mapping_table:
            if min_ <= np.ceil(self.salary) <= max_:
                return level
        raise ValueError('Salary is out of range')

    def health_insurance_fee(self):
        salary_level = self.__salary_level_mapping(health_insurance_mapping_table)
        return salary_level * 0.0517 * 0.3 # 健康保險費(個人負擔30%)

    def labor_insurance_fee(self):
        salary_level = self.__salary_level_mapping(labor_insurance_mapping_table)
        return salary_level * 0.12 * 0.2 # 勞工保險費(個人負擔20%)

    def tax(self):
        tax_salary = np.ceil(self.salary - self.health_insurance_fee() - self.labor_insurance_fee())
        # https://www.ntbt.gov.tw/multiplehtml/1b82b380e1a34de9afd204d39b007db2
        for (min_, max_), rate, base in tax_mapping_table:
            (min_, max_), base = (min_/12, max_/12), base/12 # 每月
            if min_ <= tax_salary <= max_:
                tax = tax_salary * rate - base
                return tax
        raise ValueError('Salary is out of range')

    def net_salary(self):
        return self.salary - self.health_insurance_fee() - self.labor_insurance_fee() - self.tax()