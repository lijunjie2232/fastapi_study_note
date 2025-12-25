from passlib.context import CryptContext
from passlib.hash import sha256_crypt, pbkdf2_sha256, scrypt, argon2

algorithms = {
    "sha256_crypt": sha256_crypt,
    "pbkdf2_sha256": pbkdf2_sha256,
    "scrypt": scrypt,
    "argon2": argon2,
}

pwd_context = {a: CryptContext(schemes=[a], deprecated="auto") for a in algorithms}


async def verify_password(plain_password, hashed_password):
    for a in algorithms:
        if pwd_context[a].verify(plain_password, hashed_password):
            return True
    return False


async def get_password_hash(password, algorithm="sha256_crypt"):
    if algorithm in algorithms:
        return pwd_context[algorithm].hash(password)
    raise ValueError(f"Unsupported algorithm: {algorithm}")


if __name__ == "__main__":
    from pprint import pprint

    password = "123456789"
    hashed_password = {a: pwd_context[a].hash(password) for a in algorithms}
    pprint("Hashed password:")
    pprint(hashed_password)

    verification_results = {
        a: pwd_context[a].verify(password, hashed_password[a]) for a in algorithms
    }
    pprint("Verification results:")
    pprint(verification_results)
