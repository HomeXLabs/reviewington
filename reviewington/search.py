from typing import List

from reviewington.discussion import Discussion
from reviewington.tags import TAGS


def has_tag_match(discussion: Discussion, selected_tags: List[str]) -> bool:
    """Returns discussions that match tag or we don't care about tags."""
    return (
        len(selected_tags) == 0
        or discussion.tag in selected_tags
        or (discussion.tag == "null" and "none" in selected_tags)
    )


def has_path_match(discussion: Discussion, filepath: str) -> bool:
    """Returns only discussions that occur on given filepath."""
    remove_leading_frontslash = filepath[1:]
    return discussion.path.startswith(remove_leading_frontslash)


def has_comment_search_match(discussion: Discussion, search_query: str) -> bool:
    """Returns discussions that contain the search in any comment."""
    return any(c for c in discussion.comments if search_query in c.body.lower())


def has_code_search_match(discussion: Discussion, search_query: str) -> bool:
    """Returns discussions that contain the search in code diff."""
    return search_query in discussion.diff_hunk.lower()


def has_search_match(discussion: Discussion, search_query: str) -> bool:
    """Returns discussions that satisfy the search criteria."""
    sq = search_query.lower()
    return has_comment_search_match(discussion, sq) or has_code_search_match(discussion, sq)


def search_discussions(
    discussions: List[Discussion],
    filepath: str,
    search_query: str,
    selected_tags: List[str],
) -> List[Discussion]:

    filtered_discussions = [
        d
        for d in discussions
        if (
            has_tag_match(d, selected_tags)
            and has_path_match(d, filepath)
            and has_search_match(d, search_query)
        )
    ]

    return filtered_discussions
