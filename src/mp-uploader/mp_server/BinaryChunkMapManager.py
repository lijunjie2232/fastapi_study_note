import json
import math
import struct
import threading
from pathlib import Path

from .utils import calculate_optimal_chunk_size, create_empty_file


class BinaryChunkMapManager:
    def __init__(self, filename, dir):
        self.map_file = Path(dir) / f"{filename}.bmap"
        self.data_file = Path(dir) / filename
        self.lock = threading.Lock()
        self.chunk_size = None
        self.magic_number = 0xB17CCA  # Binary MAP identifier
        self.header_format = "QQQ"  # magic_number, total_chunks, chunk_size
        self.header_size = struct.calcsize(self.header_format)
        self.init()

    def check_init(self):
        assert self.chunk_size != None, Exception(
            "Chunk size not initialized. Please call initialize_map() first."
        )
        return True

    def init(self):
        # if map file exists, then read chuck_size info from it
        if self.map_file.exists():
            with open(self.map_file, "rb") as f:
                header_data = f.read(self.header_size)
                magic, total_chunks, chunk_size = struct.unpack(
                    self.header_format, header_data
                )
                assert magic == self.magic_number, Exception(
                    "Invalid binary chunk map file. Please check the file."
                )
                self.chunk_size = chunk_size

    def initialize_map(self, file_size, chunk_size, reinit=False):
        if self.map_file.exists() and not reinit:
            return
        """Initialize binary chunk map file with bitmap structure"""

        self.chunk_size = chunk_size

        total_chunks = math.ceil(file_size / chunk_size)
        bitmap_size = math.ceil(total_chunks / 8)  # 8 bits per byte

        # Create header
        header = struct.pack(
            self.header_format, self.magic_number, total_chunks, chunk_size
        )

        # Create empty bitmap
        bitmap = bytearray(bitmap_size)

        # Write to binary file
        with self.lock:
            with open(self.map_file, "wb") as f:
                f.write(header)
                f.write(bitmap)

    def mark_chunk(self, offset, complete=True):
        self.check_init()
        """Mark specific chunk as completed or incompleted in bitmap using direct offset writing"""
        chunk_index = offset // self.chunk_size

        with self.lock:
            with open(self.map_file, "r+b") as f:
                # Calculate exact position of the bit in the bitmap
                byte_index = chunk_index // 8
                bit_index = chunk_index % 8

                # Seek directly to the byte containing this bit
                f.seek(self.header_size + byte_index)

                # Read current byte
                current_byte = ord(f.read(1))

                # Set the specific bit to 1 (completed)
                if complete:
                    updated_byte = current_byte | (1 << bit_index)
                else:
                    # Incomplete
                    updated_byte = current_byte & ~(1 << bit_index)

                # Write back only the modified byte
                f.seek(self.header_size + byte_index)
                f.write(bytes([updated_byte]))

    def get_chunk_status(self, offset):
        self.check_init()
        """Get chunk status (completed or incomplete)"""
        chunk_index = offset // self.chunk_size

        with self.lock:
            with open(self.map_file, "rb") as f:
                # Calculate exact position of the bit in the bitmap
                byte_index = chunk_index // 8
                bit_index = chunk_index % 8

                # Seek directly to the byte containing
                f.seek(self.header_size + byte_index)
                current_byte = ord(f.read(1))
                return (current_byte >> bit_index) & 1

    def get_incomplete_chunks(self):
        self.check_init()
        """Get list of incomplete chunk offsets from bitmap"""
        incomplete = []

        with self.lock:
            with open(self.map_file, "rb") as f:
                # Read header
                header_data = f.read(self.header_size)
                magic, total_chunks, chunk_size = struct.unpack(
                    self.header_format, header_data
                )

                # Read bitmap
                bitmap_size = math.ceil(total_chunks / 8)
                bitmap = f.read(bitmap_size)

                # Check each chunk status
                for i in range(total_chunks):
                    byte_index = i // 8
                    bit_index = i % 8

                    if byte_index < len(bitmap):
                        bit_value = (bitmap[byte_index] >> bit_index) & 1
                        if bit_value == 0:  # Not completed
                            incomplete.append(i * chunk_size)

        return incomplete

    def is_complete(self):
        if self.chunk_size is None:
            return False
        """Check if all chunks are completed"""
        incomplete = self.get_incomplete_chunks()
        return len(incomplete) == 0


def setup_file_and_chunk_map(filename, dir, size, chunk_size=None):
    """Create both file and chunk map simultaneously"""
    # Create sparse file
    create_empty_file(filename, dir, size)

    # Create chunk map manager
    chunk_manager = BinaryChunkMapManager(filename, dir)

    # # Initialize chunk map
    chunk_manager.initialize_map(size, chunk_size)

    return chunk_manager
