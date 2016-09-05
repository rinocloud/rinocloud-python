
import unittest
import rinocloud
import shutil
import tempfile
import os


class RinocloudConfigTests(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_set_local_path(self):
        rinocloud.set_local_path(os.path.join(self.test_dir, "test_data/"), create_dir=True)
        self.assertEqual(os.path.exists(rinocloud.path), True)

    def test_set_domain(self):
        rinocloud.set_domain('localhost')
        self.assertEqual(rinocloud.api_domain, 'localhost')
        self.assertEqual(rinocloud.api_base, 'localhost/api/1/')
        self.assertEqual(rinocloud.urls["upload"], 'localhost/api/1/files/upload_multipart/')


class RinocloudObjectTest(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        rinocloud.set_local_path(os.path.join(self.test_dir, "test_data/"), create_dir=True)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_create_object_name(self):
        o = rinocloud.Object()
        o.set_name("file.txt")
        self.assertEqual(o.name, "file.txt")
        self.assertEqual(o.filepath, os.path.join(rinocloud.path, "file.txt"))

    def test_create_object_name_increment(self):
        o = rinocloud.Object()
        o.set_name("file.txt")

        with open(o.filepath, 'w') as outfile:
            outfile.write('test content')

        o2 = rinocloud.Object()
        o2.set_name("file.txt")

        self.assertEqual(o2.name, "file1.txt")
        self.assertEqual(o2.filepath, os.path.join(rinocloud.path, "file1.txt"))

    def test_create_object_hash(self):
        o = rinocloud.Object()
        o.set_name("file.txt")

        with open(o.filepath, 'w') as outfile:
            outfile.write('1\n2\n3\n4\n5')

        o.calculate_etag()

        self.assertEqual(o.etag, "fe743783afdf86af96aac1781ceff960-1")

    def test_create_object_name_overwrite(self):
        o = rinocloud.Object()
        o.set_name("file.txt")

        with open(o.filepath, 'w') as outfile:
            outfile.write('test content')

        o2 = rinocloud.Object()
        o2.set_name("file.txt", overwrite=True)

        self.assertEqual(o2.name, "file.txt")
        self.assertEqual(o2.filepath, os.path.join(rinocloud.path, "file.txt"))

    def test_sort(self):
        query = rinocloud.Query()
        query.sort('-f')
        self.assertEqual(query._sort, '-f')


class RinocloudCollectionTest(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        rinocloud.set_local_path(os.path.join(self.test_dir, "test_data/"), create_dir=True)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_create_collection_name(self):
        c = rinocloud.Collection()
        c.set_name("folder", create_dir=True)
        self.assertEqual(c.name, "folder")
        self.assertEqual(c.filepath, os.path.join(rinocloud.path, "folder"))

    def test_collection_children_name(self):
        c = rinocloud.Collection()
        c.set_name("folder", create_dir=True)

        o = rinocloud.Object()
        o.set_name("file.txt")

        self.assertEqual(o.name, "file.txt")
        self.assertEqual(o.filepath, os.path.join(rinocloud.path, "file.txt"))

        c.add(o)
        self.assertEqual(o.filepath, os.path.join(rinocloud.path, "folder/file.txt"))
