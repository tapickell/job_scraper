"""
Module Doc String
"""

import os
import re

# import pipe
import pandas as pd

dtypes = {
    "title": "category",
    "technology": "object",
    "posting_id": "category",
    "apply_method": "category",
    "company": "category",
}


def fp_rev_sort(l):
    "sort without mutating state"
    lc = l.copy()
    lc.sort(reverse=True)
    return lc


files = [f for f in os.listdir(".") if os.path.isfile(f) and re.match(r"^results", f)]
fs = fp_rev_sort(files)
df = pd.read_csv(fs[0], dtype=dtypes, usecols=list(dtypes))

deduped = df[df.duplicated()]
filtered = deduped.query("technology != '[]'")

# sort the money field to be largest values first,
# sort by the money field so no vales last and lasrgest first value is first
# sorted = filtered.

# weighting ??
# add weights to functional, senior, technology I like
