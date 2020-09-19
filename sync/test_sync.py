import unittest
import tempfile
import ntpath
import os

from sync import get_links
from sync import transform_links

## Utils ##
def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

class TestSync(unittest.TestCase):

    def test_multiple_get_links(self):
        """This will ensure that get links will return a list of multiple md links"""        
        result = get_links("this is a [link](www.link.com) and this is a [link](./link)")
        expected = ["www.link.com", "./link"]
        index = 0
        for link in result:
            self.assertEqual(link.get("href"), expected[index])
            index += 1

    def test_transform_links(self):
        """Ensure that transform links will turns links to relative github link or existing file name"""
        with tempfile.NamedTemporaryFile() as tmp:
            name = path_leaf(tmp.name)
            transform_links("", "/tmp", [{name : name}], "")

if __name__ == '__main__':
    unittest.main()