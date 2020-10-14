import unittest
import tempfile
import shutil
import ntpath
import os

from sync import get_links
from sync import transform_text
from sync import is_url
from sync import is_ref
from sync import remove_ending_forward_slash
from sync import get_tags
from sync import get_file_dirs
from sync import download_files
from sync import yaml_files_to_dic_list
from sync import get_files
from sync import get_list_of_files


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

    def test_get_list_of_files(self):
        """ get all the values from a list of dics and return a list """
        expected = ["/prefix/f.tmp", "/prefix/t.xt"]
        result = get_list_of_files("/prefix", [{"_": "f.tmp", "__": "t.xt"}])
        self.assertEqual(result, expected)

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
        self.assertEqual(is_ref(""), False)
        self.assertEqual(is_ref("#footer"), True)
        self.assertEqual(is_ref("www.google.com"), False)

    def test_remove_ending_forward_slash(self):
        """ Remove a slash if it is the last character in a string """
        actual = remove_ending_forward_slash("www.google.com/")
        expected = "www.google.com"
        self.assertEqual(actual, expected)

    def test_get_tags(self):
        """ map a list of dictionaries to only
        have name, displayName feilds """
        expected = [{'name': 'test_tag', 'displayName': 'test_display'}]
        tags = {'tags': [
            {
                'name': 'test_tag',
                'displayName': 'test_display',
                'files': []
            },
        ]}

        self.assertEqual(get_tags(tags), expected)

    def test_download_files(self):
        """ Download file to tmp directory if url is valid """
        expected = True
        dirpath = tempfile.mkdtemp()
        actual = download_files(
            "https://raw.githubusercontent.com/tektoncd/pipeline/master",
            dirpath,
            [{"README.md": "README.md"}]
        )
        shutil.rmtree(dirpath)
        self.assertEqual(actual, expected)

        dirpath = tempfile.mkdtemp()
        self.assertRaises(
            Exception,
            download_files,
            "http://fake.c0m",
            dirpath,
            [{"test": "test"}]
        )
        shutil.rmtree(dirpath)

    def test_yaml_files_to_dic_list(self):
        """ convert a list of files into a list of dictionaries """
        # create a tmp file with yaml txt
        text = "{displayOrder: 1}"
        actual = None
        tmp_name = None

        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp_name = tmp.name
            tmp.write(text.strip().encode())

        expected = [{'displayOrder': 1}]
        actual = yaml_files_to_dic_list([tmp_name])
        self.read_and_delete_file(tmp_name)
        self.assertEqual(actual, expected)

    def test_get_files(self):
        """ create a list of files within a
        directory that contain a valid extension"""
        expected = None
        actual = None

        with tempfile.NamedTemporaryFile(delete=True) as tmp:
            expected = [tmp.name]
            actual = get_files("/tmp", self.path_leaf(tmp.name))

        self.assertEqual(actual, expected)

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

        actual = get_file_dirs(entry, 0, "/tmp", "/tmp")
        self.assertEqual(actual, expected)

    def test_get_links(self):
        """ return a list of links formated in markdown in a given string"""
        actual = "www.link.com"

        expected = get_links("")
        self.assertEqual([], expected)

        expected = get_links("[link](www.link.com) this is a link")
        self.assertEqual(actual, expected[0].get("href"))

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

    def test_transform_text(self):
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

        actual = None
        tmp_name = None

        # write to file
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp_name = tmp.name
            name = self.path_leaf(tmp_name)
            tmp.write(text.strip().encode())

        # mutate file
        transform_text("", "/tmp", [{name: name}], "test.com")
        # read and delete file
        actual = self.read_and_delete_file(tmp_name)

        self.assertEqual(actual.strip(), expected.strip())


if __name__ == '__main__':
    unittest.main()
