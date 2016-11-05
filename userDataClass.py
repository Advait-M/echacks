import indicoio
import warnings
import pyredb as pydb
import Backend as twitData


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

    # compareWithParty takes a UserData and a pyrebase db and returns a string that discusses how that user's emotions
    #   correspond with the average emotion of their political party.
    # compareWithParty: UserData Pyrebase -> Str
    def compareWithParty(self):
        usersList = firedb.getAll()
        emotionsList = ["anger", "joy", "sadness", "surprise", "fear"]
        partiesList = ["Green", "Liberal", "Conservative", "Libertarian"]
        emotionsOfUserParty = [0, 0, 0, 0, 0]

        for i in usersList:
            tempParty = [i["Green"],i["Liberal"],i["Conservative"],i["Libertarian"]]
            probableParty = tempParty.index(max(tempParty))
            if probableParty == self.politicalParty:
                tempEmotion = [i["anger"], i["joy"], i["sadness"], i["surprise"], i["fear"]]
                probableEmotion = emotionsList.index(max(tempEmotion))
                emotionsOfUserParty[probableEmotion] += 1

        partyEmotion = emotionsList[emotionsOfUserParty.index(max(emotionsOfUserParty))]

        if partyEmotion == self.mood:
            return ["Aligned mood", self.politicalParty, partyEmotion, self.mood]
        else:
            return ["Non-Aligned mood", self.politicalParty, partyEmotion, self.mood]


        """
    # deleteFromDB takes a UserData and a pyrebase db and mutates db to remove UserData from it.
    # deleteFromDB: UserData Pyrebase -> None
    # Effects: Mutates db so that UserData is removed.
    def deleteFromDB(self):

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