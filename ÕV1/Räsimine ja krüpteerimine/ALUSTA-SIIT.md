# Salasõna andmebaasis
**Debian või Ubuntu · 150 minutit praktilist tööd + kuni 30 minutit varuaega**

Loo Marile ja Jürile sama väljamõeldud salasõna. Mõlema konto jaoks valid ise uue soola, arvutad räsi ja salvestad tulemuse MariaDB-sse. Eraldi katses krüpteerid Mari salasõna nii, et seda saab võtmega avada. Lõpus kontrollib programm sinu salvestatud andmeid. Koodi kirjutada pole vaja.

## 1. Ava labor (10 min)
Paki ZIP lahti, ava terminal kaustas **praktikum** ja käivita `./lab start`. Oota teadet „Labor on valmis”. Vali ainult selle harjutuse jaoks salasõna, mida mäletad tunni lõpuni. Kasuta mõlema konto ja esimese kuue ülesande jaoks täpselt sama salasõna. Tippimisel salasõna ekraanile ei ilmu.

## 2. Krüpteeri salasõna ja salvesta tulemus (15 min)
1. Käivita terminalis `./lab krupteeri`. Sisesta Mari katsesalasõna. Kopeeri kogu väljastatud krüptogramm.
2. Ava MongoDB käsuga `./lab mongo`. Asenda sõna KRÜPTOGRAMM oma tulemusega ning sisesta järgmine käsk. Jäta jutumärgid alles.

       db.proov.replaceOne({_id:"mari"}, {_id:"mari", token:"KRÜPTOGRAMM"}, {upsert:true})

3. Kontrolli käsuga `db.proov.findOne({_id:"mari"})`, et väljal token on sinu kopeeritud väärtus. Terminali naasmiseks sisesta `exit`.

Krüpteerimisvõti luuakse labori esimesel käivitamisel ja seda hoitakse MongoDB-st eraldi. Kontrollprogramm avab salvestatud krüptogrammi sama võtmega. See kirje on mõeldud krüpteerimise harjutamiseks.

## 3. Loo kaks soola ja arvuta räsid (20 min)
1. Käivita terminalis `openssl rand -hex 16`. Kopeeri 32 märgist koosnev tulemus oma märkmetesse pealkirja **Mari sool** alla.
2. Käivita `./lab rasi`. Kleebi Mari sool ja sisesta katsesalasõna. Kopeeri 64-märgiline tulemus märkmetesse pealkirja **Mari räsi** alla.
3. Korda mõlemat sammu Jüri jaoks. Genereeri uus sool ja sisesta sama salasõna. Hoia kummagi kasutaja sool ja räsi paaris.

Võrdle tulemusi. Milline sisend muutus? Sool on avalik juhuarv. Labori räsitööriist kasutab salasõna ja soola koos scrypt-algoritmiga. Soola läheb uuesti vaja, kui kasutaja järgmisel korral sisse logib.

## 4. Salvesta soolad ja räsid MariaDB-sse (20 min)
Ava `./lab sql`. Asenda neli suurtähtedega kohatäitjat oma väärtustega. Kleebi täidetud käsk MariaDB aknasse koos lõpus oleva semikooloniga.

    REPLACE INTO harjutus (nimi, sool, rasi) VALUES
      ('mari', 'MARI_SOOL', 'MARI_RÄSI'),
      ('juri', 'JÜRI_SOOL', 'JÜRI_RÄSI');

Kontrolli mõlemat rida. Päring näitab ainult räsi algust.

    SELECT nimi, LENGTH(sool), LEFT(rasi, 8) FROM harjutus;

Kirjuta üles, kas räsialgused on erinevad. MariaDB-st väljumiseks sisesta `exit`. Kui hiljem avastad vea, saad parandatud REPLACE-käsu uuesti sisestada.

## 5. Märgi graafi Mari lugemisõigus (10 min)
Ava `./lab graaf`. Lisa seos järgmise käsuga.

    MERGE (k:Konto {nimi:'mari'}) MERGE (f:Fail {nimi:'aruanne'}) MERGE (k)-[:LOEB]->(f);

Välju käsuga `:exit`. Neo4j seob konto aruandega kasutajanime kaudu. Graafi jaoks piisab nimest ja õigusest.

## 6. Kontrolli algseisu (15 min)
Käivita `./lab kontroll` ja sisesta sama katsesalasõna. Otsi viit rida märkega **KORRAS**. Kui mõni rida näitab **PARANDA**, tee vastav samm uuesti. Kui mõlema konto räsid ja krüptogramm korraga kontrolli ei läbi, proovi esmalt salasõna uuesti sisestada.

Käivita kontroll veel kord ja sisesta meelega vale salasõna. Millised read jäid korras ja miks? Kontrolli lõpetuseks uuesti õige salasõnaga. Pane kirja algseisu kontrolli viis tulemust ja vasta kahele küsimusele:

1. Kuidas sai kontrollprogramm kindlaks teha, et MariaDB-s oleva räsiga sobib sinu salasõna?
2. Mida saab MongoDB krüptogrammi ja õige võtmega teha, mida MariaDB räsi ja soolaga teha ei saa?

## 7. Leia ja paranda vigane sool (25 min)

Mari teatab, et tema salasõna lakkas töötamast pärast kontoandmete parandamist. Tekita see olukord oma laboris. Hoia alles ülesande 3 märkmed, sest sealt leiad Mari õige soola.

1. Ennusta, millised viiest kontrollreast ebaõnnestuvad, kui Mari soola lahtrisse satub Jüri sool, aga Mari räsi jääb endiseks.
2. Ava `./lab sql`. Asenda JÜRI_SOOL Jüri tegeliku soolaga ja muuda ainult Mari kirjet.

       UPDATE harjutus SET sool='JÜRI_SOOL' WHERE nimi='mari';

3. Välju käsuga `exit`. Käivita `./lab kontroll` algse katsesalasõnaga. Märgi üles tegelikud vearead. Miks näitab Mari MongoDB proovikirje ikka KORRAS?
4. Taasta MariaDB-s sama UPDATE-käsuga Mari algne sool. Kontrolli uuesti. Kirjuta ühe lausega, milline tulemus kinnitab, et ka algne räsi jäi terveks.

## 8. Vaheta ainult Jüri salasõna (25 min)

Jüri valib uue katsesalasõna. Mari jätkab algsega. Kasuta ülesandest 3 tuttavaid käske, et luua Jürile värske sool ja arvutada tema uue salasõna räsi. Võrdle uut soola Jüri varasemaga.

Ava MariaDB ja asenda Jüri sool ja räsi **ühe käsuga**. Asenda kohatäitjad enda väärtustega.

    UPDATE harjutus SET sool='UUS_SOOL', rasi='UUS_RÄSI' WHERE nimi='juri';

Välju käsuga `exit`. Katseta vana salasõna käsuga `./lab kontroll`. See käsk proovib sama sisestust mõlemal kontol. Milline rida tõendab, et vana salasõna Jürile enam ei sobi? Milline rida kinnitab, et Mari konto töötab endiselt?

Käivita nüüd `./lab lopukontroll`. Esimese küsimuse juures sisesta Mari algne salasõna ja teise juures Jüri uus salasõna. Otsi kuut rida märkega **KORRAS**. Kui Jüri rida ebaõnnestub, kontrolli, kas kasutasid räsimisel ja salvestamisel sama uut soola.

## 9. Esita katsete tulemused (10 min)

Lisa ülesande 6 vastustele järgmine tabel. Märgi iga katse juurde tegelikult nähtud tulemus ja selle põhjus.

| Katse | Millised kontrollread näitasid PARANDA? | Mis põhjustas tulemuse? |
|---|---|---|
| Mari kirjes oli Jüri sool | | |
| Mari algne sool oli taastatud | | |
| Pärast salasõnavahetust prooviti Jüri kontol vana salasõna | | |

Lisa kuus lõppkontrolli rida. Jäta salasõnad oma vastusest välja. Peata labor käsuga `./lab stop`.
