import MySQLdb
import MySQLdb.cursors


def adatbazis_kapcsolat():
    return MySQLdb.connect(
        host="localhost",
        user="jozsef",
        passwd="bozso",
        db="kviz",
        charset="utf8mb4",
        use_unicode=True,
    )


def aktiv_kerdesek_lekerese(kapcsolat):
    kurzor = kapcsolat.cursor(MySQLdb.cursors.DictCursor)
    kurzor.execute("""
        SELECT id, tipus, szoveg, helyes_szam, helyes_datum
        FROM kerdes
        WHERE aktiv = 1
        ORDER BY id
        """)
    return kurzor.fetchall()


def valaszlehetosegek_lekerese(kapcsolat, kerdes_id):
    kurzor = kapcsolat.cursor(MySQLdb.cursors.DictCursor)
    kurzor.execute(
        """
        SELECT id, szoveg, helyes
        FROM valaszlehetoseg
        WHERE kerdes_id = %s
        ORDER BY id
        """,
        (kerdes_id,),
    )
    return kurzor.fetchall()


def lista_helyes_lekerese(kapcsolat, kerdes_id):
    kurzor = kapcsolat.cursor()
    kurzor.execute(
        """
        SELECT elem
        FROM lista_helyes
        WHERE kerdes_id = %s
        ORDER BY id
        """,
        (kerdes_id,),
    )
    return [sor[0] for sor in kurzor.fetchall()]


def futas_letrehozasa(kapcsolat, jatekos_nev):
    kurzor = kapcsolat.cursor()
    kurzor.execute(
        "INSERT INTO futas (jatekos_nev) VALUES (%s)",
        (jatekos_nev,),
    )
    kapcsolat.commit()
    return kurzor.lastrowid


def valasz_mentese(
    kapcsolat,
    futas_id,
    kerdes_id,
    valasztott_valasz_id=None,
    adott_szoveg=None,
    adott_szam=None,
    adott_datum=None,
    helyes=0,
    pont=0.0,
    elteres_szam=None,
    elteres_nap=None,
):
    kurzor = kapcsolat.cursor()
    kurzor.execute(
        """
        INSERT INTO naplo (
            futas_id, kerdes_id, valasztott_valasz_id, adott_szoveg, adott_szam,
            adott_datum, helyes, pont, elteres_szam, elteres_nap
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """,
        (
            futas_id,
            kerdes_id,
            valasztott_valasz_id,
            adott_szoveg,
            adott_szam,
            adott_datum,
            helyes,
            pont,
            elteres_szam,
            elteres_nap,
        ),
    )
    kapcsolat.commit()


if __name__ == "__main__":
    kapcsolat = None
    try:
        kapcsolat = adatbazis_kapcsolat()

        kerdesek = aktiv_kerdesek_lekerese(kapcsolat)
        print(f"Aktív kérdések száma: {len(kerdesek)}")

        for k in kerdesek:
            print(f'{k["id"]} | {k["tipus"]} | {k["szoveg"][:60]}')

            if k["tipus"] == "feleletvalasztos":
                opciok = valaszlehetosegek_lekerese(kapcsolat, k["id"])
                print(" opciók:", [o["szoveg"] for o in opciok])

            if k["tipus"] == "lista":
                elemek = lista_helyes_lekerese(kapcsolat, k["id"])
                print(" helyes elemek:", elemek)

    except Exception as e:
        print("Hiba:", e)

    finally:
        if kapcsolat:
            kapcsolat.close()
