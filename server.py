# use python reddit api wrapper
import praw
# use google storage
from google.cloud import storage
# use to get current time
import calendar
import datetime
# use for json
import json

# praw setup
reddit = praw.Reddit(
    # create a script app on reddit.com to get these values
    client_id="",
    client_secret="",
    password="",
    user_agent="",
    username="",
)

# create a new bucket in a specific location


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
# bucket_list = list_all_buckets()
# print(bucket_list)


# check if subreddit bucket !exist, save


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
# print(getUtcTime())


def get_subreddits_to_monitor():
    # always in use
    bucket_name = "comment_fetcher_config"
    source_blob_name = "subreddits_to_monitor"
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    # uncomment to upload new list of subreddits
    # data_set = '["cars", "trucks", "autos", "honda", "nissan", "ford", "kia", "tesla", "nfl", "braves", "baseball", "soccer", "hockey", "wallstreetbets", "movies"]'
    # data_set_as_json = json.loads(data_set)
    # print(data_set_as_json)
    # json_as_string = json.dumps(data_set_as_json)
    # blob.upload_from_string(json_as_string)

    # uncomment to download list of subreddits
    json_as_string = blob.download_as_string()
    json_data = json.loads(json_as_string)
    # json_data.append("new_subreddit")
    return json_data


# test
# getSubredditsToMonitor()


def set_blob_metadata(bucket_name, blob_name, utc_time_start, utc_time_end, number_of_comments, subreddit_id):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.get_blob(blob_name)
    # dictionary can be sent as json
    metadata = {}
    utc_time_start = utc_time_start
    utc_time_end = utc_time_end
    number_of_comments = number_of_comments
    subreddit_id = subreddit_id
    for key in ["utc_time_start", "utc_time_end", "number_of_comments", "subreddit_id"]:
        metadata[key] = eval(key)
    blob.metadata = metadata
    blob.patch()
    # print("The metadata for the blob {} is {}".format(blob.name, blob.metadata))

# test
# set_blob_metadata("comment_fetcher_config", "subreddits_to_monitor",
#                   1630552522, 1630551922, 1000, "t5_12345")


def convert_list_of_subreddits_to_string():
    list_of_subreddits = get_subreddits_to_monitor()
    seperator = "+"
    return seperator.join(list_of_subreddits)

# test
# string_of_subreddits_to_monitor = convert_list_of_subreddits_to_string()

# for loop config
number_of_comments_to_fetch = 10
dict_of_subreddits = {}

# subreddits to monitor, fetched from cloud storage
string_of_subreddits_to_monitor = convert_list_of_subreddits_to_string()

# comment fetch from reddit
for comment in reddit.subreddit(string_of_subreddits_to_monitor).stream.comments():
    # create custom comment
    custom_comment = {}

    # check if subreddit of comments exists already
    for name, list_of_comments in dict_of_subreddits:
        if name == comment.subreddit_id:
            print("bucket {} already exists".format(index))
        else:
            print("creating new list for {}".format(comment.subreddit_id))
            dict_of_subreddits[comment.subreddit_id] = []

    # add custom comment properties
    if comment.author:
        custom_comment[u'author_id'] = str(
            reddit.redditor(comment.author).id)
    if comment.author:
        custom_comment['author_name'] = str(
            reddit.redditor(comment.author).name)
    if comment.body:
        custom_comment['body'] = comment.body
    if comment.created_utc:
        custom_comment['created_utc'] = float(comment.created_utc)
    if comment.distinguished:
        custom_comment['distinguished'] = comment.distinguished
    if comment.edited:
        custom_comment['edited'] = comment.edited
    if comment.id:
        custom_comment['id'] = comment.id
        doc_ref = ""
    if comment.is_submitter:
        custom_comment['is_submitter'] = comment.is_submitter
    if comment.link_id:
        custom_comment['link_id'] = comment.link_id
    if comment.parent_id:
        custom_comment['parent_id'] = comment.parent_id
    if comment.subreddit_id:
        custom_comment['subreddit_id'] = comment.subreddit_id
    if comment.saved:
        custom_comment['saved'] = comment.saved
    if comment.score:
        custom_comment['score'] = comment.score
    if comment.stickied:
        custom_comment['stickied'] = comment.stickied

    # uncomment to include data

    # if comment.permalink: custom_comment['permalink'] = comment.permalink
    # if comment.replies: custom_comment['replies'] = comment.replies
    # uncomment to include data
    # if comment.submission: custom_comment['submission'] = comment.submission
    # if comment.subreddit: custom_comment['subreddit'] = comment.subreddit
    # uncomment to include data
    # if comment.body_html:
    #     custom_comment['body_html'] = str(comment.body_html)

    # push comment to batch of comments
    


    # todo send to cloud storage
