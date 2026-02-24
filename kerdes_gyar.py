import datetime

import adatbazis
from kerdesek import DatumKerdes, FeleletValasztosKerdes, ListaKerdes, SzamKerdes


def kerdesek_betoltese_adatbazisbol(kapcsolat):

    kerdes_sorok = adatbazis.aktiv_kerdesek_lekerese(kapcsolat)

    kerdes_lista = []

    for sor in kerdes_sorok:
        kerdes_id = sor["id"]
        tipus = sor["tipus"]
        szoveg = sor["szoveg"]

        if tipus == "szam":
            helyes_szam = sor["helyes_szam"]
            kerdes_lista.append(SzamKerdes(kerdes_id, szoveg, helyes_szam))

        elif tipus == "datum":
            helyes_datum = sor["helyes_datum"]
            if isinstance(helyes_datum, str):
                helyes_datum = datetime.date.fromisoformat(helyes_datum)
            kerdes_lista.append(DatumKerdes(kerdes_id, szoveg, helyes_datum))

        elif tipus == "lista":
            helyes_elemek = adatbazis.lista_helyes_lekerese(kapcsolat, kerdes_id)
            kerdes_lista.append(ListaKerdes(kerdes_id, szoveg, helyes_elemek))

        elif tipus == "feleletvalasztos":
            opciok = adatbazis.valaszlehetosegek_lekerese(kapcsolat, kerdes_id)
            kerdes_lista.append(FeleletValasztosKerdes(kerdes_id, szoveg, opciok))

        else:
            print(f"Ismeretlen kérdéstípus: {tipus} (id={kerdes_id})")

    return kerdes_lista
