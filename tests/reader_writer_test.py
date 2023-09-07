import unittest
import os
from wadflow import WADFile, WriteableLump, write_lumps_to_pwad


class TestWriteableLumpAndWADWrite(unittest.TestCase):
    def setUp(self):
        self.lump_name = "TESTLUMP"
        self.lump_data = b"TEST DATA FOR LUMP"
        self.writable_lump = WriteableLump(self.lump_name, self.lump_data)

    def test_write_and_read(self):
        # Writing to a new WAD
        output_path = "output_test.wad"
        write_lumps_to_pwad([self.writable_lump], output_path)

        # Reading the written WAD
        new_wad = WADFile(output_path)
        read_data = new_wad.read_lump(self.lump_name)

        self.assertEqual(self.lump_data, read_data)

        # Cleanup
        os.remove(output_path)


if __name__ == "__main__":
    unittest.main()

