import hashlib
import json
import os
import threading
from pathlib import Path, PosixPath
from typing import BinaryIO

from . import HASH_METHOD


def create_empty_file(filename: str, dir: str | PosixPath, size: int):
    """Create sparse file of specified size"""
    with open(Path(dir) / filename, "wb") as f:
        f.seek(size - 1)
        f.write(b"\0")


def write_chunk_to_position(filename, offset: int, data: bytes):
    """Write chunk data to specific file position"""
    with open(filename, "r+b") as f:
        f.seek(offset)
        f.write(data)


def calculate_hash(
    filename=None, fileIO: BinaryIO = None, hash_type=HASH_METHOD
) -> str:
    """Calculate MD5 hash of entire file
    hash_method:

    """
    assert filename or fileIO, Exception("Either filename or fileIO must be provided")
    assert hash_type in hashlib.algorithms_available, Exception(
        f"Hash method {hash_type} not available. Available methods: {hashlib.algorithms_available}"
    )
    hash = getattr(hashlib, hash_type)()

    if filename:
        with open(filename, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash.update(chunk)
        return hash.hexdigest()
    else:
        try:
            assert hasattr(fileIO, "read"), Exception("fileIO is not readable")
            for chunk in iter(lambda: fileIO.read(4096), b""):
                hash.update(chunk)
            return hash.hexdigest()
        except Exception as e:
            raise Exception(f"Error calculating hash: {e}")


# Write chunk at specific position
def write_chunk(filename, position, data, lock):
    with lock:  # Ensure thread-safe file access
        with open(filename, "r+b") as f:
            f.seek(position)
            f.write(data)


# Multithreaded writing example
def parallel_write_chunks(filename, chunks_data):
    lock = threading.Lock()
    threads = []

    for position, data in chunks_data:
        t = threading.Thread(target=write_chunk, args=(filename, position, data, lock))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()


# calculate_optimal_chunk_size
def calculate_optimal_chunk_size(file_size):
    """Calculate optimal chunk size based on file size"""
    # Example: 1MB chunks for files smaller than 10MB, 5MB chunks for larger files
    if file_size < 10 * 1024 * 1024:
        return 1024 * 1024
    else:
        return 5 * 1024 * 1024
