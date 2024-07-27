"""
Module Doc String
"""
import os
import re
import pipe
import pandas as pd

dtypes = {
    "title": "category",
    "technology": "object",
    "posting_id": "category",
    "apply_method": "category",
    "company": "category"
}

def fpsort(l):
    "sort without mutating state"
    lc = l.copy()
    lc.sort()
    return lc

def fpreverse(l):
    "reverse without mutating state"
    lc = l.copy()
    lc.reverse() # this is marginaly better
    return lc

# filepath = "results_2024-07-26_00/09/36.660941.csv"
files = [f for f in os.listdir('.') if os.path.isfile(f) and re.match(r"^results", f)]
# files.sort()
# files.reverse() # mutating data feels so dirty :sad_panda:
# preped_files = files | fpsort() | fpreverse() # need to figure out how pipes work in Python
fs = fpreverse(fpsort(files))
df = pd.read_csv(fs[0], dtype=dtypes, usecols=list(dtypes))

filtered = df.query("technology != '[]'")
deduped = filtered[filtered.duplicated()]
