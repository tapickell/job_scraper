"""
Module Doc String
"""

import os
import pprint
import re

# import pipe
import pandas as pd

dtypes = {
    "title": "category",
    "technology": "object",
    "money": "object",
    "salary": "object",
    "benefits": "object",
    "industries": "object",
    "posting_id": "category",
    "apply_method": "category",
    "company": "category",
}


def fp_rev_sort(l):
    "sort without mutating state"
    lc = l.copy()
    lc.sort(reverse=True)
    return lc


def prepare_latest():
    "gets the latest csv file and dedups and filters out missing tech"
    files = [f for f in os.listdir(".") if os.path.isfile(f) and re.match(r"^results", f)]
    fs = fp_rev_sort(files)
    df = pd.read_csv(fs[0], dtype=dtypes, usecols=list(dtypes))

    filtered = df.query("technology != '[]'")
    return filtered

pprint.pp(prepare_latest())

# weighting ??
# add weights to functional, senior, technology I like
