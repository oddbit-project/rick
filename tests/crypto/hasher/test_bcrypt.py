import pytest
from rick.crypto.hasher.bcrypt import BcryptHasher


class TestBcryptHasher:
    rounds = 8  # lower round count for testing purposes
    valid_passwords = {
        "12345678": "$2b$08$Ex7KPIGtDml1hzlpSjlZv.S4F6ToP1DD1L8bylO6i6v8U9OmCU.IG",
        "sdktrqjkl4dskl": "$2b$08$2A/LDGvtHdhayOEqLXThaOM5jq.IcvGI18JBy/xjQsxlOj8MlsXiO",
        "423FDS$&dYdcWs/dAS5": "$2b$08$yjsNQsYLFMHrCZXAKbdItObDtMjScF/GViqyGMb4zP3EggvxRAkR2",
    }

    invalid_passwords = [
        "",
    ]

    def test_hash(self):
        bc = BcryptHasher(self.rounds)
        for pw, compat_hash in self.valid_passwords.items():
            pw_hash = bc.hash(pw)
            assert len(pw_hash) > 16
            tokens = pw_hash[1:].split("$", 2)
            assert tokens[0] == bc._prefix
            assert int(tokens[1]) == bc._rounds
            assert bc.is_valid(pw, compat_hash) is True
            assert bc.need_rehash(pw_hash) is False

        # test cases where rehash is needed
        bc = BcryptHasher(self.rounds + 1)
        for pw, compat_hash in self.valid_passwords.items():
            pw_hash = bc.hash(pw)
            # new hash has round=9
            assert bc.need_rehash(pw_hash) is False
            # existing hash has round=8
            assert bc.need_rehash(compat_hash) is True

    def test_hash_exception(self):
        bc = BcryptHasher(self.rounds)
        for pwd in self.invalid_passwords:
            with pytest.raises(ValueError):
                _ = bc.hash(pwd)
