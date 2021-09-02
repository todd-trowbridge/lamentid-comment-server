# use python reddit api wrapper
import praw
# use google storage
from google.cloud import storage
# use to get current time
import calendar
import datetime

# praw setup
reddit = praw.Reddit(
    # create a script app on reddit.com to get these values
    client_id="",
    client_secret="",
    password="",
    user_agent="",
    username="",
)

# todo pull list of subreddits to monitor from cloud storage

# create a new bucket in specific location with storage class


def add_subreddit_bucket(bucket_name):

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

# test
# add_subreddit_bucket("test_bucket")

# lists all buckets


def list_all_buckets():
    bucket_list = []  # bucket list ... lol
    storage_client = storage.Client()
    buckets = storage_client.list_buckets()

    for bucket in buckets:
        bucket_list.append(bucket.name)
    return bucket_list

# test
# list_all_buckets()


def check_save_subreddit_bucket(subreddit_id):
    subredditId = subreddit_id
    bucket_list = list_all_buckets()
    try:
        bucket_list.index(subreddit_id)
        print("bucket {} already exists".format(subredditId))
    except:
        print("creating new bucket for {}".format(subredditId))
        add_subreddit_bucket(subreddit_id)
    return ""

# test
# check_save_subreddit_bucket("t5_123456")

# upload blob as string to cloud storage *blob is any type of mime compliant file*
def upload_json_from_string(json_as_string, bucket_name, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_string(json_as_string)

# test
# upload_json_from_string('{{"hello": "world"}}', "t5_123456", "TEST BLOB")

# get utc time


def getUtcTime():
    current_datetime = datetime.datetime.utcnow()
    current_timetuple = current_datetime.utctimetuple()
    current_timestamp = calendar.timegm(current_timetuple)
    return current_timestamp

# test
print(getUtcTime())

def getSubredditsToMonitor():


# todo uncomment to run praw

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
