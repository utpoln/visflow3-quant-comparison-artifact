# Verbatim copy of the registered VisFlow library "filter_and_sort"
# (same provenance note as lib_go_term_lookup.py). In this workflow no
# filters/sort_by are configured on the Adapter node, so this step is
# exercised as a no-op pass-through — exactly what VisFlow itself does for
# this workflow (confirmed against its own Results panel output).
import pandas as pd, operator

OPS = {"lt": operator.lt, "gt": operator.gt, "lte": operator.le, "gte": operator.ge, "eq": operator.eq}

def run(input):
    df = pd.DataFrame(input.get("data",[]))
    filters  = input.get("filters",{})
    sort_col = input.get("sort_by")
    asc      = input.get("ascending", True)
    for col, conditions in filters.items():
        if col not in df.columns: continue
        for op_name, val in conditions.items():
            op = OPS.get(op_name)
            if op: df = df[op(df[col], val)]
    if sort_col and sort_col in df.columns:
        df = df.sort_values(sort_col, ascending=asc)
    return df.to_dict(orient="records")
