import unittest
import datetime

from kerdesek import (
    egyszerusit,
    SzamKerdes,
    DatumKerdes,
    ListaKerdes,
    FeleletValasztosKerdes,
)


class TestEgyszerusit(unittest.TestCase):
    def test_egyszerusit_levag_kisbetu_ekezet(self):
        self.assertEqual(egyszerusit("  ÁRVÍZTŰRŐ  "), "arvizturo")


class TestSzamKerdes(unittest.TestCase):
    def setUp(self):
        self.k = SzamKerdes(1, "teszt", 100)

    def test_helyes_valasz(self):
        r = self.k.ertekel(100)
        self.assertEqual(r["helyes"], 1)
        self.assertEqual(r["pont"], 1.0)
        self.assertEqual(r["adott_szam"], 100.0)
        self.assertEqual(r["elteres_szam"], 0.0)

    def test_nem_szam(self):
        r = self.k.ertekel("abc")
        self.assertEqual(r["helyes"], 0)
        self.assertEqual(r["pont"], 0.0)
        self.assertIsNone(r["adott_szam"])
        self.assertIsNone(r["elteres_szam"])

    def test_majdnem_jo_tartomany_also(self):
        r = self.k.ertekel(80)
        self.assertEqual(r["helyes"], 0)
        self.assertEqual(r["pont"], 0.5)

    def test_majdnem_jo_tartomany_felso(self):
        r = self.k.ertekel(125)
        self.assertEqual(r["helyes"], 0)
        self.assertEqual(r["pont"], 0.5)

    def test_nem_jo_kivul(self):
        r = self.k.ertekel(126)
        self.assertEqual(r["helyes"], 0)
        self.assertEqual(r["pont"], 0.0)

    def test_helyes_szam_nullaval(self):
        k0 = SzamKerdes(2, "nulla", 0)
        r1 = k0.ertekel(0)
        self.assertEqual(r1["helyes"], 1)
        self.assertEqual(r1["pont"], 1.0)

        r2 = k0.ertekel(5)
        self.assertEqual(r2["helyes"], 0)
        self.assertEqual(r2["pont"], 0.5)


class TestDatumKerdes(unittest.TestCase):
    def setUp(self):
        self.helyes = datetime.date(1969, 7, 20)
        self.k = DatumKerdes(1, "teszt", self.helyes)

    def test_helyes_datum(self):
        r = self.k.ertekel("1969-07-20")
        self.assertEqual(r["helyes"], 1)
        self.assertEqual(r["pont"], 1.0)
        self.assertEqual(r["elteres_nap"], 0)
        self.assertEqual(r["adott_datum"], self.helyes)

    def test_majdnem_jo_10_napon_belul(self):
        r = self.k.ertekel("1969-07-30")
        self.assertEqual(r["helyes"], 0)
        self.assertEqual(r["pont"], 0.5)
        self.assertEqual(r["elteres_nap"], 10)

    def test_nem_jo_10_napon_tul(self):
        r = self.k.ertekel("1969-07-31")
        self.assertEqual(r["helyes"], 0)
        self.assertEqual(r["pont"], 0.0)
        self.assertEqual(r["elteres_nap"], 11)

    def test_rossz_formatum(self):
        r = self.k.ertekel("1969/07/20")
        self.assertEqual(r["helyes"], 0)
        self.assertEqual(r["pont"], 0.0)
        self.assertIsNone(r["adott_datum"])
        self.assertIsNone(r["elteres_nap"])

    def test_strip_kezeles(self):
        r = self.k.ertekel("  1969-07-20 ")
        self.assertEqual(r["helyes"], 1)
        self.assertEqual(r["pont"], 1.0)


class TestListaKerdes(unittest.TestCase):
    def setUp(self):
        helyes = ["Jupiter", "Szaturnusz", "Uránusz", "Neptunusz", "Föld"]
        self.k = ListaKerdes(1, "teszt", helyes)

    def test_uressel(self):
        r = self.k.ertekel([])
        self.assertEqual(r["helyes"], 0)
        self.assertEqual(r["pont"], 0.0)
        self.assertEqual(r["talalat_db"], 0)

    def test_5_talalat_kulonbozo_irassal(self):
        r = self.k.ertekel(["jupiter", "SZATURNUSZ", "Uranusz", "neptunusz", "fold"])
        self.assertEqual(r["helyes"], 1)
        self.assertEqual(r["pont"], 1.0)
        self.assertEqual(r["talalat_db"], 5)

    def test_3_talalat_majdnem(self):
        r = self.k.ertekel(["Jupiter", "Szaturnusz", "Plútó", "Mars", "Neptunusz"])
        self.assertEqual(r["helyes"], 0)
        self.assertEqual(r["pont"], 0.5)
        self.assertEqual(r["talalat_db"], 3)

    def test_2_vagy_kevesebb_nem_jo(self):
        r = self.k.ertekel(["Jupiter", "Mars", "Plútó"])
        self.assertEqual(r["helyes"], 0)
        self.assertEqual(r["pont"], 0.0)
        self.assertEqual(r["talalat_db"], 1)

    def test_duplikalt_elemek_set_miatt(self):
        r = self.k.ertekel(["Jupiter", "Jupiter", "Jupiter"])
        self.assertEqual(r["talalat_db"], 1)


class TestFeleletValasztosKerdes(unittest.TestCase):
    def setUp(self):
        self.opciok = [
            {"id": 10, "szoveg": "A", "helyes": 0},
            {"id": 11, "szoveg": "B", "helyes": 1},
            {"id": 12, "szoveg": "C", "helyes": 0},
        ]
        self.k = FeleletValasztosKerdes(1, "teszt", self.opciok)

    def test_helyes_opcio(self):
        r = self.k.ertekel(11)
        self.assertEqual(r["helyes"], 1)
        self.assertEqual(r["pont"], 1.0)
        self.assertEqual(r["valasztott_valasz_id"], 11)

    def test_rossz_opcio(self):
        r = self.k.ertekel(10)
        self.assertEqual(r["helyes"], 0)
        self.assertEqual(r["pont"], 0.0)
        self.assertIn("A helyes válasz: B", r["uzenet"])

    def test_nem_letezo_id(self):
        r = self.k.ertekel(999)
        self.assertEqual(r["helyes"], 0)
        self.assertEqual(r["pont"], 0.0)
        self.assertIsNone(r["valasztott_valasz_id"])

    def test_nem_int_input(self):
        r = self.k.ertekel("abc")
        self.assertEqual(r["helyes"], 0)
        self.assertEqual(r["pont"], 0.0)
        self.assertIsNone(r["valasztott_valasz_id"])

    def test_string_szam_input(self):
        r = self.k.ertekel("11")
        self.assertEqual(r["helyes"], 1)
        self.assertEqual(r["pont"], 1.0)
        self.assertEqual(r["valasztott_valasz_id"], 11)


if __name__ == "__main__":
    unittest.main(verbosity=2)
