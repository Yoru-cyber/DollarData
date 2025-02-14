from datetime import datetime
import pandas as pd
from dollar_data.models import Dollar
from dollar_data.utils import (
    clean_dataframe,
    dollar_to_bs_rate,
    read_xls,
    scrape_excel,
    insert_into_database,
)


def update_database():
    file_path = scrape_excel()
    data = read_xls(file_path)
    last_date_db = Dollar.query.order_by(Dollar.id.desc()).first()
    df = pd.DataFrame(data)
    clean_dataframe(df)
    df = dollar_to_bs_rate(df)
    df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d %H:%M:%S")
    print(df)
    df = df.sort_values("Date", ascending=True).reset_index(drop=True)
    df = df[~(df["Date"] <= last_date_db.date)]
    insert_into_database(df)


def check_missing_entries():
    last_date_row = Dollar.query.order_by(Dollar.id.desc()).first()
    last_date = datetime.strptime(last_date_row.date, "%Y-%m-%d %H:%M:%S")
    actual_date = datetime.strptime(str(datetime.now()), "%Y-%m-%d %H:%M:%S.%f")
    print(abs(last_date - actual_date))
