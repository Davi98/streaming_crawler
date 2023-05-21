from google.cloud import bigquery
from dotenv import load_dotenv
import os
load_dotenv()




class Bigquery:


    def __init__(self, dataset_name, project_id):
        self.dataset_name = dataset_name
        self.project_id = project_id
        self.client = bigquery.Client.from_service_account_json(json_credentials_path=os.environ.get("GOOGLE_CREDENTIALS"))
        self.dataset_ref = self.client.dataset(self.dataset_name)
       

    def load_data_from_gcs(self,spider_name,exec_date):
        try:
            job_config = bigquery.LoadJobConfig(
                source_format=bigquery.SourceFormat.CSV,
                autodetect=True,
                write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
                create_disposition=bigquery.CreateDisposition.CREATE_IF_NEEDED,
                skip_leading_rows=1
                )

            table_id = f"streamingsdata.data.{spider_name}"
   
            job = self.client.load_table_from_uri(f'gs://streamingsdata/{spider_name}/{exec_date}.csv', table_id, job_config=job_config)
            job.result()

  
        except Exception as e:
            print(e)
        
