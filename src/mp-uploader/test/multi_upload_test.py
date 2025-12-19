import hashlib
import json
import logging
import os
from pathlib import Path

import httpx

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def calculate_file_hash(file_path):
    """Calculate SHA256 hash of a file"""
    hash_sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()


def get_file_size(file_path):
    """Get the size of a file in bytes"""
    return os.path.getsize(file_path)


def test_multipart_upload():
    base_url = "http://localhost:6666"

    # Use test_video.mp4 in the same directory
    test_file_path = Path(__file__).parent / "test_video2.mp4"

    # Check if test file exists
    if not os.path.exists(test_file_path):
        logger.error(f"Test file {test_file_path} not found in current directory")
        return

    # Get file info
    file_size = get_file_size(test_file_path)
    file_hash = calculate_file_hash(test_file_path)

    logger.info(
        f"Starting upload test for {test_file_path} of size {file_size} bytes with hash {file_hash}"
    )

    # Initialize upload
    response = httpx.post(
        f"{base_url}/upload/init",
        params={"file_size": file_size, "file_hash": file_hash},
    )
    logger.info(f"Init response: {json.dumps(response.json(), indent=2)}")

    # Get upload status
    response = httpx.get(f"{base_url}/upload/status/{file_hash}")
    logger.info(f"Status response: {json.dumps(response.json(), indent=2)}")

    # Upload chunks
    chunk_size = response.json()["chunk_size"]
    with open(test_file_path, "rb") as f:
        offset = 0
        chunk_number = 0
        while True:
            chunk_data = f.read(chunk_size)
            if not chunk_data:
                break

            chunk_hash = hashlib.sha256(chunk_data).hexdigest()

            # Upload chunk
            files = {"chunk": ("chunk", chunk_data)}
            response = httpx.post(
                f"{base_url}/upload/chunk",
                params={
                    "file_hash": file_hash,
                    "chunk_hash": chunk_hash,
                    "offset": offset,
                },
                files=files,
            )
            logger.info(
                f"Chunk {chunk_number} at offset {offset} response: {json.dumps(response.json(), indent=2)}"
            )

            offset += len(chunk_data)
            chunk_number += 1

    # Final status check
    response = httpx.get(f"{base_url}/upload/status/{file_hash}")
    logger.info(f"Final status response: {json.dumps(response.json(), indent=2)}")


if __name__ == "__main__":
    test_multipart_upload()
