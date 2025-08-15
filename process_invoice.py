import sys, re
import pandas as pd
import pdfplumber

if len(sys.argv) != 3:
    print("Usage: process_invoice.py input.pdf output.xlsx", file=sys.stderr)
    sys.exit(1)

input_pdf = sys.argv[1]
output_xlsx = sys.argv[2]

# Extract tables from PDF (AVAR format)
rows = []
with pdfplumber.open(input_pdf) as pdf:
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            for row in table:
                if any(row):
                    rows.append(row)

df_raw = pd.DataFrame(rows)

# Try to detect columns by header names
header_row_index = None
for i, row in df_raw.iterrows():
    if any(isinstance(x, str) and 'Summa' in x for x in row):
        header_row_index = i
        break

if header_row_index is None:
    header_row_index = 0

df = pd.DataFrame(rows[header_row_index+1:], columns=rows[header_row_index])

# Normalize column picking
def pick_col(df, *names):
    for name in names:
        for col in df.columns:
            if col and name.lower() in str(col).lower():
                return col
    return None

col_mpn = pick_col(df, 'Artikuls', 'MPN', 'Code')
col_qty = pick_col(df, 'Daudz', 'Quantity', 'Qty')
col_sum = pick_col(df, 'Summa', 'Totalsprice', 'Amount')
col_order = pick_col(df, 'Order', 'Order reference')

out = pd.DataFrame()
out['MPN'] = df[col_mpn].astype(str) if col_mpn else ''
out['Replacem'] = ''
out['Quantity'] = df[col_qty] if col_qty else ''
out['Totalsprice'] = df[col_sum] if col_sum else ''

if col_order:
    out['Order reference'] = df[col_order].astype(str).str.extract(r'(\d+)', expand=False).fillna('')
else:
    current = ''
    orders = []
    pat = re.compile(r'#\s*(\d+)\b')
    for _, row in df.iterrows():
        text = ' '.join(str(v) for v in row.values)
        m = pat.search(text)
        if m:
            current = m.group(1)
        orders.append(current)
    out['Order reference'] = orders

out.to_excel(output_xlsx, index=False)
