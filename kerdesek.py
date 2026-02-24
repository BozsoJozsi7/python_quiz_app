import datetime
from abc import ABC, abstractmethod

import unidecode


def egyszerusit(szoveg: str) -> str:
    return unidecode.unidecode(szoveg.strip().lower())


class Kerdes(ABC):
    def __init__(self, kerdes_id: int, szoveg: str, tipus: str):
        self.kerdes_id = kerdes_id
        self.szoveg = szoveg
        self.tipus = tipus

    @abstractmethod
    def ertekel(self, valasz):
        pass


class SzamKerdes(Kerdes):
    def __init__(self, kerdes_id: int, szoveg: str, helyes_szam: float):
        super().__init__(kerdes_id, szoveg, "szam")
        self.helyes_szam = float(helyes_szam)

    def ertekel(self, valasz):
        try:
            adott = float(valasz)
        except (TypeError, ValueError):
            return {
                "helyes": 0,
                "pont": 0.0,
                "uzenet": "Nem számot adtál meg.",
                "adott_szam": None,
                "elteres_szam": None,
            }

        elteres = adott - self.helyes_szam

        if self.helyes_szam != 0:
            elteres_szazalek = (elteres / self.helyes_szam) * 100
        else:
            elteres_szazalek = 0

        if adott == self.helyes_szam:
            return {
                "helyes": 1,
                "pont": 1.0,
                "uzenet": "A válasz helyes!",
                "adott_szam": adott,
                "elteres_szam": elteres,
            }

        if -20 <= elteres_szazalek <= 25:
            return {
                "helyes": 0,
                "pont": 0.5,
                "uzenet": f"A válasz majdnem jó. Eltérés: {elteres:.3g}",
                "adott_szam": adott,
                "elteres_szam": elteres,
            }

        return {
            "helyes": 0,
            "pont": 0.0,
            "uzenet": f"A válasz helytelen. Eltérés: {elteres:.3g}",
            "adott_szam": adott,
            "elteres_szam": elteres,
        }


class DatumKerdes(Kerdes):
    def __init__(self, kerdes_id: int, szoveg: str, helyes_datum: datetime.date):
        super().__init__(kerdes_id, szoveg, "datum")
        self.helyes_datum = helyes_datum

    def ertekel(self, valasz: str):
        try:
            adott = datetime.date.fromisoformat(valasz.strip())
        except Exception:
            return {
                "helyes": 0,
                "pont": 0.0,
                "uzenet": "Nem megfelelő dátumformátum: éééé-hh-nn (pl. 2024-10-05).",
                "adott_datum": None,
                "elteres_nap": None,
            }

        elteres_nap = abs((adott - self.helyes_datum).days)

        if elteres_nap == 0:
            return {
                "helyes": 1,
                "pont": 1.0,
                "uzenet": "A válasz helyes!",
                "adott_datum": adott,
                "elteres_nap": 0,
            }

        if elteres_nap <= 10:
            return {
                "helyes": 0,
                "pont": 0.5,
                "uzenet": f"A válasz majdnem jó. Eltérés: {elteres_nap} nap.",
                "adott_datum": adott,
                "elteres_nap": elteres_nap,
            }

        return {
            "helyes": 0,
            "pont": 0.0,
            "uzenet": f"A válasz helytelen. Eltérés: {elteres_nap} nap.",
            "adott_datum": adott,
            "elteres_nap": elteres_nap,
        }


class ListaKerdes(Kerdes):
    def __init__(self, kerdes_id: int, szoveg: str, helyes_elemek: list[str]):
        super().__init__(kerdes_id, szoveg, "lista")
        self.helyes = {egyszerusit(x) for x in helyes_elemek}

    def ertekel(self, valasz_lista):

        if not valasz_lista:
            return {
                "helyes": 0,
                "pont": 0.0,
                "uzenet": "Nem adtál meg elemeket.",
                "adott_szoveg": "",
                "talalat_db": 0,
            }

        adott = {egyszerusit(x) for x in valasz_lista if str(x).strip() != ""}
        talalat = self.helyes & adott

        adott_szoveg = ", ".join(sorted(adott))
        talalat_db = len(talalat)

        if talalat_db == 5:
            return {
                "helyes": 1,
                "pont": 1.0,
                "uzenet": "A válasz helyes!",
                "adott_szoveg": adott_szoveg,
                "talalat_db": talalat_db,
            }

        if talalat_db >= 3:
            return {
                "helyes": 0,
                "pont": 0.5,
                "uzenet": f"A válasz majdnem helyes. Találat: {talalat_db}/5",
                "adott_szoveg": adott_szoveg,
                "talalat_db": talalat_db,
            }

        return {
            "helyes": 0,
            "pont": 0.0,
            "uzenet": f"A válasz nem jó. Találat: {talalat_db}/5",
            "adott_szoveg": adott_szoveg,
            "talalat_db": talalat_db,
        }


class FeleletValasztosKerdes(Kerdes):
    def __init__(self, kerdes_id: int, szoveg: str, opciok: list[dict]):
        super().__init__(kerdes_id, szoveg, "feleletvalasztos")
        self.opciok = opciok

    def ertekel(self, valasztott_valasz_id: int):
        try:
            valasztott_valasz_id = int(valasztott_valasz_id)
        except (TypeError, ValueError):
            return {
                "helyes": 0,
                "pont": 0.0,
                "uzenet": "Érvénytelen választás.",
                "valasztott_valasz_id": None,
            }

        valasztott = None
        for o in self.opciok:
            if o["id"] == valasztott_valasz_id:
                valasztott = o
                break

        if valasztott is None:
            return {
                "helyes": 0,
                "pont": 0.0,
                "uzenet": "Érvénytelen választás.",
                "valasztott_valasz_id": None,
            }

        if int(valasztott["helyes"]) == 1:
            return {
                "helyes": 1,
                "pont": 1.0,
                "uzenet": "A válasz helyes!",
                "valasztott_valasz_id": valasztott_valasz_id,
            }

        helyes = next((x for x in self.opciok if int(x["helyes"]) == 1), None)
        helyes_szoveg = helyes["szoveg"] if helyes else "(ismeretlen)"

        return {
            "helyes": 0,
            "pont": 0.0,
            "uzenet": f"A válasz helytelen. A helyes válasz: {helyes_szoveg}.",
            "valasztott_valasz_id": valasztott_valasz_id,
        }
