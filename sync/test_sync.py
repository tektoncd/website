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

def read_and_delete_file(name):
    file = open(name, "r")
    text = file.read() 
    file.close()
    os.remove(name)
    return text

class TestSync(unittest.TestCase):

    def test_multiple_get_links(self):
        """This will ensure that get links will return a list of multiple md links"""        
        expected = ["www.link.com", "./link"]
        result = get_links("this is a [link](www.link.com) and this is a [link](./link)")

        for index, link in enumerate(result):
            self.assertEqual(link.get("href"), expected[index])

    def test_transform_links(self):
        """Ensure that transform links will turns links to relative github link or existing file name"""
        expected = "Hello world [link](test.com/./adw/a/d/awdrelative) and [github](www.github.com)\n"
        result = None
        tmp_name = None
        text = "Hello world [link](test.com/./adw/a/d/awdrelative) and [github](www.github.com)\n"

        #write to file
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp_name = tmp.name
            name = path_leaf(tmp_name)
            tmp.write(text.encode())

        #mutate file  
        transform_links("", "/tmp", [{name : name}], "test.com")
        #read and delete file
        result = read_and_delete_file(tmp_name)
        
        self.assertEqual(expected, result)

if __name__ == '__main__':
    unittest.main()