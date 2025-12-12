import os
from pathlib import Path
from typing import List
from fastapi import FastAPI, File, UploadFile, Query

from mp_server import (
    CHUNK_SIZE,
    PROJ_ROOT,
    HASH_METHOD,
    BinaryChunkMapManager,
    setup_file_and_chunk_map,
    calculate_hash,
    write_chunk_to_position,
)

app = FastAPI()

__UPLOAD_DIR__ = PROJ_ROOT / "upload"
__UPLOAD_DIR__.mkdir(parents=True, exist_ok=True)


@app.post("/upload/init")
async def init_upload(
    file_size: int,
    file_hash: str,
):
    file_path = __UPLOAD_DIR__ / f"{file_hash}"
    # Check if file already exists with matching hash
    # Not support dir yet
    if file_path.is_file():
        # there is no need to repleace a file with another file having the same hash
        if calculate_hash(file_path) == file_hash:
            return {
                "status": "completed",
                "message": "File already exists",
            }
        else:
            # check if there is a incomplete upload task
            chunk_manager = BinaryChunkMapManager(f"{file_hash}", __UPLOAD_DIR__)
            try:
                chunk_manager.check_init()
                return {
                    "status": "incomplete",
                    "message": "Upload not finish",
                    "chunk_size": CHUNK_SIZE,
                    "hash": HASH_METHOD,
                    "chunks": chunk_manager.get_incomplete_chunks(),
                }
            except Exception:
                # there is not a valid chunk map, so this is a new upload task
                pass
    # Create empty file with hash as name
    chunk_manager = setup_file_and_chunk_map(
        f"{file_hash}",
        __UPLOAD_DIR__,
        file_size,
        CHUNK_SIZE,
    )

    # Generate chunk ranges map and return
    return {
        "status": "incomplete",
        "message": "multi-part upload task ready",
        "chunk_size": CHUNK_SIZE,
        "hash": HASH_METHOD,
        "chunks": chunk_manager.get_incomplete_chunks(),
    }


@app.post("/upload/chunk")
async def upload_chunk(
    file_hash: str,
    chunk_hash: str,
    offset: int,
    chunk: UploadFile = File(...),
):
    """here first check the chunk_hash, if chunk_hash matches,
        write the chunk to the file by offset
        and update the bitmap by chunk status manager

    Args:
        file_hash (str): the hash of total file
        chunk_hash (str): the hash of current chunk
        offset (int): the offset of current chunk
        chunk (UploadFile, optional): _description_. Defaults to File(...).
    """
    file_path = __UPLOAD_DIR__ / f"{file_hash}"
    chunk_manager = BinaryChunkMapManager(f"{file_hash}", __UPLOAD_DIR__)
    if chunk_manager.is_complete():
        return {
            "status": "completed",
            "message": "Upload ",
        }
    if chunk_hash == calculate_hash(fileIO=chunk.file):
        chunk.file.seek(0)
        write_chunk_to_position(file_path, offset, chunk.file.read())
        chunk_manager.mark_chunk(offset, complete=True)
        return {
            "status": "chunk_completed",
            "message": "Chunk upload finished",
        }
    else:
        return {
            "status": "chunk_failed",
            "message": "Chunk upload failed",
        }
    pass


@app.get("/upload/status/{file_hash}")
async def get_upload_status(file_hash: str):
    file_path = __UPLOAD_DIR__ / f"{file_hash}"

    chunk_manager = BinaryChunkMapManager(f"{file_hash}", __UPLOAD_DIR__)
    if not chunk_manager.is_complete():
        return {
            "status": "incomplete",
            "message": "Upload not finish",
            "chunk_size": CHUNK_SIZE,
            "hash": HASH_METHOD,
            "chunks": chunk_manager.get_incomplete_chunks(),
        }
    else:
        # check hash of the total file
        if calculate_hash(file_path) == file_hash:
            return {
                "status": "completed",
                "message": "File already exists",
            }
        else:
            return {
                "status": "bad_file",
                "message": "File hash mismatch",
            }


@app.post("/upload/verify-chunks")
async def verify_chunks(file_hash: str, chunk_hashes: dict):
    """
    Verify chunk hashes and reset bitmap for bad chunks.

    Args:
        file_hash (str): The hash of the total file
        chunk_hashes (dict): Dictionary mapping offset to chunk hash

    Returns:
        dict: Status and list of incomplete chunks
    """
    chunk_manager = BinaryChunkMapManager(file_hash, __UPLOAD_DIR__)

    # Check each provided chunk hash
    for offset_str, chunk_hash in chunk_hashes.items():
        offset = int(offset_str)

        # Read the chunk data from file
        file_path = __UPLOAD_DIR__ / f"{file_hash}"
        with open(file_path, "rb") as f:
            f.seek(offset)
            chunk_data = f.read(CHUNK_SIZE)  # Assuming fixed chunk size

        # Calculate actual chunk hash
        actual_hash = calculate_hash(chunk_data)

        # If hash doesn't match, mark chunk as incomplete
        if actual_hash != chunk_hash:
            chunk_manager.mark_chunk(offset, complete=False)

    # Return all incomplete chunks
    return {
        "status": "incomplete",
        "chunk_size": CHUNK_SIZE,
        "hash": HASH_METHOD,
        "incomplete_chunks": chunk_manager.get_incomplete_chunks(),
    }


@app.get("/download/init")
async def init_download(file_hash: str):
    """Initialize download by checking file existence and returning chunk information"""
    file_path = __UPLOAD_DIR__ / f"{file_hash}"

    # Check if file exists
    if not file_path.is_file():
        return {
            "status": "error",
            "message": "File not found",
        }

    # Verify file integrity
    if calculate_hash(file_path) != file_hash:
        return {
            "status": "error",
            "message": "File hash mismatch",
        }

    # Get file size
    file_size = file_path.stat().st_size

    # Create chunk manager to get chunk information
    chunk_manager = BinaryChunkMapManager(f"{file_hash}", __UPLOAD_DIR__)
    try:
        chunk_manager.check_init()
    except Exception:
        # If no chunk map exists, create one
        setup_file_and_chunk_map(f"{file_hash}", __UPLOAD_DIR__, file_size, CHUNK_SIZE)
        chunk_manager = BinaryChunkMapManager(f"{file_hash}", __UPLOAD_DIR__)

    return {
        "status": "ready",
        "message": "Download ready",
        "file_size": file_size,
        "chunk_size": CHUNK_SIZE,
        "hash": HASH_METHOD,
        "total_chunks": (file_size + CHUNK_SIZE - 1) // CHUNK_SIZE,
        "chunks": [
            i * CHUNK_SIZE for i in range((file_size + CHUNK_SIZE - 1) // CHUNK_SIZE)
        ],  # All chunk offsets
    }


@app.get("/download/chunk")
async def download_chunk(file_hash: str, offset: int):
    """Download a specific chunk of the file"""
    file_path = __UPLOAD_DIR__ / f"{file_hash}"

    # Check if file exists
    if not file_path.is_file():
        return {
            "status": "error",
            "message": "File not found",
        }

    try:
        # Read chunk data from file
        with open(file_path, "rb") as f:
            f.seek(offset)
            chunk_data = f.read(CHUNK_SIZE)

        # Calculate chunk hash for verification
        chunk_hash = calculate_hash(chunk_data)

        return {
            "status": "chunk_ready",
            "chunk_hash": chunk_hash,
            "offset": offset,
            "size": len(chunk_data),
            "data": chunk_data,  # This would be the binary data
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to read chunk: {str(e)}",
        }


@app.get("/download/chunk-hashes")
async def get_chunk_hashes(file_hash: str, offsets: List[int] = Query([])):
    """
    Get hash values for specified chunks or all chunks of a file.

    Args:
        file_hash (str): The hash of the file
        offsets (str, optional): Comma-separated list of offsets to get hashes for.
                                If not provided, returns hashes for all chunks.

    Returns:
        dict: Status and chunk hashes mapping offset to hash
    """
    file_path = __UPLOAD_DIR__ / f"{file_hash}"

    # Check if file exists
    if not file_path.is_file():
        return {
            "status": "error",
            "message": "File not found",
        }

    try:
        # Get file size
        file_size = file_path.stat().st_size

        # Determine which offsets to process
        # if offsets:
        #     # Parse comma-separated offsets
        #     target_offsets = [int(offset.strip()) for offset in offsets.split(",")]
        # else:
        # if not offsets:
        # # Generate all chunk offsets
        # target_offsets = [
        #     i * CHUNK_SIZE
        #     for i in range((file_size + CHUNK_SIZE - 1) // CHUNK_SIZE)
        # ]

        target_offsets = (
            [i * CHUNK_SIZE for i in range((file_size + CHUNK_SIZE - 1) // CHUNK_SIZE)]
            if not offsets
            else offsets
        )

        # Calculate hash for each requested chunk
        chunk_hashes = {}
        with open(file_path, "rb") as f:
            for offset in target_offsets:
                # Validate offset is within file bounds
                if offset >= file_size:
                    continue

                f.seek(offset)
                chunk_data = f.read(CHUNK_SIZE)
                chunk_hash = calculate_hash(chunk_data)
                chunk_hashes[offset] = chunk_hash

        return {
            "status": "success",
            "chunk_size": CHUNK_SIZE,
            "hash": HASH_METHOD,
            "chunk_hashes": chunk_hashes,
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to calculate chunk hashes: {str(e)}",
        }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
