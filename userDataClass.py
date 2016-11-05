import indicoio
import warnings
import pyredb as pydb
import Backend as twitData
import math

class UserData:
    """
    Fields:
        (can be added with parameter updaters)
        realName: String
        twitterHandle: String
        opinionString: String
        politicalParty: String
        Mood: String


    """
    def __init__(self):
        self.realName = ""
        self.twitterHandle = ""
        self.opinionString = ""
        self.politicalParty = ""
        self.mood = ""

    def __str__(self):
        return "Real Name: " + self.realName + "\nTwitter Handle: " + self.twitterHandle + "\nOpinion: " + \
               self.opinionString + "\nParty: " + self.politicalParty + "\nMood: " + self.mood

    # Parameter updaters

    # ------------------------------------------------------------------------------------------------------------------
    # updateRealName takes self and a string called inName and mutates self to make the user's
    #   real name be the inputted string.
    # updateRealName: UserData Str -> None
    # Effects: self is mutated
    def updateRealName(self, inName):
        self.realName = inName

    # updateHandle takes self and a string called inHandle and mutates self to make the user's
    #   twitter handle be the inputted string.
    # updateRealName: UserData Str -> None
    # Effects: self is mutated
    def updateHandle(self, inHandle):
        self.twitterHandle = inHandle

    # updateOpinion takes self and a string called opiString and mutates self so that
    #   the string that is sent to indico is updated with the latest tweet
    # updateMood: UserDate Str -> None
    # Effects: Mutates self
    def updateOpinion(self, opiString):
        self.opinionString += (" " + opiString)

    # updateParty takes self and a string called inParty and mutates the party
    #   element of self to inParty, which is received from indico.
    # updateMood: UserDate Str -> None
    # Effects: Mutates self
    def updateParty(self, inParty):
        self.politicalParty = inParty

    # updateMood takes self and a string called inMood and mutates the mood property
    #   of self to inMood, which is received from indico.
    # updateMood: UserDate Str -> None
    # Effects: Mutates self
    def updateMood(self, inMood):
        self.mood = inMood
    #------------------------------------------------------------------------------------------------------------------
    #End of Parameter Updaters


    # askInfo takes a UserData and a string called request and returns a string corresponding to
    #   the appropriate data given self.opinionString and request.
    # askInfo: UserData Str Str -> anyof(Str Dict)
    # Requires: Request is anyof(mood, party)
    #           dictOrString is anyof(dictionary string)
    def askInfo(self, request, dictOrString):
        if request == "mood":
            tempDict = indicoio.emotion(self.opinionString, api_key=config["indico_key"])
            if dictOrString == "dictionary":
                return tempDict
            else:
                maxVal = max(tempDict.values())
                for i in tempDict:
                    if tempDict[i] == maxVal:
                        return i
        elif request == "party":
            tempDict = indicoio.political(self.opinionString, api_key=config["indico_key"])
            if dictOrString == "dictionary":
                return tempDict
            else:
                maxVal = max(tempDict.values())
                for i in tempDict:
                    if tempDict[i] == maxVal:
                        return i
        else:
            warnings.warn("invalid request", UserWarning)

    # Database Operations
    # ------------------------------------------------------------------------------------------------------------------
    # addToDB takes a UserData and a pyrebase db and mutates the database in order to add UserData to the db.
    # addToDB: UserData Pyrebase -> None
    # Effects: Pyrebase is mutated to include self
    def addToDB(self):
        firedb.addUser(self.twitterHandle, self.realName, self.askInfo("mood", "dictionary"),
                    self.askInfo("party", "dictionary"))

    # compareWithParty takes a UserData and returns a number that discusses how that user's emotions
    #   correspond with the average emotion of their political party in the form of error from these emotions.
    # compareWithParty: UserData Pyrebase -> Str
    def compareWithParty(self):
        usersList = firedb.getAll()
        emotionsList = ["anger", "joy", "sadness", "surprise", "fear"]
        partiesList = ["Green", "Liberal", "Conservative", "Libertarian"]
        emotionsOfUserParty = [0, 0, 0, 0, 0]
        partyCount = 0

        for i in usersList:
            tempParty = [i["Green"],i["Liberal"],i["Conservative"],i["Libertarian"]]
            probableParty = tempParty.index(max(tempParty))
            if probableParty == self.politicalParty:
                tempEmotion = [i["anger"], i["joy"], i["sadness"], i["surprise"], i["fear"]]
                for i in range(0,len(tempEmotion)):
                    emotionsOfUserParty[i] += tempEmotion[i]
                partyCount += 1

        if partyCount == 0:
            return 0
        for i in range(0, len(emotionsOfUserParty)):
            emotionsOfUserParty[i] = emotionsOfUserParty[i]/partyCount

        error = 0
        userD = self.askInfo("mood", "dictionary")
        userMood = [userD["anger"], userD["joy"], userD["sadness"], userD["surprise"], userD["fear"]]
        for i in range(0,len(emotionsOfUserParty)):
            tempError = math.sqrt(math.pow(userMood[i]-emotionsOfUserParty[i], 2))
            error += tempError

        return error

    # interpretError takes a float point value and returns a string telling the user about their level of difference in
    #   emotion between them and their party in aggregate.
    # interpretError: Float -> Str
    """
    def interpretError(floatIn):
        borders = [10, 30, 50, 70, 90, 1000000]
        textAssociation = [
            "Your tweeted emotion matches highly with your tweeted political party: ",
            "Your tweeted emotion is fairly matched up with your tweeted political party: ",
            "Your tweeted emotion is moderately matched with your tweeted political party: ",
            "Your tweeted emotion is less than moderately well associated with your tweeted political party",
            "Your tweeted emotion poorly matches with your tweeted political party: ",
            "It is highly unlikely that your tweeted emotion matches that of the others in your political party given the data."
        ]
        for i in range(0, len(borders)):
            if floatIn < borders[i]:
                return textAssociation[i]
            else:
                pass


    """
    # ------------------------------------------------------------------------------------------------------------------
    # End of Database Operations



if __name__ == "__main__":
    #Tests
    # get api keys securely
    config = {}
    with open("config.py") as f:
        code = compile(f.read(), "config.py", 'exec')
        exec(code, config)
    f.close()
    firedb = pydb.LogiticaPolitica()

    # Test each individual operation.
    """
    basicTest1 = UserData()
    # print(basicTest1)
    userHandle = "ethguo"
    basicTest1.updateHandle(userHandle)
    # basicTest1.updateOpinion("I have an opinion")
    # print(basicTest1)
    tdata = twitData.getTweets(basicTest1.twitterHandle)
    basicTest1.updateOpinion(tdata[1])
    basicTest1.updateRealName(tdata[0])
    print("asdasdsadsadas")
    print(basicTest1.opinionString)
    # print(basicTest1)
    basicTest1.updateMood(basicTest1.askInfo("mood", "string"))
    print(basicTest1)
    basicTest1.updateParty(basicTest1.askInfo("party", "string"))
    print(basicTest1)
    print(basicTest1.askInfo("mood", "dictionary"))
    print(basicTest1.askInfo("party", "dictionary"))
    basicTest1.addToDB()

    print(basicTest1.compareWithParty())
    """

    #Populate the database and test serial tweets
    # CHANGE THIS TO ONE WHEN THE DB IS POPULATED
    on = 1
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

    if on == 0:
        for i in politicallyActiveHandles:
            newUser = UserData()
            tweets = twitData.getTweets(i)
            if tweets == []:
                pass
            else:
                newUser.updateHandle(i)
                newUser.updateRealName(tweets[0])
                newUser.updateOpinion(twitData.getTweets(i)[1])
                newUser.updateMood(newUser.askInfo("mood", "string"))
                newUser.updateParty(newUser.askInfo("party", "string"))
                newUser.addToDB()