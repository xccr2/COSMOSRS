import os
import sys
import secrets
import hashlib
from getpass import getpass
from pathlib import Path
from cryptography.fernet import Fernet, InvalidToken

KEY = Path("/keys/fernet.key")


def derive(password, salt):
    return hashlib.scrypt(password.encode(), salt=salt, n=2**17, r=8, p=1,
                          maxmem=256 * 1024**2, dklen=32).hex()


def read_password(prompt="Sisesta katsesalasõna: "):
    value = getpass(prompt)
    if not value:
        raise ValueError("Salasõna on tühi.")
    return value


def salt_bytes(value):
    if not isinstance(value, str) or len(value) != 32:
        raise ValueError("Sool peab olema 32 kuueteistkümnendmärki.")
    salt = bytes.fromhex(value)
    if len(salt) != 16:
        raise ValueError("Vigane sool.")
    return salt


def verify_rows(rows, docs, links, password, cipher, juri_password=None):
    results = []
    salts = []
    for name in ("mari", "juri"):
        ok = False
        if name in rows:
            try:
                salt, digest = rows[name]
                raw = salt_bytes(salt)
                salts.append(raw)
                ok = secrets.compare_digest(derive(juri_password if name == "juri" and juri_password is not None else password, raw), digest)
            except (ValueError, TypeError):
                pass
        results.append((f"MariaDB: {name} sool ja räsi vastavad salasõnale", ok))
    results.append(("MariaDB: kontodel on erinevad soolad", len(set(salts)) == 2))
    try:
        doc = docs[0]
        ok = (len(docs) == 1 and set(doc) == {"_id", "token"} and
              cipher.decrypt(doc["token"]) == password.encode())
    except (IndexError, InvalidToken, TypeError, ValueError, KeyError):
        ok = False
    results.append(("MongoDB: Mari proovikirje avaneb algseks salasõnaks", ok))
    results.append(("Neo4j: Mari saab aruannet lugeda", links == 1))
    return results


def databases(action):
    import pymysql
    from pymongo import MongoClient
    from neo4j import GraphDatabase
    with pymysql.connect(host="sql", user="lab", password=os.environ["SQL_PASS"],
                         database="lab", autocommit=True, connect_timeout=3) as sql, sql.cursor() as cur, \
         MongoClient("mongo", username="lab", password=os.environ["MONGO_PASS"],
                     serverSelectionTimeoutMS=3000) as mongo, \
         GraphDatabase.driver("bolt://graph:7687", auth=("neo4j", os.environ["GRAPH_PASS"])) as driver, \
         driver.session() as graph:
        if action == "init":
            mongo.admin.command("ping")
            graph.run("RETURN 1").consume()
            cur.execute("""CREATE TABLE IF NOT EXISTS harjutus
                        (nimi VARCHAR(32) PRIMARY KEY, sool VARCHAR(32) NOT NULL,
                         rasi VARCHAR(64) NOT NULL)""")
            try:
                with KEY.open("xb") as f:
                    f.write(Fernet.generate_key())
            except FileExistsError:
                pass
            return
        password = read_password("Sisesta Mari katsesalasõna: ")
        juri_password = None
        if action == "lopukontroll":
            juri_password = read_password("Sisesta Jüri uus katsesalasõna: ")
        cur.execute("SELECT nimi,sool,rasi FROM harjutus WHERE nimi IN ('mari','juri')")
        rows = {name: (salt, digest) for name, salt, digest in cur}
        docs = list(mongo.lab.proov.find({"_id": "mari"}))
        links = graph.run("MATCH (:Konto {nimi:'mari'})-[r:LOEB]->(:Fail {nimi:'aruanne'}) RETURN count(r) AS n").single()["n"]
        results = verify_rows(rows, docs, links, password, Fernet(KEY.read_bytes()), juri_password)
        if action == "lopukontroll":
            results.append(("Kontodel on erinevad salasõnad", password != juri_password))
        for label, ok in results:
            print(("KORRAS" if ok else "PARANDA"), label)
        return int(not all(ok for _, ok in results))


def main(action):
    if action == "krupteeri":
        print(Fernet(KEY.read_bytes()).encrypt(read_password().encode()).decode())
    elif action == "rasi":
        salt = salt_bytes(input("Kleebi selle konto sool: ").strip())
        print(derive(read_password(), salt))
    elif action in ("init", "kontroll", "lopukontroll"):
        return databases(action)
    else:
        raise ValueError("Tundmatu käsk.")


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1]))
    except ValueError as error:
        sys.exit(str(error))
