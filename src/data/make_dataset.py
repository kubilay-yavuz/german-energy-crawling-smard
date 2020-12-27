from src.constants import *
import pandas as pd
import numpy as np
import io
import requests


def fix_col_name(col):
    for key in column_fixer.keys():
        col = col.replace(key, column_fixer[key])
    return col.lower()


# key moduleIds_categories_subcats keyi
def request_data(param_body, key, url):
    param_body["request_form"][0]["moduleIds"] = moduleIds_categories_subcats[key]
    df_all = pd.DataFrame()
    print(key)
    for area_ in bidding_zones_control_areas.keys():
        param_body["request_form"][0]["region"] = bidding_zones_control_areas[area_]
        req = requests.post(url, json=param_body, headers=req_headers)
        raw_data = pd.read_csv(io.StringIO(req.text), sep=";", thousands=',')
        raw_data.columns = [fix_col_name(i) for i in raw_data.columns]
        raw_data["region"] = area_
        df_all = df_all.append(raw_data.rename(columns={"datum": "date", "uhrzeit": "time_of_day"}))
    df_all["datetime"] = pd.to_datetime(df_all["date"] + " " + df_all["time_of_day"], format="%b %d, %Y %I:%M %p")
    df_all = df_all.drop(columns=["date", "time_of_day"])
    df_all = df_all.replace("-", np.nan).reset_index(drop=True)
    for i in df_all.columns.difference(["region", "datetime"]):
        if "-" in i:
            df_all[i.replace("-", "_")] = df_all[i].astype(str).apply(lambda x: x.replace(",", "")).astype(float)
            del df_all[i]
        else:
            df_all[i] = df_all[i].astype(str).apply(lambda x: x.replace(",", "")).astype(float)

    df_all["createdat"] = datetime.today()
    # df_all[df_all[df_all.columns.difference(["region", "datetime"])].astype(float)
    # df_all.to_csv(key + ".csv", index=False)
    return df_all
