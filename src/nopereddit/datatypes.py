from dataclasses import dataclass


@dataclass
class Post:
    Title: str
    SubredditType: str
    Subreddit: str
    Hidden: bool
    Pinned: bool
    Spoiler: bool
    Locked: bool
    NSFW: bool
    Author: str
    Comments: int
    PermanentLink: str
    MediaURL: str
    CreatedAt: int
    IsVideo: bool
    Upvotes: int
    Downvotes: int
    Id: str
    UpvoteRatio: float
