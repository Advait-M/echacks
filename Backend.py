from twitter import *
def getTweets(handle):

    config = {}
    with open("config.py") as f:
        code = compile(f.read(), "config.py", 'exec')
        exec(code, config)
    f.close()
    twitter = Twitter(auth=OAuth(config["access_key"], config["access_secret"], config["consumer_key"], config["consumer_secret"]))
    results = twitter.statuses.user_timeline(screen_name = handle)
    # print(results)
    # print()
    statii = []
    for status in results:
        statii.append(status["text"])
    print(statii)
    return statii
if __name__ == "__main__":
    getTweets("POTUS")