"""0003: Hashed Truncated N-tuple Trees with Object ID layout tests."""
import unittest
from ocfl.layout import LayoutException
from ocfl.layout_0003_hash_and_id_n_tuple import Layout_0003_Hash_And_Id_N_Tuple, _percent_encode, _id_to_path


class TestAll(unittest.TestCase):
    """TestAll class to run tests."""

    def test__percent_encode(self):
        """Test _percent_encode function."""
        self.assertEqual(_percent_encode("."), "%2e")
        self.assertEqual(_percent_encode("ç"), "%c3%a7")

    def test__id_to_path(self):
        """Test _id_to_path function."""
        self.assertEqual(_id_to_path(identifier="object-01", digest_algorithm="sha256", tuple_size=3, number_of_tuples=3),
                         "3c0/ff4/240/object-01")
        self.assertEqual(_id_to_path(identifier="object-01", digest_algorithm="md5", tuple_size=3, number_of_tuples=3),
                         "ff7/553/449/object-01")
        self.assertEqual(_id_to_path(identifier="object-01", digest_algorithm="md5", tuple_size=5, number_of_tuples=2),
                         "ff755/34492/object-01")
        self.assertEqual(_id_to_path(identifier="object-01", digest_algorithm="md5", tuple_size=0, number_of_tuples=0),
                         "object-01")
        self.assertEqual(_id_to_path(identifier="object-01", digest_algorithm="md5", tuple_size=2, number_of_tuples=15),
                         "ff/75/53/44/92/48/5e/ab/b3/9f/86/35/67/28/88/object-01")
        self.assertEqual(_id_to_path(identifier="..hor/rib:le-$id", digest_algorithm="sha256", tuple_size=3, number_of_tuples=3),
                         "487/326/d8c/%2e%2ehor%2frib%3ale-%24id")
        self.assertEqual(_id_to_path(identifier="..hor/rib:le-$id", digest_algorithm="md5", tuple_size=3, number_of_tuples=3),
                         "083/197/66f/%2e%2ehor%2frib%3ale-%24id")  # digest: 08319766fb6c2935dd175b94267717e0
        self.assertEqual(_id_to_path(identifier="..Hor/rib:lè-$id", digest_algorithm="sha256", tuple_size=3, number_of_tuples=3),
                         "373/529/21a/%2e%2eHor%2frib%3al%c3%a8-%24id")
        long_object_id = "abcdefghij" * 26
        long_object_id_digest = "55b432806f4e270da0cf23815ed338742179002153cd8d896f23b3e2d8a14359"
        self.assertEqual(_id_to_path(identifier=long_object_id, digest_algorithm="sha256", tuple_size=3, number_of_tuples=3),
                         f"55b/432/806/abcdefghijabcdefghijabcdefghijabcdefghijabcdefghijabcdefghijabcdefghijabcdefghijabcdefghijabcdefghij-{long_object_id_digest}")
        long_object_id_101 = "abcdefghij" * 10 + "a"
        long_object_id_101_digest = "5cc73e648fbcff136510e330871180922ddacf193b68fdeff855683a01464220"
        self.assertEqual(_id_to_path(identifier=long_object_id_101, digest_algorithm="sha256", tuple_size=3, number_of_tuples=3),
                         f"5cc/73e/648/abcdefghijabcdefghijabcdefghijabcdefghijabcdefghijabcdefghijabcdefghijabcdefghijabcdefghijabcdefghij-{long_object_id_101_digest}")

    def test_check_digest_algorithm(self):
        """Test check_digest_algorithm method."""
        layout = Layout_0003_Hash_And_Id_N_Tuple()
        self.assertRaises(LayoutException, layout.check_digest_algorithm, None)
        self.assertRaises(LayoutException, layout.check_digest_algorithm, "no-a-digest-algorithm")
        self.assertRaises(LayoutException, layout.check_digest_algorithm, "")  # stil not!
        self.assertEqual(layout.check_digest_algorithm("md5"), None)
        self.assertEqual(layout.digest_algorithm, "md5")

    def test_check_tuple_size(self):
        """Test check_tuple_size method."""
        layout = Layout_0003_Hash_And_Id_N_Tuple()
        self.assertRaises(LayoutException, layout.check_tuple_size, None)
        self.assertRaises(LayoutException, layout.check_tuple_size, "string-not-num")
        self.assertRaises(LayoutException, layout.check_tuple_size, -1)
        self.assertRaises(LayoutException, layout.check_tuple_size, 33)
        self.assertEqual(layout.check_tuple_size(0), None)
        self.assertEqual(layout.tuple_size, 0)
        self.assertEqual(layout.check_tuple_size(32), None)
        self.assertEqual(layout.tuple_size, 32)

    def test_check_number_of_tuples(self):
        """Test check_number_of_tuples method."""
        layout = Layout_0003_Hash_And_Id_N_Tuple()
        self.assertRaises(LayoutException, layout.check_number_of_tuples, None)
        self.assertRaises(LayoutException, layout.check_number_of_tuples, "string-not-num")
        self.assertRaises(LayoutException, layout.check_number_of_tuples, -1)
        self.assertRaises(LayoutException, layout.check_number_of_tuples, 33)
        self.assertEqual(layout.check_number_of_tuples(0), None)
        self.assertEqual(layout.number_of_tuples, 0)
        self.assertEqual(layout.check_number_of_tuples(32), None)
        self.assertEqual(layout.number_of_tuples, 32)

    def test_check_full_config(self):
        """Test check_full_config method."""
        layout = Layout_0003_Hash_And_Id_N_Tuple()
        layout.check_and_set_layout_params(config={"digestAlgorithm": "md5",
                                                   "tupleSize": 0,
                                                   "numberOfTuples": 0},
                                           require_extension_name=False)
        self.assertRaises(LayoutException,
                          layout.check_and_set_layout_params,
                          config={"digestAlgorithm": "md5",
                                                     "tupleSize": 3,
                                                     "numberOfTuples": 0},
                          require_extension_name=False)
        # An md5 digest is 32 hex digits long
        layout.check_and_set_layout_params(config={"digestAlgorithm": "md5",
                                                   "tupleSize": 4,
                                                   "numberOfTuples": 8},
                                           require_extension_name=False)
        self.assertRaises(LayoutException,
                          layout.check_and_set_layout_params,
                          config={"digestAlgorithm": "md5",
                                                     "tupleSize": 4,
                                                     "numberOfTuples": 9},
                          require_extension_name=False)


    def test_config(self):
        """Test config property."""
        layout = Layout_0003_Hash_And_Id_N_Tuple()
        self.assertIn("extensionName", layout.config)
        self.assertIn("tupleSize", layout.config)

    def test_name(self):
        """Test canonical name."""
        self.assertEqual(Layout_0003_Hash_And_Id_N_Tuple().NAME, "0003-hash-and-id-n-tuple-storage-layout")

    def test_identifier_to_path(self):
        """Test identifier_to_path."""
        d = Layout_0003_Hash_And_Id_N_Tuple()
        # From the extension
        self.assertEqual(d.identifier_to_path("object-01"), "3c0/ff4/240/object-01")
        self.assertEqual(d.identifier_to_path("..hor/rib:le-$id"), "487/326/d8c/%2e%2ehor%2frib%3ale-%24id")
