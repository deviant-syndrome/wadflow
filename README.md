# WadFlow

WadFlow is a Python library designed to simplify reading from and writing to DOOM WAD files. It is not a full-featured WAD editor, but rather a tool for reading and writing lumps. 
This library is not concerned with WAD game-specific inner semantics, and does not provide any functionality for editing lumps. It is designed to be used as a building block and automation tool for more complex WAD editors.
It is written in pure Python and has no dependencies, it is not built for performance but rather for simplicity and ease of use, 
so it can be used to perform batch tasks on WAD files.

# Features
* Read lumps from WAD files.
* Write lumps to WAD files.
* Basic header verification to ensure WAD file integrity.
* Simple and intuitive API.

# Usage
## Reading a WAD
```python
from wadflow import WADFile

# Load the WAD file
wad = WADFile("path_to_wad_file.wad")

# List lump names
print(wad.list_lump_names())

# Read specific lump data
data = wad.read_lump("LUMP_NAME")
```
## Writing to a WAD
```python
from wadflow import WriteableLump, write_lumps_to_wad

# Create a lump
lump = WriteableLump("LUMP_NAME", b"your binary data")

# Write lumps to a new PWAD file
write_lumps_to_wad([lump], "output_path.wad")
```

# Documentation
## WADFile
**init(self, file_path: str):** Initializes a new WADFile instance.

**read_lump(self, lump_name: str) -> bytes:** Reads a lump by name and returns its data.

**list_lump_names(self) -> List[str]:** Lists all the lump names in the WAD file.

## WriteableLump
**init(self, name: str, data: bytes):** Creates a new lump with a name and binary data.

**get_size(self) -> int:** Returns the size of the lump's data.

**get_data(self) -> bytes:** Returns the lump's binary data.

## Functions
**write_lumps_to_wad(lumps: List[WriteableLump], wad_filepath: str):** Writes a list of lumps to a new WAD file.

# Testing
WadFlow includes unit tests. Run them with:
```bash
python -m unittest discover -s tests
```

# License
0BSD
