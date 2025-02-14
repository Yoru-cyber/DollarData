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
    df["Date"] = pd.to_datetime(df["Date"])
    df = df[~(df["Date"] <= last_date_db.date)]
    df.sort_values("Date")
    insert_into_database(df)
