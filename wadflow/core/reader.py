import struct
from typing import List, Tuple, Optional


def check_header(wad_file):
    """
    Check the WAD file header.

    Args:
        wad_file (file): The WAD file to check.

    Raises:
        InvalidWADFile: If the provided file is not a valid WAD file.
    """
    wad_type = wad_file.read(4)
    if wad_type not in [b'IWAD', b'PWAD']:
        raise InvalidWADFile(f"'{wad_file.name}' is not a valid WAD file. Found type: {wad_type.decode('ascii')}")


class InvalidWADFile(Exception):
    """
    Custom exception to represent an invalid WAD file.
    """
    pass


class WADFile:
    """
    A class to represent and interact with Doom WAD files.

    Attributes:
        file_path (str): The path to the WAD file.

    Methods:
        read_lump: Return the data for the specified lump.
        list_lump_names: Return a list of all lump names in the WAD file.
    """

    def __init__(self, file_path: str) -> None:
        """
        Initialize a WADFile instance.

        Args:
            file_path (str): The path to the WAD file.

        Raises:
            InvalidWADFile: If the provided file is not a valid WAD file.
        """
        self.file_path = file_path
        self._lumps = None

        # Only check the header on initialization
        with open(self.file_path, 'rb') as wad_file:
            check_header(wad_file)

    def _load_lumps(self) -> List[Tuple[str, int, int]]:
        """
        Load lumps information from the WAD file.

        Returns:
            List[Tuple[str, int, int]]: List of lumps. Each tuple contains lump name, offset, and size.
        """
        with open(self.file_path, 'rb') as wad:
            # Skip WAD type
            wad.seek(4)

            # Read number of lumps and directory offset
            data = wad.read(8)
            num_lumps, dir_offset = struct.unpack('<ii', data)

            # Go to directory start
            wad.seek(dir_offset)
            lumps = []

            # Read each directory entry
            for _ in range(num_lumps):
                lump_data = wad.read(16)
                offset, size, name = struct.unpack('<ii8s', lump_data)
                name = name.rstrip(b'\0').decode('ascii')
                lumps.append((name, offset, size))
        return lumps

    @property
    def lumps(self) -> List[Tuple[str, int, int]]:
        """Lazy loading of lumps."""
        if self._lumps is None:
            self._lumps = self._load_lumps()
        return self._lumps

    def read_lump(self, lump_name: str) -> Optional[bytes]:
        """
        Read and return the data for the specified lump.

        Args:
            lump_name (str): The name of the lump to read.

        Returns:
            bytes: The lump data.
        """
        for name, offset, size in self.lumps:
            if name == lump_name:
                with open(self.file_path, 'rb') as wad:
                    wad.seek(offset)
                    return wad.read(size)
        return None

    def list_lump_names(self) -> List[str]:
        """
        List all the lump names in the WAD file.

        Returns:
            List[str]: List of lump names.
        """
        return [lump[0] for lump in self.lumps]
