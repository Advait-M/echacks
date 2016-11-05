#!/usr/bin/env python3

from pyrebase import *
import config as cf

class LogiticaPolitica:
    def __init__(self):
        self.config = cf.firebaseStuff
        self.firebase = initialize_app(self.config)
        self.db = self.firebase.database()

    # start takes a LogiticaPolitical and starts a db stream to dynamically change and access the database.
    # start: LogiticaPolitica -> None
    # Effects: stream started with db to access and edit.
    def start(self):
        self.stream = self.db.stream(self.streamHandler)


    def streamHandler(self, post):
        event = post["event"]
        key = post["path"]
        value = post["data"]

        if event == "put":
            print(key, ":", value)

    def addUser(self, handle, uName, moods, parties):
        dataDict = dict(moods, **parties)
        dataDict["name"] = uName
        self.db.child(handle).set(dataDict)

    # getAll takes a pyredb and returns a dictionary containing values for each correlation between political parties
    #   and emotion for each entry in the database.
    # getAll: pyredb -> Dict
    def getAll(self):
        all_users = self.db.child("/").get()
        masterList = []
        for user in all_users.each():
            mDict = {}
            mDict["handle"] = user.key()
            mDict["Conservative"] = (user.val())["Conservative"]
            mDict["Green"] = (user.val())["Green"]
            mDict["Liberal"] = (user.val())["Liberal"]
            mDict["Libertarian"] = (user.val())["Libertarian"]
            mDict["fear"] = (user.val())["fear"]
            mDict["joy"] = (user.val())["joy"]
            mDict["surprise"] = (user.val())["surprise"]
            mDict["anger"] = (user.val())["anger"]
            mDict["sadness"] = (user.val())["sadness"]
            mDict["name"] = (user.val())["name"]
            masterList.append(mDict)
        #print(masterList)
        return masterList

if __name__ == "__main__":
    test = LogiticaPolitica()
    test.start()
    test.getAll()