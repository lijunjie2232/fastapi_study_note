from pathlib import Path

PROJ_ROOT = Path(__file__).parent.resolve()
CHUNK_SIZE = 1024 * 1024 * 32
HASH_METHOD = "sha256"

from .BinaryChunkMapManager import BinaryChunkMapManager, setup_file_and_chunk_map
from .utils import (
    calculate_hash,
    calculate_optimal_chunk_size,
    create_empty_file,
    parallel_write_chunks,
    write_chunk,
    write_chunk_to_position,
)

__all__ = [
    "write_chunk_to_position",
    "calculate_hash",
    "create_empty_file",
    "calculate_optimal_chunk_size",
    "parallel_write_chunks",
    "write_chunk",
    "setup_file_and_chunk_map",
    "BinaryChunkMapManager",
]
