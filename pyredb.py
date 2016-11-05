#!/usr/bin/env python3

from pyrebase import *
import config as cf

class WaitNoMore:
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


if __name__ == "__main__":
    test = WaitNoMore()
    test.start()
    print("a")
