import pandas as pd

def sort_and_group_by_quarter(data):
    """
    Sorts, groups and returns the given data by year and quarter
    """
    groupedData = pd.DataFrame(data).groupby(["year", "quarter"]).sum().to_dict(orient='index')
    restructedData = [
        {
            'quarter': q,
            'data': d
        }
        for (q, d) in groupedData.items()
    ]
    sortedData = sorted(restructedData, key=lambda x: x['quarter'])
    for quarter in sortedData:
        quarter["quarter"] = f"Q{quarter['quarter'][1]} {quarter['quarter'][0]}"
    return sortedData
