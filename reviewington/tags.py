import re

TAGS = [
    {"id": "change", "name": "Change"},
    {"id": "question", "name": "Question"},
    {"id": "concern", "name": "Concern"},
    {"id": "discussion", "name": "Discussion"},
    {"id": "praise", "name": "Praise"},
    {"id": "suggestion", "name": "Suggestion"},
    {"id": "nitpick", "name": "Nitpick"},
    {"id": "guide", "name": "Guide"},
    {"id": "none", "name": "None"},
]

TAG_IDS = [tag["id"] for tag in TAGS]


def normalize_tag(tag):
    """Lowercase the tag and removes special chars."""
    tag = tag.lower()
    tag = re.sub("[^A-Za-z0-9]+", "", tag)
    return tag
