import json
import time
from datetime import datetime, timedelta, timezone

import jwt
import tqdm

# import secrets

# print(secrets.token_hex(32))
# exit(0)

SECURITY_ALGORITHM = "HS256"
SECURITY_KEY = "e3c56abd1523a8fd4b73da842c272d1cf8a42acc78aafbd18890daaa2feb4755"


def generate_jwt(payload, secret=SECURITY_KEY, algorithm="HS256", expires_in=None):
    if expires_in is not None:
        import datetime

        payload["exp"] = datetime.datetime.now(datetime.UTC) + datetime.timedelta(
            seconds=expires_in
        )
    token = jwt.encode(
        payload,
        secret,
        algorithm=algorithm,
    )
    return token


def decode_jwt(token, secret=SECURITY_KEY, algorithms=["HS256"]):
    try:
        decoded = jwt.decode(token, secret, algorithms=algorithms)
        return decoded
    except jwt.ExpiredSignatureError:
        raise Exception("Token has expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid token")


def create_access_token(
    data: dict, expires_delta: timedelta | None = timedelta(seconds=60 * 60 * 24)
):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECURITY_KEY, algorithm=SECURITY_ALGORITHM)
    return encoded_jwt


if __name__ == "__main__":
    # generate a sample JWT
    sample_payload = {"user_id": 123, "role": "admin"}
    # token = generate_jwt(
    #     sample_payload,
    #     expires_in=2,  # token expires in 5 seconds
    # )
    token = create_access_token(
        data=sample_payload,
        expires_delta=timedelta(seconds=2),
    )
    print("Generated JWT:")
    print(token)

    # decode the sample JWT
    decoded_payload = decode_jwt(token)
    print("[Result] Decoded JWT payload:", decoded_payload)
    try:
        print("[Result] Decoded with wrong key:", decode_jwt(token, secret="wrongkey"))
    except Exception as e:
        print("[Result] Decoding with wrong key failed:", str(e))
    print("* Decoded with expired token:")
    for _ in tqdm.tqdm(range(3), desc="Waiting for token to expire"):
        time.sleep(1)  # wait for token to expire
    try:
        print("[Result] ", decode_jwt(token))
    except Exception as e:
        print("[Result] Decoding expired token failed:", str(e))
