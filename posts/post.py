"""
author: {username: "Beeezle", id: "5d0c19fe9ba1373573f27219"}
category: "programming"
comments: [{created: "2019-06-21T00:19:06.357Z",…},…]
created: "2019-06-20T23:44:01.640Z"
id: "5d0c1a419ba137182ef2721a"
score: 191
text: "Now lemme tell ya something, young blood."
title: "FizzleDizzle"
type: "text"
upvotePercentage: 81
views: 5290
votes: [{user: "5d0c19fe9ba1373573f27219", vote: 1}, {user: "5d0c1a609ba13771b7f2721b", vote: 1},…]
"""
from tools.my_dict import MyDict
from users.user import User


class Post(MyDict):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.votes = []
        self.comments = []
        self.upvote_percentage = []
        if self.author:
            self.author = User(**self.author)
