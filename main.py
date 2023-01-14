import numpy as np
import matplotlib.pyplot as plt
from algo import compute_tax_mainlandchina

salary = range(5000, 5000*12, 1)
tax = np.vectorize(compute_tax_mainlandchina)(salary)
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

