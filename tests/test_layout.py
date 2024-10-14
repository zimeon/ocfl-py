"""Digest tests."""
import unittest
import unittest.mock
from ocfl.layout import Layout, LayoutException
from ocfl.pyfs import open_fs


class TestAll(unittest.TestCase):
    """TestAll class to run tests."""

    def test_init_and_config(self):
        """Test almost everything, just a little."""
        layout = Layout()
        self.assertEqual(type(layout), Layout)
        self.assertEqual(layout.config_file, "extensions/BASE/config.json")
        self.assertEqual(layout.config, None)

    def test_strip_root(self):
        """Test strip_root."""
        layout = Layout()
        self.assertEqual(layout.strip_root('a/b', 'a'), 'b')
        self.assertEqual(layout.strip_root('a/b', ''), 'a/b')
        self.assertEqual(layout.strip_root('a/b/c', 'a/b/c'), '.')
        self.assertEqual(layout.strip_root('a/b/c', 'a/b/'), 'c')
        self.assertEqual(layout.strip_root('a/b/c/', 'a/b'), 'c')
        self.assertRaises(LayoutException, layout.strip_root, 'a', 'b')
        self.assertRaises(LayoutException, layout.strip_root, 'a', 'a/b')
        self.assertRaises(LayoutException, layout.strip_root, '', 'a/b')

    def test_is_valid(self):
        """Test is_valid method."""
        layout = Layout()
        self.assertTrue(layout.is_valid(''))
        self.assertTrue(layout.is_valid('anything'))

    def test_encodea_and_decode(self):
        """Test encode and decode methods."""
        layout = Layout()
        self.assertEqual(layout.encode(''), '')
        self.assertEqual(layout.encode('something'), 'something')
        self.assertEqual(layout.encode('http://a.b.c'), 'http%3A%2F%2Fa.b.c')
        self.assertEqual(layout.decode(''), '')
        self.assertEqual(layout.decode('something-else'), 'something-else')
        self.assertEqual(layout.decode('http%3a%2f%2Fa.b.c'), 'http://a.b.c')
        self.assertRaises(LayoutException, layout.identifier_to_path, 'id')

    def test_read_layout_params(self):
        """Test read_layout_params."""
        root_fs = open_fs("extra_fixtures/extension_configs")
        layout = Layout()
        layout.NAME = "good_param"
        layout.param = None

        def parse_param(value):
            layout.param = value
        layout.PARAMS = {"param": parse_param}
        layout.read_layout_params(root_fs=root_fs, params_required=True)
        self.assertEqual(layout.param, "yay!")
        # No config file but none required
        # Idoesn't do anything, nothing to check)
        layout.NAME = "no_config"
        layout.read_layout_params(root_fs=root_fs, params_required=False)
        # Error cases
        # No config file
        layout.NAME = "no_config"
        self.assertRaises(LayoutException, layout.read_layout_params, root_fs=root_fs, params_required=True)
        layout.NAME = "not_json"
        self.assertRaises(LayoutException, layout.read_layout_params, root_fs=root_fs)
        layout.NAME = "not_json_object"
        self.assertRaises(LayoutException, layout.read_layout_params, root_fs=root_fs)

    def test_check_and_set_layout_params(self):
        """Test check_and_set_layout_params."""
        layout = Layout()
        layout.NAME = "mylayout"
        layout.param = None

        def parse_param(value):
            layout.param = value
        layout.PARAMS = {"param": parse_param}
        self.assertRaises(LayoutException,
                          layout.check_and_set_layout_params, config={})
        self.assertRaises(LayoutException,
                          layout.check_and_set_layout_params,
                          config={"extensionName": "wrong-name"})
        # Good case
        layout.check_and_set_layout_params(
            config={"extensionName": "mylayout",
                    "param": "42",
                    "extraParam": "whatever"})
        self.assertEqual(layout.param, "42")

    def test_write_layout_params(self):
        """Test write_layout_params."""
        root_fs = open_fs("mem://")
        layout = Layout()
        # No config_file will return none, so simply exits
        self.assertEqual(layout.write_layout_params(root_fs=root_fs), None)
        # File exists
        layout.NAME = "a_name"
        with unittest.mock.patch("ocfl.layout.Layout.config", new_callable=unittest.mock.PropertyMock) as mock_config:
            mock_config.return_value = {"hello": "you"}
            # First write works....
            layout.write_layout_params(root_fs=root_fs)
            # Second hits file exists
            self.assertRaises(LayoutException, layout.write_layout_params,
                              root_fs=root_fs)
            # Change name, make bad JSON causing write exception
            layout.NAME = "new_name"
            mock_config.return_value = {unittest: "key in json.dump must not be module name!"}
            self.assertRaises(LayoutException, layout.write_layout_params,
                              root_fs=root_fs)
