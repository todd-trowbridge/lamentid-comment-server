# to pass data to firebase
import firebase_admin
import praw
from firebase_admin import credentials, firestore

# Use a service account
path = "./credentials.json"
cred = credentials.Certificate(path)
firebase_admin.initialize_app(cred)

db = firestore.client()

# praw setup
reddit = praw.Reddit(
    # create a script app on reddit.com to get these values
    client_id="Sebmbo0V4E9LKBEHo0NK6A",
    client_secret="1dgyT3OUVzySOqzEUPH3TzRDjvpFTg",
    password="nivbow-hudCu3-sewwat",
    user_agent="testscript by u/lamentid",
    username="lamentid",
)

# todo pull list of subreddits to monitor from firestore
subredditsToMonitor_ref = db.collection(u'configs').document(u'subredditsToMonitor')
subredditsToMonitor_doc = subredditsToMonitor_ref.get().to_dict()
# print(subredditsToMonitor_doc['subreddits'])
subredditsString = list(subredditsToMonitor_doc['subreddits'])
print('+'.join(subredditsString))

# brands to monitor
brandsToScan = ["Kia", "Nissan", "Honda", "Ford", "Tesla"]
kiaProducts = ["Soul", "Seltos", "Sportage", "Niro", "Sorento", "Telluride", "Carnival"]
nissanProducts = ["Versa", "Senta", "Altima", "Maxima", "Leaf", "GT-R", "GTR", "Kicks", "Rogue Sport", "Rogue", "Murano", "Pathfinder", "Armada", "Ariya", "Frontier", "Titan"]
hondaProducts = ["HR-V", "HRV", "CR-V", "CRV", "Passport", "Pilot", "Civic Sedan", "Civic", "Accord", "Insight", "Accord Hybrid", "Clarity", "Civic Hatchback", "Civic Type-R", "Civic TypeR", "Odyssey", "Ridgeline", "Prologue"]
fordProducts = ["Ecosport", "Escape", "Bronco Sport", "Bronco", "Edge", "Explorer", "Mustang Mach-E", "Mach-E", "Mustang Mach E", "Mach E", "Expediton", "Maverick", "Ranger", "Transit", "F-150", "F 150", "F-150 Lightning", "F 150 Lightning", "Super Duty", "SuperDuty", "Mustang"]
teslaProducts = ["Model S", "Model 3", "Model X", "Model Y"]