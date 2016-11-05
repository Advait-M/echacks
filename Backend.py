from twitter import *
import time

# Use API keys securely
config = {}
with open("config.py") as f:
    code = compile(f.read(), "config.py", 'exec')
    exec(code, config)
f.close()

#Instance Twitter
twitter = Twitter(
auth=OAuth(config["access_key"], config["access_secret"], config["consumer_key"], config["consumer_secret"]))

# getTweets takes a string called handle and produces a list of strings corresponding to the user's name and a long
#   string of all their tweets concatinated.
# getTweets: Str -> listof(Str)
def getTweets(handle):
    #print(handle)

    try:
        results = twitter.statuses.user_timeline(screen_name = handle)
        if results != []:

            # print(results)
            # print()

            statii = []

            #print(results)
            #print(results[0])

            uName = results[0]["user"]["name"]

            #print(uName)

            for status in results:
                statii.append(status["text"])

            # print(statii)

            textS = " ".join(statii)
            while "\n" in textS:
                i = textS.index("\n")
                textS = textS[0:i] + textS[i+1:]

            #print(textS)
            #print([uName, textS])

            return [uName, textS]
        else:
            return[]
    except TwitterHTTPError:
        return []
if __name__ == "__main__":
    politicallyActiveHandles = [
        "RepublicanStudy",
        "daveweigel",
        "fixfelicia",
        "pwire",
        "susanpage",
        "alex_wags",
        "HotlineReid",
        "PElliottAP",
        "bethreinhard",
        "thegarance",
        "mikememoli",
        "ErinMcPike",
        "markknoller",
        "SuzyKhimm",
        "jaketapper",
        "nprpolitics",
        "McClatchyDC",
        "SwingState",
        "Wonkette",
        "GOP12",
        "LizMair",
        "LarrySabato",
        "Dave_Wasserman",
        "anamariecox",
        "samgf",
        "donnabrazile",
        "chucktodd",
        "cbellantoni",
        "Atrios",
        "nicopitney",
        "ggreenwald",
        "wonkroom",
        "stevebenen",
        "AlanColmes",
        "ewerickson",
        "mindyfinn",
        "dmataconis",
        "TPCarney",
        "jbarro",
        "Heminator",
        "reihansalam",
        "nathandaschle",
        "fivethirtyeight",
        "ppppolls",
        "MysteryPollster",
        "RasmussenPoll"]

