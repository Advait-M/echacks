import indicoio
import warnings
import pyredb as pydb

class UserData:
    def __init__(self):
        self.realName = ""
        self.twitterHandle = ""
        self.opinionString = ""
        self.politicalParty = ""
        self.mood = ""

    def __str__(self):
        return "Real Name: " + self.realName + "\nTwitter Handle: "+ self.twitterHandle + "\nOpinion: " + \
               self.opinionString +"\nParty: "+self.politicalParty+"\nMood: "+self.mood

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

    # askInfo takes a UserData and a string called request and returns a string corresponding to
    #   the appropriate data given self.opinionString and request.
    # askInfo: UserData Str Str -> Str
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

    # addToDB takes a UserData and a pyrebase db and mutates the database in order to add UserData to the db.
    # addToDB: UserData Pyrebase -> None
    # Effects: Pyrebase is mutated to include self
    def addToDB(self):
        pydb.addUser(self.twitterHandle, self.realName, self.askInfo("mood", "dictionary"),\
                     self.askInfo("party", "dictionary"))

        """
        # compareWithParty takes a UserData and a pyrebase db and returns a string that discusses how that user's emotions
        #   correspond with the average emotion of their political party.
        # compareWithParty: UserData Pyrebase -> Str
        def compareWithParty(self, db):

        """

        """
        # deleteFromDB takes a UserData and a pyrebase db and mutates db to remove UserData from it.
        # deleteFromDB: UserData Pyrebase -> None
        # Effects: Mutates db so that UserData is removed.
        def deleteFromDB(self, db):

        """

if __name__ == "__main__":
    #Tests
    # get api keys securely
    config = {}
    with open("config.py") as f:
        code = compile(f.read(), "config.py", 'exec')
        exec(code, config)
    f.close()

    basicTest1 = UserData()
    print(basicTest1)
    basicTest1.updateOpinion("I have an opinion")
    print(basicTest1)
    basicTest1.updateOpinion("about stuff")
    print(basicTest1)
    basicTest1.updateMood(basicTest1.askInfo("mood", "string"))
    print(basicTest1)
    basicTest1.updateParty(basicTest1.askInfo("party", "string"))
    print(basicTest1)

