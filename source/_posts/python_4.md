---
title: Python Note 4
tags: Python, Note
---
# Python Note 4

### Pypi & Pip
+ [pypi](https://pypi.org/)
+ use as : pip install openpyxl  to install 

### Use openpyxl
```
import openpyxl as xl
from openpyxl.chart import BarChart, Reference
wb = xl.load_workbook("pydemo2/transactions.xlsx")
sheet = wb["Sheet1"]
for row in range(2, sheet.max_row + 1):
    cell = sheet.cell(row, 3)
    real_val = cell.value * 0.9
    real_val_cell = sheet.cell(row, 4)
    real_val_cell.value = real_val

values = Reference(sheet, min_row=2, max_row=sheet.max_row, min_col=4, max_col=4)
chart = BarChart()
chart.add_data(values)
sheet.add_chart(chart, 'e2')
wb.save('pydemo2/transactions_n2.xlsx')
```
