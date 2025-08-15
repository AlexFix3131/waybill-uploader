#!/usr/bin/env python3
# process_invoice.py
# Usage: python process_invoice.py input.pdf output.xlsx
# Extracts rows to columns: MPN, Replacem, Quantity, Totalsprice, Order reference
# Rules: per AVAR (Totalsprice from Summa; ignore Cena; copy #order per block)
import sys, re, os
import pandas as pd

# This script expects a CSV extracted from the PDF beforehand.
# For a quick demo, if input is CSV, we read it; if PDF, exit with message.
inp = sys.argv[1]
outp = sys.argv[2]

if inp.lower().endswith('.csv'):
    df = pd.read_csv(inp, sep=None, engine='python')
else:
    print('ERROR: This template expects a CSV extracted from PDF. Use OCR/CSV step in your pipeline.', file=sys.stderr)
    sys.exit(2)

def norm(s): return re.sub(r'\s+',' ',str(s).strip().lower())

inv = {norm(c):c for c in df.columns}
def pick(*alts):
    for a in alts:
        a = norm(a)
        if a in inv: return inv[a]
        for k,v in inv.items():
            if a in k or k in a: return v
    return None

col_mpn = pick('mpn','artikuls','item code','code')
col_qty = pick('quantity','daudz.','qty','daudz')
col_sum = pick('summa','totalsprice','line total','amount')
col_order = pick('order reference','order nr','order')

out = pd.DataFrame()
out['MPN'] = df[col_mpn].astype(str) if col_mpn else ''
out['Replacem'] = ''
out['Quantity'] = df[col_qty] if col_qty else ''
out['Totalsprice'] = df[col_sum] if col_sum else ''

if col_order:
    out['Order reference'] = df[col_order].astype(str).str.extract(r'(\d+)', expand=False).fillna('')
else:
    # fallback from markers in any column
    current = ''
    orders = []
    pat = re.compile(r'#\s*(\d+)\b')
    for _, row in df.iterrows():
        text = ' '.join(str(v) for v in row.values)
        m = pat.search(text)
        if m: current = m.group(1)
        orders.append(current)
    out['Order reference'] = orders

out.to_excel(outp, index=False)
print(outp)
