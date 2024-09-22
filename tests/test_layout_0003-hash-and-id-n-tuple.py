"""0003: Hashed Truncated N-tuple Trees with Object ID layout tests."""
import unittest
from ocfl.layout_0003_hash_and_id_n_tuple import Layout_0003_Hash_And_Id_N_Tuple, _percent_encode, _id_to_path


class TestAll(unittest.TestCase):
    """TestAll class to run tests."""

    def test__percent_encode(self):
        """Test _percent_encode function."""
        self.assertEqual(_percent_encode('.'), '%2e')
        self.assertEqual(_percent_encode('ç'), '%c3%a7')

    def test__id_to_path(self):
        """Test _id_to_path function."""
        self.assertEqual(_id_to_path(identifier='object-01', digest_algorithm='sha256', tuple_size=3, number_of_tuples=3),
                         '3c0/ff4/240/object-01')
        self.assertEqual(_id_to_path(identifier='object-01', digest_algorithm='md5', tuple_size=3, number_of_tuples=3),
                         'ff7/553/449/object-01')
        self.assertEqual(_id_to_path(identifier='object-01', digest_algorithm='md5', tuple_size=5, number_of_tuples=2),
                         'ff755/34492/object-01')
        self.assertEqual(_id_to_path(identifier='object-01', digest_algorithm='md5', tuple_size=0, number_of_tuples=0),
                         'object-01')
        self.assertEqual(_id_to_path(identifier='object-01', digest_algorithm='md5', tuple_size=2, number_of_tuples=15),
                         'ff/75/53/44/92/48/5e/ab/b3/9f/86/35/67/28/88/object-01')
        self.assertEqual(_id_to_path(identifier='..hor/rib:le-$id', digest_algorithm='sha256', tuple_size=3, number_of_tuples=3),
                         '487/326/d8c/%2e%2ehor%2frib%3ale-%24id')
        self.assertEqual(_id_to_path(identifier='..hor/rib:le-$id', digest_algorithm='md5', tuple_size=3, number_of_tuples=3),
                         '083/197/66f/%2e%2ehor%2frib%3ale-%24id') #08319766fb6c2935dd175b94267717e0
        self.assertEqual(_id_to_path(identifier='..Hor/rib:lè-$id', digest_algorithm='sha256', tuple_size=3, number_of_tuples=3),
                         '373/529/21a/%2e%2eHor%2frib%3al%c3%a8-%24id')
        long_object_id = 'abcdefghij' * 26
        long_object_id_digest = '55b432806f4e270da0cf23815ed338742179002153cd8d896f23b3e2d8a14359'
        self.assertEqual(_id_to_path(identifier=long_object_id, digest_algorithm='sha256', tuple_size=3, number_of_tuples=3),
                         f'55b/432/806/abcdefghijabcdefghijabcdefghijabcdefghijabcdefghijabcdefghijabcdefghijabcdefghijabcdefghijabcdefghij-{long_object_id_digest}')
        long_object_id_101 = 'abcdefghij' * 10 + 'a'
        long_object_id_101_digest = '5cc73e648fbcff136510e330871180922ddacf193b68fdeff855683a01464220'
        self.assertEqual(_id_to_path(identifier=long_object_id_101, digest_algorithm='sha256', tuple_size=3, number_of_tuples=3),
                         f'5cc/73e/648/abcdefghijabcdefghijabcdefghijabcdefghijabcdefghijabcdefghijabcdefghijabcdefghijabcdefghijabcdefghij-{long_object_id_101_digest}')

    def test_name(self):
        """Test canonical name."""
        self.assertEqual(Layout_0003_Hash_And_Id_N_Tuple().name, '0003-hash-and-id-n-tuple-storage-layout')

    def test_identifier_to_path(self):
        """Test identifier_to_path."""
        d = Layout_0003_Hash_And_Id_N_Tuple()
        # From the extension
        self.assertEqual(d.identifier_to_path('object-01'), '3c0/ff4/240/object-01')
        self.assertEqual(d.identifier_to_path('..hor/rib:le-$id'), '487/326/d8c/%2e%2ehor%2frib%3ale-%24id')
