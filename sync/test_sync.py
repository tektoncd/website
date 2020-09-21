import unittest
import tempfile
import shutil
import ntpath
import os

from sync import get_links
from sync import transform_links
from sync import is_url
from sync import is_ref
from sync import remove_ending_forward_slash
from sync import get_tags
from sync import get_file_dirs
from sync import download_files
from sync import yaml_files_to_list
from sync import get_files


class TestSync(unittest.TestCase):

    # Utils

    def path_leaf(self, path):
        head, tail = ntpath.split(path)
        return tail or ntpath.basename(head)

    def read_and_delete_file(self, name):
        file = open(name, "r")
        text = file.read()
        file.close()
        os.remove(name)
        return text

    # Tests

    def test_multiple_get_links(self):
        """ This will ensure that get links will
        return a list of multiple md links """
        expected = ["www.link.com", "./link"]
        result = get_links("this is a [link](www.link.com) and [link](./link)")

        for index, link in enumerate(result):
            self.assertEqual(link.get("href"), expected[index])

    def test_is_ref(self):
        """ Verify if a string is a reference. A reference is
        defined as  a string where its first character is a hashtag """
        self.assertEqual(False, is_ref(""))
        self.assertEqual(True, is_ref("#footer"))
        self.assertEqual(False, is_ref("www.google.com"))

    def test_remove_ending_forward_slash(self):
        """ Remove a slash if it is the last character in a string """
        expected = remove_ending_forward_slash("www.google.com/")
        self.assertEqual("www.google.com", expected)

    def test_get_tags(self):
        """ map a list of dictionaries to only
        have name, displayName feilds """
        excepted = [{'name': 'test_tag', 'displayName': 'test_display'}]
        tags = {'tags': [
            {
                'name': 'test_tag',
                'displayName': 'test_display',
                'files': []
            },
        ]}

        self.assertEqual(get_tags(tags), excepted)

    def test_download_files(self):
        """ Download file to tmp directory if url is valid """
        excepted = True
        dirpath = tempfile.mkdtemp()
        result = download_files(
            "https://raw.githubusercontent.com/tektoncd/pipeline/master",
            dirpath,
            [{"README.md": "README.md"}]
        )
        shutil.rmtree(dirpath)
        self.assertEqual(result, excepted)

        dirpath = tempfile.mkdtemp()
        self.assertRaises(
            Exception,
            download_files,
            "http://fake.c0m",
            dirpath,
            [{"test": "test"}]
        )
        shutil.rmtree(dirpath)

    def test_yaml_files_to_list(self):
        """ convert a list of files into a list of dictionaries """
        # create a tmp file with yaml txt
        text = "{displayOrder: 1}"
        result = None
        tmp_name = None

        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp_name = tmp.name
            tmp.write(text.strip().encode())

        excepted = [{'displayOrder': 1}]
        result = yaml_files_to_list([tmp_name])
        self.read_and_delete_file(tmp_name)
        self.assertEqual(result, excepted)

    def test_get_files(self):
        """ create a list of files within a
        directory that contain a valid extension"""
        excepted = None
        result = None

        with tempfile.NamedTemporaryFile(delete=True) as tmp:
            excepted = [tmp.name]
            result = get_files("/tmp", self.path_leaf(tmp.name))

        self.assertEqual(result, excepted)

    def test_get_file_dirs(self):
        expected = (
            'https://github.com/tektoncd/cli/raw/master/docs',
            "/tmp",
            "/tmp",
            [{"README.md": "_index.md"}]
        )

        entry = {
            "component": "CLI",
            "displayOrder": 2,
            "repository": "https://github.com/tektoncd/cli",
            "docDirectory": "docs",
            "tags": [
                {
                    "name": "master",
                    "displayName": "master",
                    "files": [
                        {
                            "README.md": "_index.md"
                        }
                    ]
                }
            ],
            "archive": "https://github.com/tektoncd/cli/tags"
        }

        result = get_file_dirs(entry, 0, "/tmp", "/tmp")
        self.assertEqual(result, expected)

    def test_get_links(self):
        """ return a list of links formated in markdown in a given string"""

        expected = get_links("")
        self.assertEqual([], expected)

        expected = get_links("[link](www.link.com) this is a link")
        self.assertEqual("www.link.com", expected[0].get("href"))

    def test_is_url(self):
        """This will return a test to see if the link is a valid url format"""
        expected = is_url("http://www.fake.g00gl3.com")
        self.assertEqual(True, expected)

        expected = is_url("http://www.google.com")
        self.assertEqual(True, expected)

        expected = is_url("http://www.github.com")
        self.assertEqual(True, expected)

        expected = is_url("./sync.py")
        self.assertEqual(False, expected)

        expected = is_url("www.github.com")
        self.assertEqual(False, expected)

    def test_transform_links(self):
        """Ensure that transform links will turns links to
        relative github link or existing file name"""

        expected = """
        [invalid-relative-link](test.com/./adw/a/d/awdrelative)
        [valid-relative-link](./sync.py)
        [valid-absolute-link](www.github.com)
        [invalid-absolute-link](https://website-invalid-random321.net)
        [valid-ref-link](#footer)
        """
        text = """
        [invalid-relative-link](./adw/a/d/awdrelative)
        [valid-relative-link](./sync.py)
        [valid-absolute-link](www.github.com)
        [invalid-absolute-link](https://website-invalid-random321.net)
        [valid-ref-link](#footer)
        """

        result = None
        tmp_name = None

        # write to file
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp_name = tmp.name
            name = self.path_leaf(tmp_name)
            tmp.write(text.strip().encode())

        # mutate file
        transform_links("", "/tmp", [{name: name}], "test.com")
        # read and delete file
        result = self.read_and_delete_file(tmp_name)

        self.assertEqual(expected.strip(), result.strip())


if __name__ == '__main__':
    unittest.main()
