# use python reddit api wrapper
import praw
# use google storage
from google.cloud import storage
# use io to create virtual files without saving
import io

# praw setup
reddit = praw.Reddit(
    # create a script app on reddit.com to get these values
    client_id="Sebmbo0V4E9LKBEHo0NK6A",
    client_secret="1dgyT3OUVzySOqzEUPH3TzRDjvpFTg",
    password="nivbow-hudCu3-sewwat",
    user_agent="testscript by u/lamentid",
    username="lamentid",
)

# pull list of subreddits to monitor from firestore

def add_subreddit_bucket(bucket_name):
    """Create a new bucket in specific location with storage class"""

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    bucket.storage_class = "STANDARD"
    new_bucket = storage_client.create_bucket(bucket, location="US-EAST1")

    print(
        "Created bucket {} in {} with storage class {}".format(
            new_bucket.name, new_bucket.location, new_bucket.storage_class
        )
    )
    return new_bucket

def list_buckets():
    """Lists all buckets."""
    bucket_list = []
    storage_client = storage.Client()
    buckets = storage_client.list_buckets()

    for bucket in buckets:
        bucket_list.append(bucket.name)
    return bucket_list

def check_save_subreddit_bucket(subreddit_id):
    subredditId = subreddit_id
    bucket_list = list_buckets()
    try:
        bucket_list.index(subreddit_id)
        print("bucket {} already exists".format(subredditId))
    except:
        print("creating new bucket for {}".format(subredditId))
        add_subreddit_bucket(subreddit_id)
    return ""

# test
check_save_subreddit_bucket("t5_123456")

def upload_blob(json_as_string, bucket_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The path to your file to upload
    # source_file_name = "local/path/to/file"
    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_string(json_as_string)

#test
upload_blob('{{"hello": "world"}}', "t5_123456", "TEST BLOB")



# for comment in reddit.subreddit("").stream.comments():
#     # create custom comment
#     custom_comment = {}

#     # add custom comment properties
#     if comment.author:
#         custom_comment[u'author_id'] = str(reddit.redditor(comment.author).id)
#     if comment.author:
#         custom_comment['author_name'] = str(
#             reddit.redditor(comment.author).name)
#     if comment.body:
#         custom_comment['body'] = comment.body

#     if comment.created_utc:
#         custom_comment['created_utc'] = float(comment.created_utc)
#     if comment.distinguished:
#         custom_comment['distinguished'] = comment.distinguished
#     if comment.edited:
#         custom_comment['edited'] = comment.edited
#     if comment.id:
#         custom_comment['id'] = comment.id
#         doc_ref = ""
#     if comment.is_submitter:
#         custom_comment['is_submitter'] = comment.is_submitter
#     if comment.link_id:
#         custom_comment['link_id'] = comment.link_id
#     if comment.parent_id:
#         custom_comment['parent_id'] = comment.parent_id
#     if comment.subreddit_id:
#         custom_comment['subreddit_id'] = comment.subreddit_id
#     if comment.saved:
#         custom_comment['saved'] = comment.saved
#     if comment.score:
#         custom_comment['score'] = comment.score
#     if comment.stickied:
#         custom_comment['stickied'] = comment.stickied

#     # uncomment to include data
#     # if comment.permalink: custom_comment['permalink'] = comment.permalink
#     # if comment.replies: custom_comment['replies'] = comment.replies

#     # uncomment to include data
#     # if comment.submission: custom_comment['submission'] = comment.submission
#     # if comment.subreddit: custom_comment['subreddit'] = comment.subreddit

#     # uncomment to include data
#     # if comment.body_html:
#     #     custom_comment['body_html'] = str(comment.body_html)

#     # todo send to cloud storage

#     # print comment id to console
#     print('{} added to google cloud storage'.format(comment.id))
