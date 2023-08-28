from google.Bigquery import Bigquery
from google.Storage import Storage
import datetime
import os
import sys

def run_spider(spider_name):
    os.system(f"scrapy crawl {spider_name}")


def upload_to_gcs(exec_date,spider_name):
    storage = Storage('streamingsdata')
    storage.upload_file(f'{spider_name}/{exec_date}.csv',f"downloads/{spider_name}.csv")


def load_to_bq(exec_date,spider_name):
    bq = Bigquery('streamingsdata','data')
    bq.load_data_from_gcs(spider_name,exec_date)

def main():
    spider_name = sys.argv[1]
    exec_date = datetime.datetime.now().strftime("%Y-%m-%d")
    run_spider(spider_name)
    upload_to_gcs(exec_date,spider_name)
    load_to_bq(exec_date,spider_name)


if __name__ == "__main__":
   main()