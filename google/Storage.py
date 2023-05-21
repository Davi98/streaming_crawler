from google.cloud import storage
import os
from dotenv import load_dotenv
load_dotenv()


class Storage:

    def __init__(self, bucket_name):
        self.storage_client = storage.Client.from_service_account_json(json_credentials_path=os.environ.get("GOOGLE_CREDENTIALS"))
        self.bucket = self.storage_client.get_bucket(bucket_name)

    def upload_file(self,file_name,file_path):
        blob = self.bucket.blob(file_name)
        try:
            blob.upload_from_filename(file_path)
        except Exception as e:
            print(e)




