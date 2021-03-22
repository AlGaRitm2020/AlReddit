from datetime import datetime
from pprint import pprint


class InMemoryPostsRepo:
    def __init__(self):
        self.next_id = 1
        self.by_id = {}

    def get_all(self):
        return tuple(self.by_id.values())

    def get_by_id(self, id):
        return self.by_id.get(id, None)

    def get_by_username(self, username):
        result = []
        for post in self.by_id.values():
            if post.author.username == username:
                result.append(post)
        return tuple(result)

    def get_by_category(self, category):
        result = []
        for post in self.by_id.values():
            if post.category == category:
                result.append(post)
        return tuple(result)

    def request_create(self, post):
        post.id = self.next_id
        post.created = datetime.now()
        self.by_id[post.id] = post
        self.next_id += 1
        return post

    def request_delete(self, id, user):
        post = self.get_by_id(id)
        if not post:
            return f'Post does not author of this post id: {id}'
        if post.author.id != user.id:
            return f'You are not author of this post is: {id}'
        del self.by_id[id]
        return None
