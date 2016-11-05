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
    print(results)
    print(results[0])
    uName = results[0]["user"]["name"]
    print(uName)
    for status in results:
        statii.append(status["text"])
    # print(statii)
    textS = " ".join(statii)
    while "\n" in textS:
        i = textS.index("\n")
        textS = textS[0:i] + textS[i+1:]

    print(textS)
    print([uName, textS])
    return [uName, textS]
if __name__ == "__main__":
    politicallyActiveHandles = [
        "RepublicanStudy",
        "benpolitico",
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

    getTweets("POTUS")