import numpy as np
import matplotlib.pyplot as plt
from mainlandchina_tax_algo import MainlandChinaTax

salary = range(5000, 5000*12, 1)
tax = [MainlandChinaTax(s).tax() for s in salary]
income = np.array(salary) - tax

fig, ax = plt.subplots()
ax.set_title('[Income, Tax] vs Salary in Mainland China')
ax.set_xlabel('Salary')
ax.set_ylabel('Income')
ax.scatter(
    x=salary,
    y=income,
    alpha=0.5)
ax.scatter(
    x=salary,
    y=tax,
    alpha=0.5)

ax.grid(True)
fig.tight_layout()

plt.show()