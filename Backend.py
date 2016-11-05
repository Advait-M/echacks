from twitter import *
config = {}
with open("config.py") as f:
    code = compile(f.read(), "config.py", 'exec')
    exec(code, config)
result_count = 0
latitude = 43.4643#42.3#18.563747#51.474144#49.28402 ##51.474144  # geographical centre of search
longitude = -80.5204#-83#-72.142439#-0.035401#-123.11765 ##-0.035401  # geographical centre of search
radius = 50
max_range = radius # search range in kilometres
num_results = 1 # minimum results to obtain
last_id = None
twitter = Twitter(auth=OAuth(config["access_key"], config["access_secret"], config["consumer_key"], config["consumer_secret"]))
query = twitter.search.tweets(q="", geocode="%f,%f,%dkm" % (latitude, longitude, max_range), count=100,
                                  max_id=last_id, until="2016-11-4")
# print(query)
for result in query["statuses"]:
    print(result["text"])