import re
from typing import List

import aiohttp
import requests

from .datatypes import Post
from .utils import _load_cache, _save_cache


class BaseClient:
    def __init__(self) -> None:
        self.cache = _load_cache()

    def check_subreddit(self, subreddit: str) -> bool:
        regex = re.compile(r"r\/[a-zA-Z0-9_]+")
        if regex.match(subreddit):
            return True

        return False

    def _update_cache(self, subreddit: str, posts: List[Post]) -> None:
        """Updates the cache.

        This method should only be used internally. Not by the user.

        Args
        ----
        `subreddit` type of `str`
            The subreddit to update the cache for
        `posts` type of `List[Post]`
            The posts to update the cache with"""
        self.cache[subreddit] = posts
        _save_cache(self.cache)

    def _get_from_cache(self, subreddit: str) -> List[Post]:
        """Gets posts from the cache.

        This method should only be used internally. Not by the user.

        Args
        ----
        `subreddit` type of `str`
            The subreddit to get posts from

        Returns
        -------
        `List[Post]` type of `list`
            A list of posts"""
        try:
            return self.cache[subreddit]
        except KeyError:
            self.cache[subreddit] = []
            _save_cache(self.cache)
            return self.cache[subreddit]


class Client(BaseClient):
    """The Client class for getting posts from reddit."""

    def __init__(self) -> None:
        super().__init__()

    async def GetPosts(self, subreddit: str) -> List[Post]:
        """Fetches from reddit .

        This method is asynchronous.

        Args
        ----
        `subreddit` type of `str`
            The subreddit to get posts from

        Returns
        -------
        `List[Post]` type of `list`
            A list of posts"""
        if not self.check_subreddit(subreddit):
            raise ValueError("Invalid subreddit")

        if subreddit in self.cache:
            if len(self.cache[subreddit]) == 0:
                self.cache[subreddit] = await self.FetchPosts(subreddit)
                _save_cache(self.cache)
            return self.cache[subreddit]

        try:
            posts = await self.FetchPosts(subreddit)
            self._update_cache(subreddit, posts)
        except RuntimeError:
            posts = self._get_from_cache(subreddit)
        return posts

    async def FetchPosts(self, subreddit: str) -> List[Post]:
        """Fetches posts directly from reddit. Too many requests will result in a 429 error.

        This method is asynchronous.

        Args
        ----
        `subreddit` type of `str`
            The subreddit to fetch posts from

        Returns
        -------
        `List[Post]` type of `list`
            A list of posts"""
        if not self.check_subreddit(subreddit):
            raise ValueError("Invalid subreddit")

        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://www.reddit.com/{subreddit}/new.json"
            ) as response:
                resp_json: dict = await response.json()
                if response.status == 429:
                    raise RuntimeError("429: Too many requests")
                elif response.status == 404:
                    raise ValueError("404: Subreddit not found")

        resp_json: list = resp_json["data"]["children"]
        childrens = []

        for child in resp_json:
            child = child["data"]
            childrens.append(
                Post(
                    Title=child["title"],
                    Author=child["author"],
                    Comments=child["num_comments"],
                    CreatedAt=child["created_utc"],
                    Downvotes=child["downs"],
                    Id=child["id"],
                    IsVideo=child["is_video"],
                    MediaURL=child["url"],
                    NSFW=child["over_18"],
                    PermanentLink=child["permalink"],
                    Pinned=child["pinned"],
                    Spoiler=child["spoiler"],
                    Subreddit=child["subreddit"],
                    SubredditType=child["subreddit_type"],
                    Upvotes=child["ups"],
                    UpvoteRatio=child["upvote_ratio"],
                    Hidden=child["hidden"],
                    Locked=child["locked"],
                )
            )

        return childrens


class ClientSync(BaseClient):
    """The same as Client, but synchronous."""

    def __init__(self) -> None:
        super().__init__()

    def GetPosts(self, subreddit: str) -> List[Post]:
        """Fetches from reddit.

        This method is synchronous.

        Args
        ----
        `subreddit` type of `str`
            The subreddit to get posts from

        Returns
        -------
        `List[Post]` type of `list`
            A list of posts"""
        if not self.check_subreddit(subreddit):
            raise ValueError("Invalid subreddit")

        if subreddit in self.cache:
            if len(self.cache[subreddit]) == 0:
                self.cache[subreddit] = self.FetchPosts(subreddit)
                _save_cache(self.cache)
            return self.cache[subreddit]

        try:
            posts = self.FetchPosts(subreddit)
            self._update_cache(subreddit, posts)
        except RuntimeError:
            posts = self._get_from_cache(subreddit)
        return posts

    def FetchPosts(self, subreddit: str) -> List[Post]:
        """Fetches posts directly from reddit.
        Too many requests will result in a 429 error.

        This method is synchronous.

        Args
        ----
        `subreddit` type of `str`
            The subreddit to fetch posts from

        Returns
        -------
        `List[Post]` type of `list`
            A list of posts"""
        if not self.check_subreddit(subreddit):
            raise ValueError("Invalid subreddit")

        response = requests.get(
            f"https://www.reddit.com/{subreddit}/new.json")
        resp_json: dict = response.json()
        if response.status_code == 429:
            raise RuntimeError("429: Too many requests")
        elif response.status_code == 404:
            raise ValueError("404: Subreddit not found")

        resp_json: list = resp_json["data"]["children"]

        childrens = []

        for child in resp_json:
            child = child["data"]
            childrens.append(
                Post(
                    Title=child["title"],
                    Author=child["author"],
                    Comments=child["num_comments"],
                    CreatedAt=child["created_utc"],
                    Downvotes=child["downs"],
                    Id=child["id"],
                    IsVideo=child["is_video"],
                    MediaURL=child["url"],
                    NSFW=child["over_18"],
                    PermanentLink=child["permalink"],
                    Pinned=child["pinned"],
                    Spoiler=child["spoiler"],
                    Subreddit=child["subreddit"],
                    SubredditType=child["subreddit_type"],
                    Upvotes=child["ups"],
                    UpvoteRatio=child["upvote_ratio"],
                    Hidden=child["hidden"],
                    Locked=child["locked"],
                )
            )

        return childrens
