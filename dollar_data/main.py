import pandas as pd
from pandas import DataFrame
import xlrd
import matplotlib.pyplot as plt
import pathlib
import requests
import sqlite3
from bs4 import BeautifulSoup

pd.options.mode.copy_on_write = True


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


def clean_dataframe(df: DataFrame) -> None:
    df.rename(
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
    df_bs_dollar_date["Date"] = pd.to_datetime(
        df_bs_dollar_date["Date"], format="%d%m%Y"
    )
    return df_bs_dollar_date


def dollar_to_bs_rate_plot(df: DataFrame):
    fig, ax = plt.subplots()
    df_bs_dollar_date = dollar_to_bs_rate(df)
    plt.xticks(rotation=75)
    df_bs_dollar_date.sort_values("Date")
    df_bs_dollar_date.plot(
        ax=ax,
        x="Date",
        y="Buy(BS. S BID)",
        ylabel="Precio Bolívares",
        xlabel="Fecha",
        figsize=(10, 10),
    )
    ax.legend(["Bolívar respecto al Dólar"])


def plot_pdf(df: DataFrame):
    fig, ax = plt.subplots()
    df_bs_dollar_date = dollar_to_bs_rate(df)
    plt.xticks(rotation=75)
    df_bs_dollar_date.sort_values("Date")
    df_bs_dollar_date.plot(
        ax=ax,
        x="Date",
        y="Buy(BS. S BID)",
        ylabel="Precio Bolívares",
        xlabel="Fecha",
        figsize=(10, 10),
    )
    ax.legend(["Bolívar respecto al Dólar"])
    plt.savefig("dollar_to_bs_rate.pdf")


def main():
    data = read_xls("../2_1_2a24_smc.xls")
    data.extend(read_xls("../2_1_2b24_smc.xls"))
    data.extend(read_xls("../2_1_2c24_smc.xls"))
    data.extend(read_xls("../2_1_2d24_smc.xls"))
    html = requests.get(
        "https://www.bcv.org.ve/estadisticas/tipo-cambio-de-referencia-smc",
        verify=False,
    )
    soup = BeautifulSoup(html.text, features="html.parser")
    a = soup.select(
        "#block-system-main > div > div.view-content > table > tbody > tr.odd.views-row-first > td.views-field.views-field-field-diario > span > a"
    )
    url = a[0].get("href")
    file_stream = requests.get(url, verify=False)
    file_name = url.split("/")[-1]
    with open(f"../{file_name}.xls", "wb") as f:
        f.write(file_stream.content)
    data.extend(read_xls(f"../{file_name}.xls"))
    df = pd.DataFrame(data)
    clean_dataframe(df)
    df = dollar_to_bs_rate(df)
    df = df.sort_values("Date")
    df = df.reset_index(drop=True)
    df = df.rename(
        columns={"Date": "DATE", "Currency": "CURRENCY", "Buy(BS. S BID)": "BUYBID"}
    )
    # cnx = sqlite3.connect('../database.db')
    # df.to_sql(name="HistoricalDollar", con=cnx, if_exists="append", index=False)
    # print(df)
    ##dollar_to_bs_rate_plot(df)
    ##plot_pdf(df)


if __name__ == "__main__":
    main()
