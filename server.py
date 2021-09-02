# use python reddit api wrapper
import praw
# use google storage
from google.cloud import storage

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

def create_bucket_class_location(bucket_name):
    """Create a new bucket in specific location with storage class"""
    # bucket_name = "your-new-bucket-name"

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    bucket.storage_class = "COLDLINE"
    new_bucket = storage_client.create_bucket(bucket, location="us")

    print(
        "Created bucket {} in {} with storage class {}".format(
            new_bucket.name, new_bucket.location, new_bucket.storage_class
        )
    )
    return new_bucket

def list_buckets():
    """Lists all buckets."""

    storage_client = storage.Client()
    buckets = storage_client.list_buckets()

    for bucket in buckets:
        print(bucket.name)

for comment in reddit.subreddit("").stream.comments():
    # create custom comment
    custom_comment = {}

    # add custom comment properties
    if comment.author:
        custom_comment[u'author_id'] = str(reddit.redditor(comment.author).id)
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

    # todo send to cloud storage

    # print comment id to console
    print('{} added to google cloud storage'.format(comment.id))
