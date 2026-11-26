"""Soolatud räsi arvutamine ja kontrollimine õppelaboris."""
import argparse
import getpass
import hashlib
import hmac
import re


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tegevus", choices=["loo", "kontrolli"])
    action = parser.parse_args().tegevus
    salt = input("Sool (32 kuueteistkümnendmärki): ").strip()
    if not re.fullmatch(r"[0-9a-fA-F]{32}", salt):
        parser.error("Kopeeri kogu 16-baidine sool.")
    if action == "kontrolli":
        saved = input("MariaDB-st loetud räsi (64 märki): ").strip().lower()
        if not re.fullmatch(r"[0-9a-f]{64}", saved):
            parser.error("Kopeeri kogu salvestatud räsi.")
    password = getpass.getpass("Katsesalasõna: ")
    if not password:
        parser.error("Sisesta katsesalasõna.")
    digest = hashlib.scrypt(password.encode(), salt=bytes.fromhex(salt),
                            n=2**17, r=8, p=1, maxmem=256*1024**2, dklen=32).hex()
    if action == "loo":
        print(digest)
        return 0
    ok = hmac.compare_digest(saved, digest)
    print("KATTUB" if ok else "EI KATTU")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
