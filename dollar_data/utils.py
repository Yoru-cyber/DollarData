"""This module provides multiple helpers functions to achieve some task for the project, read files, scrape data and so goes on."""

import os
from pathlib import Path
import pandas as pd
from pandas import DataFrame
from sqlalchemy import Engine, create_engine
import xlrd
import matplotlib.pyplot as plt
import pathlib
import requests
from bs4 import BeautifulSoup

pd.options.mode.copy_on_write = True

cwd = os.getcwd()
engine = create_engine(f"sqlite:////{cwd}/database.db", echo=True)


def read_xls(path: pathlib.Path | str) -> list:
    """Reads data from an Excel (.xls) file.

    This function opens an Excel file specified by the given path, iterates through each sheet,
    and extracts data from rows 10 to 30 which hold the values of currencies and Buy BID etc.
    The first column of each row is removed, and the sheet name (assumed to be the date when the information was written)
    is prepended to each row's data.

    :param path: The path to the Excel file.  Can be a string or a pathlib.Path object.
    :type path: pathlib.Path | str
    :return: A list of lists, where each inner list represents a row of data.  The first element
             of each inner list is the sheet name (year), followed by the cell values.
    :rtype: list
    :raises FileNotFoundError: If the specified file does not exist.
    :raises XLRDError: If there is an error reading the Excel file (e.g., invalid format).

    :Example:

    .. code-block:: python

        import pathlib
        path = pathlib.Path("data.xls")  # Or path = "data.xls"
        data = read_xls(path)
        print(data)
        # Example output
        # [['2023', 'USD', 10.74, 20.14, 30.01, 50.20], ['2023', 40.52, 50.47, 60.69], ...]
    """
    data = list()
    wb = xlrd.open_workbook(path)
    sheets = wb.sheets()
    for sheet in sheets:
        # The current format names each sheet with the date
        date = sheet.name
        # The current format holds in these rows the data with the relevant information
        for i in range(10, 31):
            row: list = sheet.row(i)
            # The first cell of the row is blank, so it's better to remove
            row.pop(0)
            arr = [date]
            for cell in row:
                arr.append(cell.value)
            data.append(arr)
    return data


def clean_dataframe(df: DataFrame) -> None:
    """Renames columns in a Pandas DataFrame.

    This function renames the columns of the input DataFrame to more descriptive names,
    making the data easier to work with.  The renaming is done in-place, modifying the
    original DataFrame.

    :param df: The Pandas DataFrame to clean.
    :type df: DataFrame
    :raises TypeError: If the input is not a Pandas DataFrame.
    :raises KeyError: If the DataFrame does not have the expected columns (0 through 6).
    :return: None (the DataFrame is modified in-place).
    :rtype: None

    :Example:

    .. code-block:: python

        import pandas as pd
        data = {'0': [1, 2, 3], '1': ['A', 'B', 'C'], '2': ['X', 'Y', 'Z'],
        '3': [10, 20, 30], '4': [11, 21, 31], '5': [12, 22, 32], '6': [13, 23, 33]}
        df = pd.DataFrame(data)
        clean_dataframe(df)
        print(df.columns)
        Index(['Date', 'Currency', 'Country', 'Buy(USD BID)',
        'Sell(USD ASK)', 'Buy(BS. S BID)', 'Sell(BS. S ASK)'],
        dtype='object')
    """
    if not isinstance(df, DataFrame):
        raise TypeError("Input must be a Pandas DataFrame")

    try:
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
    except KeyError as e:
        raise KeyError(f"DataFrame does not have the expected columns: {e}")


def dollar_to_bs_rate(df: DataFrame) -> DataFrame:
    """Extracts and formats USD to BS. S exchange rates from a DataFrame.

    This function takes a DataFrame containing currency exchange rate data, filters it to
    include only USD to BS. S rates, converts the 'Date' column to datetime objects, and
    returns a new DataFrame containing only the 'Date', 'Currency', and 'Buy(BS. S BID)'
    columns for USD.

    :param df: The input DataFrame containing currency exchange rate data.  Must have
               columns 'Date', 'Currency', and 'Buy(BS. S BID)'.
    :type df: DataFrame
    :raises TypeError: If the input is not a Pandas DataFrame.
    :raises KeyError: If the DataFrame does not contain the required columns.
    :return: A new DataFrame containing the USD to BS. S exchange rates with a datetime 'Date' column.
    :rtype: DataFrame

    :Example:

    .. code-block:: python

        import pandas as pd
        data = {'Date': ['20012024', '21012024', '20012024'],
                'Currency': ['USD', 'EUR', 'USD'],
                'Buy(BS. S BID)': [10, 20, 30]}
        df = pd.DataFrame(data)
        usd_rates = dollar_to_bs_rate(df)
        # print(usd_rates)
        #   Date Currency  Buy(BS. S BID)
        # 0 2024-01-20      USD              10
        # 2 2024-01-20      USD              30
    """
    if not isinstance(df, DataFrame):
        raise TypeError("Input must be a Pandas DataFrame")

    required_columns = ["Date", "Currency", "Buy(BS. S BID)"]
    if not all(col in df.columns for col in required_columns):
        raise KeyError(f"DataFrame must contain columns: {required_columns}")

    df_bs_dollar_date = df[
        ["Date", "Currency", "Buy(BS. S BID)"]
    ].copy()  # Create a copy to avoid SettingWithCopyWarning

    df_bs_dollar_date.drop(
        df_bs_dollar_date[df_bs_dollar_date["Currency"] != "USD"].index, inplace=True
    )
    df_bs_dollar_date["Date"] = pd.to_datetime(
        df_bs_dollar_date["Date"], format="%d%m%Y"
    )
    return df_bs_dollar_date


def dollar_to_bs_rate_plot(df: DataFrame):
    """Generates a plot of the USD to BS. S exchange rate over time.

    This function takes a Pandas DataFrame, extracts the USD to BS. S exchange rate data
    using the `dollar_to_bs_rate` function, and creates a line plot of the rate over time.
    The plot is displayed using Matplotlib.

    :param df: The input DataFrame containing currency exchange rate data.
    :type df: DataFrame

    :raises TypeError: If the input is not a Pandas DataFrame.
    :raises KeyError: If the DataFrame does not contain the required columns.
    :raises FileNotFoundError: If the function `dollar_to_bs_rate` cannot find the file.
    :raises XLRDError: If the function `dollar_to_bs_rate` fails to read the file.

    :return: None

    :Example:

    .. code-block:: python

        import pandas as pd
        # Sample DataFrame (replace with your actual data)
        data = {'Date': ['20012024', '21012024', '20012024'],
                'Currency': ['USD', 'EUR', 'USD'],
                'Buy(BS. S BID)': [10, 20, 30]}
        df = pd.DataFrame(data)
        dollar_to_bs_rate_plot(df)  # Displays the plot.
    """
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
    """Generates and saves a PDF plot of the USD to BS. S exchange rate over time.

    This function takes a Pandas DataFrame, extracts the USD to BS. S exchange rate data
    using the `dollar_to_bs_rate` function, and creates a line plot of the rate over time.
    The plot is then saved as a PDF file named "dollar_to_bs_rate.pdf".

    :param df: The input DataFrame containing currency exchange rate data.
    :type df: DataFrame

    :raises TypeError: If the input is not a Pandas DataFrame.
    :raises KeyError: If the DataFrame does not contain the required columns.
    :raises FileNotFoundError: If the function `dollar_to_bs_rate` cannot find the file.
    :raises XLRDError: If the function `dollar_to_bs_rate` fails to read the file.

    :return: None

    :Example:

    .. code-block:: python

        import pandas as pd
        # Sample DataFrame (replace with your actual data)
        data = {'Date': ['20012024', '21012024', '20012024'],
                'Currency': ['USD', 'EUR', 'USD'],
                'Buy(BS. S BID)': [10, 20, 30]}
        df = pd.DataFrame(data)
        plot_pdf(df)  # Generates and saves the PDF plot.  Waku waku! (Excited!)
    """
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


def scrape_excel() -> str:
    """Scrapes the latest Excel file containing exchange rate data from the BCV website.

    This function fetches the HTML from the BCV website, parses it using BeautifulSoup,
    extracts the link to the latest Excel file, downloads the file, and saves it locally.

    :param None: This function does not take any parameters.

    :return: The full path to the saved Excel file.
    :rtype: str

    :raises requests.exceptions.RequestException: If there's an error during the HTTP request.
    :raises IndexError: If the expected HTML elements are not found on the BCV website.

    :Example:

    .. code-block:: python

        scrape_excel()
        # '/path/to/your/dollar_data/excel_files/last_updated_excel.xls'  # Example path.
    """
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
    file_name = "last_updated_excel.xls"
    path = f"{cwd}/dollar_data/excel_files/"
    Path(path).mkdir(exist_ok=True)
    with open(f"{path}{file_name}", "wb") as f:
        f.write(file_stream.content)
    return f"{path}{file_name}"


def insert_into_database(df: DataFrame):
    """Inserts data from a Pandas DataFrame into a SQL database.

    This function takes a Pandas DataFrame containing historical dollar exchange rate data,
    resets the index, renames the columns to match the database schema, and appends the data
    to the "HistoricalDollar" table in the specified SQL database.

    :param df: The Pandas DataFrame containing the data to insert.
    :type df: DataFrame
    :param engine: The SQLAlchemy Engine object used to connect to the database.
    :type engine: Engine
    :raises TypeError: If the input `df` is not a Pandas DataFrame.
    :raises TypeError: If the input `engine` is not a SQLAlchemy Engine.
    :raises Exception: If an error occurs during the database insertion process.
    :return: None
    :rtype: None

    :Example:

    .. code-block:: python

        import pandas as pd
        from sqlalchemy import create_engine
        # ... database connection details ...
        engine = create_engine('sqlite:////{somepath}/database.db')  # Example
        data = {'DATE': ['2024-01-20'], 'CURRENCY': ['USD'], 'BUYBID': [10]}
        df = pd.DataFrame(data)
        insert_into_database(df, engine)
    """
    if not isinstance(df, DataFrame):
        raise TypeError("Input 'df' must be a Pandas DataFrame")

    if not isinstance(engine, Engine):
        raise TypeError("Input 'engine' must be a SQLAlchemy Engine")

    df = df.reset_index(drop=True)
    df = df.rename(
        columns={"Date": "DATE", "Currency": "CURRENCY", "Buy(BS. S BID)": "BUYBID"}
    )
    try:
        df.to_sql(con=engine, name="HistoricalDollar", if_exists="append", index=False)
    except Exception as e:
        raise Exception(f"Error inserting data into database: {e}")
