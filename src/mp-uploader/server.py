import os
from pathlib import Path

from fastapi import FastAPI, File, UploadFile

from mp_server import (
    CHUNK_SIZE,
    PROJ_ROOT,
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
    chunk_manager = BinaryChunkMapManager(f"{file_hash}", __UPLOAD_DIR__)
    if chunk_manager.is_complete():
        return {
            "status": "completed",
            "message": "Upload ",
        }
    if chunk_hash == calculate_hash(chunk.file):
        write_chunk_to_position(f"{file_hash}", offset, chunk.file.read())
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
        "incomplete_chunks": chunk_manager.get_incomplete_chunks(),
        "chunk_size": CHUNK_SIZE,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=6666)
