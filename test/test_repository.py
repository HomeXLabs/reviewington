import unittest

from reviewington.repository import Repository

TEST_REPO_ID = "HomeXLabs/reviewington-test"


class TestRepository(unittest.TestCase):
    def test_initialize(self):
        repository = Repository(TEST_REPO_ID)
        self.assertEqual(repository.name, TEST_REPO_ID)


if __name__ == "__main__":
    unittest.main()
