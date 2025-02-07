import pandas as pd
from pandas import DataFrame
import numpy as np
import xlrd
import matplotlib.pyplot as plt
import pathlib

def read_xls(path: pathlib.Path | str) -> list:
    data = list()
    wb = xlrd.open_workbook(path)
    sheets = wb.sheets()
    for sheet in sheets:
        year = sheet.name
        for i in range(10, 31):
            row: list = sheet.row(i)
            row.pop(0)
            arr = [year]
            for cell in row:
                arr.append(cell.value)
            data.append(arr)
    return data


def write_csv(df: DataFrame, file: str) -> None:
    return df.to_csv(f"./{file}")


def clean_dataframe(df: DataFrame) -> DataFrame:
    return df.rename(
        columns={
            0: "Date",
            1: "Currency",
            2: "Country",
            3: "Buy(USD BID)",
            4: "Sell(USD ASK)",
            5: "Buy(BS. S BID)",
            6: "Sell(BS. S ASK)",
        },
        inplace=True,
    )


def dollar_to_bs_rate(df: DataFrame) -> DataFrame:
    df_bs_dollar_date = df[["Date", "Currency", "Buy(BS. S BID)"]]
    df_bs_dollar_date.drop(
        df_bs_dollar_date[df_bs_dollar_date["Currency"] != "USD"].index, inplace=True
    )
    df_bs_dollar_date["Date"] = df_bs_dollar_date["Date"].astype(str)
    df_bs_dollar_date["Date"] = pd.to_datetime(
        df_bs_dollar_date["Date"], format="%d%m%Y"
    )
    return df_bs_dollar_date

def dollar_to_bs_rate_plot(df: DataFrame):
    df_bs_dollar_date = dollar_to_bs_rate(df)
    plt.xticks(rotation=75)
    df_bs_dollar_date.plot(
        x="Date",
        y="Buy(BS. S BID)",
        ylabel="Bolivar respecto al Dolar",
        figsize=(10, 10),
    )
if __name__ == "__main__":
    pass

