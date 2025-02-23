
import os


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = ""

client = storage.Client()

buckets = list(client.list_buckets())
print("Buckets:", buckets)
