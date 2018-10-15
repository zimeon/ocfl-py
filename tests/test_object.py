# -*- coding: utf-8 -*-
"""Digest tests."""
import io
import json
import os
import sys
import tempfile
import unittest
from ocfl.object import Object, ObjectException, remove_first_directory
from ocfl.version import VersionMetadata


class TestAll(unittest.TestCase):
    """TestAll class to run tests."""

    def test01_init(self):
        """Test Object init."""
        oo = Object()
        self.assertEqual(oo.identifier, None)
        self.assertEqual(oo.digest_algorithm, 'sha512')
        self.assertEqual(oo.skips, set())
        self.assertEqual(oo.ocfl_version, 'draft')
        self.assertEqual(oo.fixity, None)
        oo = Object(identifier='a:b', digest_algorithm='sha1', skips=['1', '2'],
                    ocfl_version='0.9.9', fixity=['md5', 'crc16'])
        self.assertEqual(oo.identifier, 'a:b')
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
        self.assertEqual(oo.digest('tests/testdata/files/empty'),
                         'd41d8cd98f00b204e9800998ecf8427e')

    def test04_start_inventory(self):
        """Test start_inventory mehthod stub."""
        oo = Object(identifier="info:a", digest_algorithm="sha256")
        inventory = oo.start_inventory()
        self.assertEqual(inventory['id'], "info:a")
        self.assertEqual(inventory['digestAlgorithm'], "sha256")
        self.assertEqual(inventory['versions'], [])
        self.assertEqual(inventory['manifest'], {})
        self.assertNotIn('fixity', inventory)
        oo = Object(identifier="info:b", digest_algorithm="sha256",
                    fixity=['md5', 'sha1'])
        inventory = oo.start_inventory()
        self.assertEqual(inventory['fixity'], {'md5': {}, 'sha1': {}})

    def test05_add_version(self):
        """Test add_version method."""
        oo = Object(digest_algorithm="md5")
        inventory = {'manifest': {}, 'versions': []}
        oo.add_version(inventory, 'fixtures/content/spec-ex-full/v1', vdir='v1',
                       metadata=VersionMetadata())
        self.assertEqual(inventory['head'], 'v1')
        self.assertEqual(inventory['manifest'],
                         {'184f84e28cbe75e050e9c25ea7f2e939': ['v1/foo/bar.xml'],
                          'c289c8ccd4bab6e385f5afdd89b5bda2': ['v1/image.tiff'],
                          'd41d8cd98f00b204e9800998ecf8427e': ['v1/empty.txt']})
        self.assertEqual(inventory['versions'],
                         [{'created': '2018-01-01T01:01:01Z',
                           'message': 'Initial import',
                           'state': {
                               '184f84e28cbe75e050e9c25ea7f2e939': ['foo/bar.xml'],
                               'c289c8ccd4bab6e385f5afdd89b5bda2': ['image.tiff'],
                               'd41d8cd98f00b204e9800998ecf8427e': ['empty.txt']},
                             'type': 'Version',
                             'user': {'address': 'alice@example.com', 'name': 'Alice'},
                             'version': 'v1'}])
        self.assertNotIn('fixity', inventory)
        # Now add second version to check forward delta
        oo.add_version(inventory, 'fixtures/content/spec-ex-full/v2', vdir='v2',
                       metadata=VersionMetadata())
        self.assertEqual(inventory['head'], 'v2')
        self.assertEqual(inventory['manifest'],
                         {'184f84e28cbe75e050e9c25ea7f2e939': ['v1/foo/bar.xml'],
                          '2673a7b11a70bc7ff960ad8127b4adeb': ['v2/foo/bar.xml'],
                          'c289c8ccd4bab6e385f5afdd89b5bda2': ['v1/image.tiff'],
                          'd41d8cd98f00b204e9800998ecf8427e': ['v1/empty.txt']})
        self.assertEqual(inventory['versions'][1],
                         {'created': '2018-02-02T02:02:02Z',
                          'message': 'Fix bar.xml, remove image.tiff, add empty2.txt',
                          'state': {
                              '2673a7b11a70bc7ff960ad8127b4adeb': ['foo/bar.xml'],
                              'd41d8cd98f00b204e9800998ecf8427e': ['empty.txt', 'empty2.txt']},
                          'type': 'Version',
                          'user': {'address': 'bob@example.com', 'name': 'Bob'},
                          'version': 'v2'})
        # Now with fixity
        oo = Object(digest_algorithm="md5", fixity=['sha1'])
        inventory = {'manifest': {}, 'versions': [], 'fixity': {'sha1': {}}}
        oo.add_version(inventory, 'fixtures/content/spec-ex-full/v1', vdir='v1',
                       metadata=VersionMetadata())

    def test06_build_inventory(self):
        """Test build_inventory."""
        oo = Object(digest_algorithm="md5")
        for (vdir, inventory) in oo.build_inventory('fixtures/content/spec-ex-full',
                                                    metadata=VersionMetadata()):
            pass
        self.assertEqual(inventory['type'], 'Object')
        self.assertEqual(inventory['head'], 'v3')
        self.assertEqual(inventory['manifest'],
                         {'184f84e28cbe75e050e9c25ea7f2e939': ['v1/foo/bar.xml'],
                          '2673a7b11a70bc7ff960ad8127b4adeb': ['v2/foo/bar.xml'],
                         'c289c8ccd4bab6e385f5afdd89b5bda2': ['v1/image.tiff'],
                          'd41d8cd98f00b204e9800998ecf8427e': ['v1/empty.txt']})
        self.assertEqual(len(inventory['versions']), 3)
        # test skips by skipping 'v3'
        oo = Object(digest_algorithm="md5", skips=['v3'])
        for (vdir, inventory) in oo.build_inventory('fixtures/content/spec-ex-full',
                                                    metadata=VersionMetadata()):
            pass
        self.assertEqual(inventory['head'], 'v2')
        self.assertEqual(len(inventory['versions']), 2)

    def test07_write_object_declaration(self):
        """Test write_object_declaration."""
        tempdir = tempfile.mkdtemp(prefix='test_write_object_declaration')
        oo = Object()
        oo.write_object_declaration(tempdir)
        self.assertEqual(os.listdir(tempdir), ['0=ocfl_object_1.0'])

    def test08_write_inventory_and_sidecar(self):
        """Test write_object_and_sidecar."""
        tempdir = tempfile.mkdtemp(prefix='test_write_inventory_and_sidecar')
        oo = Object()
        oo.write_inventory_and_sidecar(tempdir, {'abc': 'def'})
        self.assertEqual(set(os.listdir(tempdir)),
                         set(['inventory.json', 'inventory.json.sha512']))
        with open(os.path.join(tempdir, 'inventory.json')) as fh:
            j = json.load(fh)
        self.assertEqual(j, {'abc': 'def'})
        with open(os.path.join(tempdir, 'inventory.json.sha512')) as fh:
            digest = fh.read()
        self.assertRegexpMatches(digest, r'''[0-9a-f]{128} inventory.json\n''')
        # and now makind directory
        oo = Object()
        invdir = os.path.join(tempdir, 'xxx')
        oo.write_inventory_and_sidecar(invdir, {'gh': 'ik'})
        self.assertEqual(set(os.listdir(invdir)),
                         set(['inventory.json', 'inventory.json.sha512']))
        with open(os.path.join(invdir, 'inventory.json')) as fh:
            j = json.load(fh)
        self.assertEqual(j, {'gh': 'ik'})

    def test09_write(self):
        """Test write method."""
        tempdir = tempfile.mkdtemp(prefix='test_write')
        oo = Object()
        self.assertRaises(ObjectException, oo.write, srcdir='fixtures/content/spec-ex-full')
        oo.identifier = 'uri:firkin'
        objdir = os.path.join(tempdir, '1')
        oo.write(srcdir='fixtures/content/spec-ex-full',
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
        self.assertRaises(ObjectException, oo.create, srcdir='fixtures/content/spec-ex-full/v1')
        oo.identifier = 'uri:kliderkin'
        objdir = os.path.join(tempdir, '1')
        oo.create(srcdir='fixtures/content/spec-ex-full/v1',
                  metadata=VersionMetadata(),
                  objdir=objdir)
        self.assertEqual(set(os.listdir(objdir)),
                         set(['0=ocfl_object_1.0',
                              'inventory.json', 'inventory.json.sha512',
                              'v1']))

    def test11_show(self):
        """Test show method."""
        s = io.StringIO()
        oo = Object(fhout=s)
        oo.show(path='fixtures/objects/of1')
        out = s.getvalue()
        if sys.version_info < (3, 0):
            out = out.encode('utf8')
        self.assertTrue(out.startswith('[fixtures/objects/of1]'))
        self.assertTrue('├── 0=ocfl_object_1.0' in out)
        # FIXME - need real tests in here when there is real output

    def test12_validate(self):
        """Test validate method."""
        oo = Object()
        self.assertTrue(oo.validate(path='fixtures/objects/of1'))
        # Error cases
        self.assertFalse(oo.validate(path='fixtures/bad-objects/bad00_no_files'))
        self.assertFalse(oo.validate(path='fixtures/bad-objects/bad01_no_decl'))
        self.assertFalse(oo.validate(path='fixtures/bad-objects/bad02_no_id'))

    def test13_parse_inventory(self):
        """Test parse_inventory method."""
        oo = Object()
        self.assertTrue(oo.parse_inventory(path='fixtures/objects/of1'))
        # Error cases
        self.assertRaises(ObjectException, oo.parse_inventory, path='fixtures/bad-objects/bad02_no_id')

    def test90_remove_first_directory(self):
        """Test encode."""
        self.assertEqual(remove_first_directory(''), '')
        self.assertEqual(remove_first_directory('a'), '')
        self.assertEqual(remove_first_directory('a/b'), 'b')
        self.assertEqual(remove_first_directory('a/b/'), 'b')
        self.assertEqual(remove_first_directory('a/b/c'), 'b/c')
