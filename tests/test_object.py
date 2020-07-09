# -*- coding: utf-8 -*-
"""Object tests."""
import fs
import fs.tempfs
import io
import json
import logging
import os
import sys
import tempfile
import unittest
from ocfl.object import Object, ObjectException
from ocfl.version import VersionMetadata


class TestAll(unittest.TestCase):
    """TestAll class to run tests."""

    if sys.version_info < (3, 2):
        def assertRegex(self, *args, **kwargs):
            """Hack for Python 2.7."""
            return self.assertRegexpMatches(*args, **kwargs)

    def test01_init(self):
        """Test Object init."""
        oo = Object()
        self.assertEqual(oo.id, None)
        self.assertEqual(oo.digest_algorithm, 'sha512')
        self.assertEqual(oo.skips, set())
        self.assertEqual(oo.ocfl_version, 'draft')
        self.assertEqual(oo.fixity, None)
        oo = Object(id='a:b', digest_algorithm='sha1', skips=['1', '2'],
                    ocfl_version='0.9.9', fixity=['md5', 'crc16'])
        self.assertEqual(oo.id, 'a:b')
        self.assertEqual(oo.digest_algorithm, 'sha1')
        self.assertEqual(oo.skips, set(('1', '2')))
        self.assertEqual(oo.ocfl_version, '0.9.9')
        self.assertEqual(oo.fixity, ['md5', 'crc16'])

    def test02_parse_version_directory(self):
        """Test parse_version_directory."""
        oo = Object()
        self.assertEqual(oo.parse_version_directory('v1'), 1)
        self.assertEqual(oo.parse_version_directory('v00001'), 1)
        self.assertEqual(oo.parse_version_directory('v99999'), 99999)
        # Bad
        self.assertRaises(Exception, oo.parse_version_directory, None)
        self.assertRaises(Exception, oo.parse_version_directory, '')
        self.assertRaises(Exception, oo.parse_version_directory, '1')
        self.assertRaises(Exception, oo.parse_version_directory, 'v0')
        self.assertRaises(Exception, oo.parse_version_directory, 'v-1')
        self.assertRaises(Exception, oo.parse_version_directory, 'v0000')
        self.assertRaises(Exception, oo.parse_version_directory, 'vv')
        self.assertRaises(Exception, oo.parse_version_directory, 'v000001')

    def test03_digest(self):
        """Test digest wrapper mathod."""
        oo = Object(digest_algorithm='md5')
        src_fs = fs.open_fs('tests/testdata')
        self.assertEqual(oo.digest(src_fs, 'files/empty'),
                         'd41d8cd98f00b204e9800998ecf8427e')
        self.assertEqual(oo.digest(src_fs, '/files/empty'),
                         'd41d8cd98f00b204e9800998ecf8427e')

    def test04_start_inventory(self):
        """Test start_inventory mehthod stub."""
        oo = Object(id="info:a", digest_algorithm="sha256")
        inventory = oo.start_inventory()
        self.assertEqual(inventory['id'], "info:a")
        self.assertEqual(inventory['digestAlgorithm'], "sha256")
        self.assertEqual(inventory['versions'], {})
        self.assertEqual(inventory['manifest'], {})
        self.assertNotIn('contentDirectory', inventory)
        self.assertNotIn('fixity', inventory)
        oo = Object(id="info:b", digest_algorithm="sha256",
                    fixity=['md5', 'sha1'])
        inventory = oo.start_inventory()
        self.assertEqual(inventory['fixity'], {'md5': {}, 'sha1': {}})
        #
        oo = Object(id="info:b", content_directory="stuff")
        inventory = oo.start_inventory()
        self.assertEqual(inventory['id'], "info:b")
        self.assertEqual(inventory['contentDirectory'], "stuff")
        self.assertEqual(inventory['digestAlgorithm'], "sha512")

    def test05_add_version(self):
        """Test add_version method."""
        self.maxDiff = None
        oo = Object(digest_algorithm="md5")
        inventory = {'manifest': {}, 'versions': {}}
        metadata = VersionMetadata()
        metadata.from_inventory_file('fixtures/1.0/content/spec-ex-full/v1_inventory.json', 'v1')
        src_fs = fs.open_fs('fixtures/1.0/content/spec-ex-full')
        oo.add_version(inventory, src_fs, src_dir='v1', vdir='v1', metadata=metadata)
        self.assertEqual(inventory['head'], 'v1')
        self.assertEqual(inventory['manifest'],
                         {'184f84e28cbe75e050e9c25ea7f2e939': ['v1/content/foo/bar.xml'],
                          'c289c8ccd4bab6e385f5afdd89b5bda2': ['v1/content/image.tiff'],
                          'd41d8cd98f00b204e9800998ecf8427e': ['v1/content/empty.txt']})
        self.assertEqual(inventory['versions'],
                         {"v1":
                          {'created': '2018-01-01T01:01:01Z',
                           'message': 'Initial import',
                           'state': {
                               '184f84e28cbe75e050e9c25ea7f2e939': ['foo/bar.xml'],
                               'c289c8ccd4bab6e385f5afdd89b5bda2': ['image.tiff'],
                               'd41d8cd98f00b204e9800998ecf8427e': ['empty.txt']},
                           'user': {'address': 'alice@example.com', 'name': 'Alice'}}})
        self.assertNotIn('fixity', inventory)
        # Now add second version to check forward delta
        metadata = VersionMetadata()
        metadata.from_inventory_file('fixtures/1.0/content/spec-ex-full/v2_inventory.json', 'v2')
        src_fs = fs.open_fs('fixtures/1.0/content/spec-ex-full/v2')
        oo.add_version(inventory, src_fs, src_dir='', vdir='v2', metadata=metadata)
        self.assertEqual(inventory['head'], 'v2')
        self.assertEqual(inventory['manifest'],
                         {'184f84e28cbe75e050e9c25ea7f2e939': ['v1/content/foo/bar.xml'],
                          '2673a7b11a70bc7ff960ad8127b4adeb': ['v2/content/foo/bar.xml'],
                          'c289c8ccd4bab6e385f5afdd89b5bda2': ['v1/content/image.tiff'],
                          'd41d8cd98f00b204e9800998ecf8427e': ['v1/content/empty.txt']})
        self.assertEqual(inventory['versions']['v2'],
                         {'created': '2018-02-02T02:02:02Z',
                          'message': 'Fix bar.xml, remove image.tiff, add empty2.txt',
                          'state': {
                              '2673a7b11a70bc7ff960ad8127b4adeb': ['foo/bar.xml'],
                              'd41d8cd98f00b204e9800998ecf8427e': ['empty.txt', 'empty2.txt']},
                          'user': {'address': 'bob@example.com', 'name': 'Bob'}})
        # Now with fixity
        oo = Object(digest_algorithm="md5", fixity=['sha1'])
        inventory = {'manifest': {}, 'versions': {}, 'fixity': {'sha1': {}}}
        md1 = VersionMetadata()
        md1.from_inventory_file('fixtures/1.0/content/spec-ex-full/v1_inventory.json', 'v1')
        src_fs = fs.open_fs('fixtures/1.0/content/spec-ex-full/v1')
        manifest_to_srcfile = oo.add_version(inventory, src_fs, src_dir='', vdir='v1', metadata=md1)
        self.assertEqual(manifest_to_srcfile, {
            'v1/content/image.tiff': 'image.tiff',
            'v1/content/empty.txt': 'empty.txt',
            'v1/content/foo/bar.xml': 'foo/bar.xml'
        })

    def test06_build_inventory(self):
        """Test build_inventory."""
        oo = Object(digest_algorithm="md5")
        src_fs = fs.open_fs('fixtures/1.0/content/spec-ex-full')
        for (vdir, inventory, manifest_to_srcfile) in oo.build_inventory(src_fs,
                                                                         metadata=VersionMetadata()):
            pass
        self.assertEqual(inventory['type'], 'https://ocfl.io/1.0/spec/#inventory')
        self.assertEqual(inventory['head'], 'v3')
        self.assertEqual(inventory['manifest'],
                         {'184f84e28cbe75e050e9c25ea7f2e939': ['v1/content/foo/bar.xml'],
                          '2673a7b11a70bc7ff960ad8127b4adeb': ['v2/content/foo/bar.xml'],
                          'c289c8ccd4bab6e385f5afdd89b5bda2': ['v1/content/image.tiff'],
                          'd41d8cd98f00b204e9800998ecf8427e': ['v1/content/empty.txt']})
        self.assertEqual(len(inventory['versions']), 3)
        # test skips by skipping 'v3'
        oo = Object(digest_algorithm="md5", skips=['v3'])
        src_fs = fs.open_fs('fixtures/1.0/content/spec-ex-full')
        for (vdir, inventory, manifest_to_srcfile) in oo.build_inventory(src_fs,
                                                                         metadata=VersionMetadata()):
            if vdir == 'v1':
                self.assertEqual(manifest_to_srcfile, {
                    'v1/content/image.tiff': 'v1/image.tiff',
                    'v1/content/empty.txt': 'v1/empty.txt',
                    'v1/content/foo/bar.xml': 'v1/foo/bar.xml'
                })
            else:
                self.assertEqual(manifest_to_srcfile, {
                    'v2/content/foo/bar.xml': 'v2/foo/bar.xml'
                })
        self.assertEqual(inventory['head'], 'v2')
        self.assertEqual(len(inventory['versions']), 2)

    def test07_write_object_declaration(self):
        """Test write_object_declaration."""
        tmpfs = fs.tempfs.TempFS(identifier='test_write_object_declaration')
        oo = Object(obj_fs=tmpfs)
        oo.write_object_declaration()
        self.assertEqual(tmpfs.listdir('/'), ['0=ocfl_object_1.0'])

    def test08_write_inventory_and_sidecar(self):
        """Test write_object_and_sidecar."""
        tmpfs = fs.tempfs.TempFS(identifier='test_write_inventory_and_sidecar')
        oo = Object(obj_fs=tmpfs)
        oo.write_inventory_and_sidecar({'abc': 'def'})
        self.assertEqual(set(tmpfs.listdir('')),
                         set(['inventory.json', 'inventory.json.sha512']))
        with tmpfs.open('inventory.json') as fh:
            j = json.load(fh)
        self.assertEqual(j, {'abc': 'def'})
        digest = tmpfs.readtext('inventory.json.sha512')
        self.assertRegex(digest, r'''[0-9a-f]{128} inventory.json\n''')
        # and now making directory
        oo = Object(obj_fs=tmpfs)
        invdir = 'xxx'
        oo.write_inventory_and_sidecar({'gh': 'ik'}, invdir)
        self.assertEqual(set(tmpfs.listdir(invdir)),
                         set(['inventory.json', 'inventory.json.sha512']))
        with tmpfs.open(fs.path.join(invdir, 'inventory.json')) as fh:
            j = json.load(fh)
        self.assertEqual(j, {'gh': 'ik'})

    def test09_build(self):
        """Test write method."""
        tempdir = tempfile.mkdtemp(prefix='test_write')
        oo = Object()
        self.assertRaises(ObjectException, oo.build, srcdir='fixtures/1.0/content/spec-ex-full')
        oo.id = 'uri:firkin'
        objdir = os.path.join(tempdir, '1')
        oo.build(srcdir='fixtures/1.0/content/spec-ex-full',
                 metadata=VersionMetadata(),
                 objdir=objdir)
        self.assertEqual(set(os.listdir(objdir)),
                         set(['0=ocfl_object_1.0',
                              'inventory.json', 'inventory.json.sha512',
                              'v1', 'v2', 'v3']))
        # FIXME - extra tests for outputs created and special cases

    def test10_create(self):
        """Test create method."""
        tempdir = tempfile.mkdtemp(prefix='test_create')
        oo = Object()
        self.assertRaises(ObjectException, oo.create, srcdir='fixtures/1.0/content/spec-ex-full/v1')
        oo.id = 'uri:kliderkin'
        objdir = os.path.join(tempdir, '1')
        oo.create(srcdir='fixtures/1.0/content/spec-ex-full/v1',
                  metadata=VersionMetadata(),
                  objdir=objdir)
        self.assertEqual(set(os.listdir(objdir)),
                         set(['0=ocfl_object_1.0',
                              'inventory.json', 'inventory.json.sha512',
                              'v1']))

    def test11_update(self):
        """Test update method."""
        tempdir = tempfile.mkdtemp(prefix='test_update')
        oo = Object()
        # First create and object
        oo.id = 'uri:wumpus'
        objdir = os.path.join(tempdir, '1')
        oo.digest_algorithm = 'sha256'
        oo.create(srcdir='fixtures/1.0/content/spec-ex-minimal/v1',
                  metadata=VersionMetadata(),
                  objdir=objdir)
        self.assertEqual(set(os.listdir(objdir)),
                         set(['0=ocfl_object_1.0',
                              'inventory.json', 'inventory.json.sha256',
                              'v1']))
        # Now update
        oo.digest_algorithm = 'sha512'
        oo.update(objdir=objdir,
                  metadata=VersionMetadata())
        self.assertEqual(set(os.listdir(objdir)),
                         set(['0=ocfl_object_1.0',
                              'inventory.json', 'inventory.json.sha512',
                              'v1', 'v2']))

    def test12_show(self):
        """Test show method."""
        s = io.StringIO()
        oo = Object()
        oo.log.addHandler(logging.StreamHandler(s))
        oo.show(objdir='fixtures/1.0/good-objects/minimal_one_version_one_file')
        out = s.getvalue()
        self.assertIn('[fixtures/1.0/good-objects/minimal_one_version_one_file]', out)
        self.assertTrue('├── 0=ocfl_object_1.0' in out)
        # FIXME - need real tests in here when there is real output

    def test13_validate(self):
        """Test validate method."""
        oo = Object()
        self.assertTrue(oo.validate(objdir='fixtures/1.0/good-objects/minimal_one_version_one_file'))
        # Error cases
        self.assertFalse(oo.validate(objdir='fixtures/1.0/bad-objects/E001_E004_no_files'))
        self.assertFalse(oo.validate(objdir='fixtures/1.0/bad-objects/E001_no_decl'))
        self.assertFalse(oo.validate(objdir='fixtures/1.0/bad-objects/E036_no_id'))

    def test14_parse_inventory(self):
        """Test parse_inventory method."""
        oo = Object()
        self.assertTrue(oo.parse_inventory(path='fixtures/1.0/good-objects/minimal_one_version_one_file'))
        # Error cases
        self.assertRaises(ObjectException, oo.parse_inventory, path='fixtures/1.0/bad-objects/E036_no_id')

    def test15_map_filepath(self):
        """Test map_filepath method."""
        oo = Object()
        # default is uri
        self.assertEqual(oo.map_filepath('a', 'v1', {}), 'v1/content/a')
        self.assertEqual(oo.map_filepath('.a?', 'v1', {}), 'v1/content/%2Ea%3F')
        self.assertEqual(oo.map_filepath('a', 'v1', {'v1/content/a': True}), 'v1/content/a__2')
        # md5
        oo = Object()
        oo.filepath_normalization = 'md5'
        self.assertEqual(oo.map_filepath('a', 'v1', {}), 'v1/content/0cc175b9c0f1b6a8')
        self.assertEqual(oo.map_filepath('a', 'v1', {'v1/content/0cc175b9c0f1b6a8': True}), 'v1/content/0cc175b9c0f1b6a8__2')
        # error case
        oo = Object()
        oo.filepath_normalization = '???'
        self.assertRaises(Exception, oo.map_filepath, 'a', 'v1', {})

    def test16_extract(self):
        """Test extract method."""
        tempdir = tempfile.mkdtemp(prefix='test_extract')
        oo = Object()
        dstdir = os.path.join(tempdir, 'vvv1')
        oo.extract('fixtures/1.0/good-objects/minimal_one_version_one_file', 'v1', dstdir)
        self.assertEqual(os.listdir(tempdir), ['vvv1'])
        self.assertEqual(os.listdir(dstdir), ['a_file.txt'])
