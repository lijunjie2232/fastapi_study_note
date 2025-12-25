import jwt
import time
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
        return "Token has expired"
    except jwt.InvalidTokenError:
        return "Invalid token"


if __name__ == "__main__":
    # generate a sample JWT
    sample_payload = {"user_id": 123, "role": "admin"}
    token = generate_jwt(
        sample_payload,
        expires_in=2,  # token expires in 5 seconds
    )
    print("Generated JWT:")
    print(token)

    # decode the sample JWT
    decoded_payload = decode_jwt(token)
    print("[Result] Decoded JWT payload:", decoded_payload)
    print("[Result] Decoded with wrong key:", decode_jwt(token, secret="wrongkey"))
    print("* Decoded with expired token:")
    for _ in tqdm.tqdm(range(3), desc="Waiting for token to expire"):
        time.sleep(1)  # wait for token to expire
    print("[Result] ", decode_jwt(token))
