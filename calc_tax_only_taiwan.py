import matplotlib.markers as markers
import numpy as np
import matplotlib.pyplot as plt
from  algorithm_tax.Taiwan import *

salary = range(10000, 10000*12, 1000)
tax = [TaiwanTax(s).tax() for s in salary]
health_insurance = [TaiwanTax(s).health_insurance_fee() for s in salary]
labor_insurance = [TaiwanTax(s).labor_insurance_fee() for s in salary]
income = np.array(salary) - tax - health_insurance - labor_insurance

fig, ax = plt.subplots()
ax.set_title('[Tax, Income, Health Insurance, Labor Insurance] vs Salary in Taiwan')
ax.set_xlabel('Salary')
ax.set_ylabel('Tax, Income, Health Insurance, Labor Insurance')

marker = markers.MarkerStyle(marker='*', fillstyle='none')
ax.scatter(x=salary, y=tax, marker=marker, color='r', alpha=0.5)
ax.scatter(x=salary, y=income, marker=marker, color='y', alpha=0.5)
ax.scatter(x=salary, y=health_insurance, marker=marker, color='g', alpha=0.5)
ax.scatter(x=salary, y=labor_insurance, marker=marker, color='b', alpha=0.5)

ax.grid(True)
fig.tight_layout()
fig.autofmt_xdate()

plt.show()