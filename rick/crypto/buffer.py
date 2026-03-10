import hashlib
import warnings
from io import BytesIO

APPROVED_ALGORITHMS = {"sha256", "sha384", "sha512", "blake2b", "blake2s"}


def hash_buffer(method, buf: BytesIO) -> str:
    if method not in APPROVED_ALGORITHMS:
        raise ValueError(
            "hash_buffer(): algorithm '{}' not approved; use one of: {}".format(
                method, ", ".join(sorted(APPROVED_ALGORITHMS))
            )
        )
    fn = getattr(hashlib, method)
    buf.seek(0)
    return fn(buf.read()).hexdigest()


def sha256_hash(buf: BytesIO) -> str:
    buf.seek(0)
    return hashlib.sha256(buf.read()).hexdigest()


def sha1_hash(buf: BytesIO) -> str:
    warnings.warn(
        "sha1_hash() is deprecated: SHA-1 is cryptographically broken; use sha256_hash() or sha512_hash() instead",
        DeprecationWarning,
        stacklevel=2,
    )
    buf.seek(0)
    return hashlib.sha1(buf.read()).hexdigest()


def sha512_hash(buf: BytesIO) -> str:
    buf.seek(0)
    return hashlib.sha512(buf.read()).hexdigest()


def blake2_hash(buf: BytesIO) -> str:
    buf.seek(0)
    return hashlib.blake2b(buf.read()).hexdigest()
