import json
import unittest

from reviewington.comment import Comment
from reviewington.repository import Repository

TEST_REPO_ID = "HomeXLabs/reviewington-test"


class TestComment(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.repository = Repository(TEST_REPO_ID)

    def test_initialize(self):
        comments = TestComment.repository.get_pr_comments()
        first_comment = comments[0].to_json()
        with open("test/test_comment/expected_pr_comments.json", "r") as f:
            expected = json.load(f)
        self.assertEquals(first_comment, expected)


if __name__ == "__main__":
    unittest.main()
