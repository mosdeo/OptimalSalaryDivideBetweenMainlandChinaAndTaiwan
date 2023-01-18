import numpy as np
import matplotlib.pyplot as plt
import matplotlib.markers as markers
from algorithm_tax.MainlandChina import MainlandChinaTax
from algorithm_tax.Taiwan import TaiwanTax
from algorithm_tax.utility import get_newset_exchange_rate, output_csv

if __name__ == '__main__':
    # 請輸入期望薪資
    salary = int(input('請輸入期望月薪資(CNY): '))

    # 取得最新匯率
    date, exchange_rate_CNY_to_TWD = get_newset_exchange_rate()
    print('{} 人民幣兌台幣匯率: {}'.format(date, exchange_rate_CNY_to_TWD))

    # 建立表格
    table = np.zeros(shape=(salary, 18), dtype=object)
    for s in range(salary):
        # 期望薪資TWD部分、扣項、到手部分
        salary_TWD = s * exchange_rate_CNY_to_TWD
        # 不足台灣法定最低工資，則不計算
        if salary_TWD < TaiwanTax.basic_salary:
            continue
        taiwanTax = TaiwanTax(salary_TWD)

        # 期望薪資CNY部分、扣項、到手部分
        salary_CNY = salary - s
        # 不足中國常規最低工資，則不計算
        if salary_CNY < MainlandChinaTax.normal_lowest_salary:
            continue
        # 這裡將公積金算入到手薪資中，但依然是扣項
        # 公積金=12%, 不繳失業保險、不繳退休金
        mainlandChinaTax = MainlandChinaTax(salary_CNY, house_savings_rate=0.12, is_retirement=False, is_unemployment_insurance=False)
        real_income_CNY = mainlandChinaTax.salary_after_tax() + mainlandChinaTax.house_savings() * 2

        # 期望總薪資的到手薪資(CNY計)
        net_salary = taiwanTax.net_salary()/exchange_rate_CNY_to_TWD + real_income_CNY

        # 填入表格
        table[s, 0] = salary # "總薪資(CNY)", 
        table[s, 1] = exchange_rate_CNY_to_TWD # "人民幣兌台幣匯率",
        table[s, 2] = date # "匯率時間",

        table[s, 3] = salary_TWD # "在台領薪資(TWD)",
        table[s, 4] = taiwanTax.labor_insurance_fee() # "個人繳勞保費",
        table[s, 5] = taiwanTax.health_insurance_fee()  # "個人繳健保費",
        table[s, 6] = taiwanTax.tax() # "台灣税金",

        table[s, 7] = salary_CNY # "在陸領薪資(CNY)",
        table[s, 8] = mainlandChinaTax.medical_insurance() # "個人繳醫保費",
        table[s, 9] = mainlandChinaTax.maternity_insurance() # "個人繳生育保險費",
        table[s,10] = mainlandChinaTax.unemployment_insurance() # "個人繳失業保險費",
        table[s,11] = mainlandChinaTax.work_injury_insurance() # "個人繳工傷保險費",
        table[s,12] = mainlandChinaTax.retirement() # "個人繳養老金",
        table[s,13] = mainlandChinaTax.house_savings() # "個人繳公積金",
        table[s,14] = mainlandChinaTax.tax() # "大陸税金",

        table[s,15] = net_salary # "到手總和(CNY)(計入勞資雙方公積金)",
        table[s,16] = net_salary/salary # "到手比率(%)",

    # 找出到手最大分配，並標記
    optimal_divide_index = np.argmax(table[:, 15])
    table[:, 17] = '否'
    table[optimal_divide_index, 17] = '最佳分配'

    # 存下所有結果的表格
    # 為了避免太冗長，只存下最佳分配前後N筆的結果
    N = 10
    output_csv(table[optimal_divide_index-N:optimal_divide_index+N+1, :])

    # 印出最佳分配
    print('最佳分配: ')
    print('- 在台領薪資(TWD): {}'.format(table[optimal_divide_index, 3]))
    print('- 在陸領薪資(CNY): {}'.format(table[optimal_divide_index, 7]))
    print('- 申報薪資比率(台:陸): {}'.format((float(table[optimal_divide_index, 3])/exchange_rate_CNY_to_TWD)/table[optimal_divide_index, 7]))
    print('- 到手總和(CNY)(計入勞資雙方公積金): {}'.format(table[optimal_divide_index, 15]))
    print('- 到手比率(%): {}'.format(table[optimal_divide_index, 16]))

    # 印出1:1分配
    middle_index = salary//2
    print('1:1分配: ')
    print('- 在台領薪資(TWD): {}'.format(table[middle_index, 3]))
    print('- 在陸領薪資(CNY): {}'.format(table[middle_index, 7]))
    print('- 申報薪資比率(台:陸): {}'.format((float(table[middle_index, 3])/exchange_rate_CNY_to_TWD)/table[middle_index, 7]))
    print('- 到手總和(CNY)(計入勞資雙方公積金): {}'.format(table[middle_index, 15]))
    print('- 到手比率(%): {}'.format(table[middle_index, 16]))

    # 繪圖
    ## 去除多餘的空行
    table = table[~np.all(table == 0, axis=1)]
    fig, ax = plt.subplots()
    ax.grid(True)
    ax.set_title('Optimal Salary Distribution Between Taiwan and Mainland China')
    ax.set_xlabel('Salary Distribution Rate (Taiwan:Both)')
    ax.set_ylabel('Salary in Taiwan, Mainland China, Income Sum of Both (CNY)')

    marker = markers.MarkerStyle(marker='.', fillstyle='none')
    scatter_marker_size = 1
    x_salary_rate = np.array(list(range(salary)))/salary
    line_salary_tw = ax.scatter(
                        label='Salary in Taiwan',
                        x=x_salary_rate, y=table[:,3]/exchange_rate_CNY_to_TWD, 
                        marker=marker, color='g', alpha=0.5, s=scatter_marker_size)
    line_salary_ch = ax.scatter(
                        label='Salary in Mainland China',
                        x=x_salary_rate, y=table[:,7], 
                        marker=marker, color='r', alpha=0.5, s=scatter_marker_size)
    line_income_both = ax.scatter(
                        label='Income Both',
                        x=x_salary_rate, y=table[:,15],
                        marker=marker, color='y', alpha=0.5, s=scatter_marker_size)
    line_optimal_divide = plt.axvline(
                        label='Optimal Divide Point',
                        x=x_salary_rate[optimal_divide_index], color='purple', alpha=0.5)
    plt.legend(
        handles=[
            line_salary_tw, 
            line_salary_ch, 
            line_income_both,
            line_optimal_divide,
            ],
        loc='center right')

    fig.tight_layout()
    fig.autofmt_xdate()
    ax.text(0.3, 0.8, 'Income included all of House Savings 12% twice.', style='italic',
        bbox={'facecolor': 'red', 'alpha': 0.3, 'pad': 10})

    plt.show()