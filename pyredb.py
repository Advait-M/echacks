#!/usr/bin/env python3

from pyrebase import *
import config as cf

class LogiticaPolitica:
    def __init__(self):
        self.config = cf.firebaseStuff
        self.firebase = initialize_app(self.config)
        self.db = self.firebase.database()


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

if __name__ == "__main__":
    test = LogiticaPolitica()
    test.start()
