import struct
from typing import List


class WriteableLump:
    """
    A class to represent a lump that can be written to a WAD file.

    Attributes:
        name (str): The name of the lump, should be no longer than 8 characters.
        data (bytes): The binary data of the lump.

    Methods:
        get_size: Return the size of the lump data in bytes.
        get_data: Return the binary data of the lump.
    """

    def __init__(self, name: str, data: bytes) -> None:
        """
        Initialize a WriteableLump instance.

        Args:
            name (str): The name of the lump, should be no longer than 8 characters.
            data (bytes): The binary data of the lump.
        """
        self.name = name
        self.data = data

    def get_size(self) -> int:
        """
        Get the size of the lump data in bytes.

        Returns:
            int: Size of the lump data.
        """
        return len(self.data)

    def get_data(self) -> bytes:
        """
        Get the binary data of the lump.

        Returns:
            bytes: The binary data of the lump.
        """
        return self.data


def write_lumps_to_pwad(lumps: List[WriteableLump], wad_filepath: str) -> None:
    """
    Write a list of lumps to a new WAD file.

    Args:
        lumps (List[WriteableLump]): List of lumps to write to the WAD file.
        wad_filepath (str): Path to the WAD file to create or overwrite.

    Raises:
        ValueError: If a lump name is longer than 8 characters.
    """
    # Create/open the PWAD file in binary write mode
    with open(wad_filepath, 'wb') as wad_file:
        # Write PWAD header
        wad_file.write(b'PWAD')

        # Lump count
        lump_count = len(lumps)
        wad_file.write(struct.pack('<I', lump_count))

        # Calculate the offset to the directory
        # It's after the header and all lump data
        lump_data_start = 12  # start after the WAD header
        lump_directory_offset = lump_data_start + sum(lump.get_size() for lump in lumps)
        wad_file.write(struct.pack('<I', lump_directory_offset))

        # Write lump data for each lump
        for lump in lumps:
            if len(lump.name) > 8:
                raise ValueError(f"Lump name '{lump.name}' is too long. Maximum allowed is 8 characters.")
            wad_file.write(lump.get_data())

        # Write lump directory for each lump
        current_offset = lump_data_start
        for lump in lumps:
            wad_file.write(struct.pack('<I', current_offset))
            wad_file.write(struct.pack('<I', lump.get_size()))
            wad_file.write(lump.name.encode('ascii').ljust(8, b'\x00'))  # Name, padded to 8 bytes
            current_offset += lump.get_size()
