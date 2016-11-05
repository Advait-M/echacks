import indicoio
config = {}
with open("config.py") as f:
    code = compile(f.read(), "config.py", 'exec')
    exec(code, config)
class UserData:
    def __init__(self):
        self.opinionString = ""
        self.politicalParty = ""
        self.mood = ""

    def __str__(self):
        return "Opinion: " + self.opinionString +"\nParty: "+self.politicalParty+"\nMood: "+self.mood

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
    # askInfo: UserData Str -> Str
    # Requires: Request is anyof(mood, party)
    def askInfo(self, request):
        if request == "mood":
            tempDict = indicoio.emotion(self.opinionString, api_key=config["indico_key"])
            maxVal = max(tempDict.values())
            for i in tempDict:
                if tempDict[i] == maxVal:
                    return i
        elif request == "party":
            tempDict = indicoio.political(self.opinionString, api_key=config["indico_key"])
            maxVal = max(tempDict.values())
            for i in tempDict:
                if tempDict[i] == maxVal:
                    return i
        else:
            raise Exception



#Tests
basicTest1 = UserData()
print(basicTest1)
basicTest1.updateOpinion("I have an opinion")
print(basicTest1)
basicTest1.updateOpinion("about stuff")
print(basicTest1)
basicTest1.updateMood(basicTest1.askInfo("mood"))
print(basicTest1)
basicTest1.updateParty(basicTest1.askInfo("party"))
print(basicTest1)