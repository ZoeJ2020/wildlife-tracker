
import os


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "crystal@wildlife-451802.iam.gserviceaccount.com"

client = storage.Client()

buckets = list(client.list_buckets())
print("Buckets:", buckets)
