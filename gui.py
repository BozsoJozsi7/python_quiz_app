import tkinter as tk
from tkinter import messagebox

import adatbazis
import kerdes_gyar


class KvizAblak:
    def __init__(self):
        self.ablak = tk.Tk()
        self.ablak.title("Kvíz")

        self.kapcsolat = None
        self.futas_id = None
        self.kerdesek = []
        self.aktualis_index = 0
        self.ossz_pont = 0.0

        self.valasztott_valasz_id_var = tk.IntVar(value=0)
        self.aktualis_tipus = None

        self.felso = tk.Frame(self.ablak)
        tk.Button(self.felso, text="Kilépés", command=self.ablak.destroy).pack(
            side=tk.RIGHT
        )
        self.felso.pack(fill=tk.X, padx=5, pady=5)

        self.start_frame = tk.Frame(self.ablak)
        self.kerdes_frame = tk.Frame(self.ablak)
        self.eredmeny_frame = tk.Frame(self.ablak)

        self._start_nezet_felepit()
        self._kerdes_nezet_felepit()
        self._eredmeny_nezet_felepit()

        self.start_nezet_mutat()

    def _start_nezet_felepit(self):
        tk.Label(self.start_frame, text="Add meg a neved:").pack(pady=5)
        self.nev_entry = tk.Entry(self.start_frame, width=30)
        self.nev_entry.pack(pady=5)
        tk.Button(self.start_frame, text="Start", command=self.start).pack(pady=10)

    def _kerdes_nezet_felepit(self):
        self.kerdes_szoveg = tk.Label(
            self.kerdes_frame, text="", wraplength=500, justify="left"
        )
        self.kerdes_szoveg.pack(pady=10)

        self.valasz_terulet = tk.Frame(self.kerdes_frame)
        self.valasz_terulet.pack(pady=10)

        self.visszajelzes = tk.Label(self.kerdes_frame, text="")
        self.visszajelzes.pack(pady=5)

        tk.Button(self.kerdes_frame, text="Következő", command=self.kovetkezo).pack(
            pady=10
        )

    def _eredmeny_nezet_felepit(self):
        self.eredmeny_label = tk.Label(self.eredmeny_frame, text="", font=("Arial", 14))
        self.eredmeny_label.pack(pady=20)
        tk.Button(self.eredmeny_frame, text="Kilépés", command=self.ablak.destroy).pack(
            pady=10
        )

    def start_nezet_mutat(self):
        self.kerdes_frame.pack_forget()
        self.eredmeny_frame.pack_forget()
        self.start_frame.pack(padx=10, pady=10)

    def kerdes_nezet_mutat(self):
        self.start_frame.pack_forget()
        self.eredmeny_frame.pack_forget()
        self.kerdes_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    def eredmeny_nezet_mutat(self):
        self.start_frame.pack_forget()
        self.kerdes_frame.pack_forget()
        self.eredmeny_frame.pack(padx=10, pady=10)

    def start(self):
        nev = self.nev_entry.get().strip()
        if not nev:
            messagebox.showerror("Hiba", "Add meg a neved!")
            return

        try:
            self.kapcsolat = adatbazis.adatbazis_kapcsolat()
            self.futas_id = adatbazis.futas_letrehozasa(self.kapcsolat, nev)
            self.kerdesek = kerdes_gyar.kerdesek_betoltese_adatbazisbol(self.kapcsolat)
        except Exception as e:
            messagebox.showerror("Hiba", str(e))
            return

        if not self.kerdesek:
            messagebox.showerror("Hiba", "Nincsenek aktív kérdések az adatbázisban")
            return

        self.aktualis_index = 0
        self.ossz_pont = 0.0
        self.kerdes_nezet_mutat()
        self.kerdes_megjelenit()

    def kerdes_megjelenit(self):
        for w in self.valasz_terulet.winfo_children():
            w.destroy()

        self.visszajelzes.config(text="")

        kerdes = self.kerdesek[self.aktualis_index]
        self.kerdes_szoveg.config(text=kerdes.szoveg)

        if kerdes.tipus == "feleletvalasztos":
            self._feleletvalasztos_megjelenit(kerdes)

        elif kerdes.tipus == "szam":
            self._szam_megjelenit(kerdes)

        elif kerdes.tipus == "datum":
            self._datum_megjelenit(kerdes)

        elif kerdes.tipus == "lista":
            self._lista_megjelenit(kerdes)

        else:
            tk.Label(
                self.valasz_terulet, text=f"(TODO válaszmező: {kerdes.tipus})"
            ).pack()

    def _feleletvalasztos_megjelenit(self, kerdes):
        self.valasztott_valasz_id_var.set(0)

        for opcio in kerdes.opciok:
            tk.Radiobutton(
                self.valasz_terulet,
                text=opcio["szoveg"],
                variable=self.valasztott_valasz_id_var,
                value=opcio["id"],
                anchor="w",
                justify="left",
            ).pack(fill=tk.X, pady=2)

    def _szam_megjelenit(self, kerdes):
        tk.Label(self.valasz_terulet, text="Válasz (szám):").pack(anchor="w")

        self.szam_entry = tk.Entry(self.valasz_terulet, width=20)
        self.szam_entry.pack(anchor="w", pady=5)

        self.szam_entry.focus_set()

    def _datum_megjelenit(self, kerdes):
        tk.Label(self.valasz_terulet, text="Válasz (éééé-hh-nn):").pack(anchor="w")

        self.datum_entry = tk.Entry(self.valasz_terulet, width=20)
        self.datum_entry.pack(anchor="w", pady=5)

        self.visszajelzes.config(text="Példa: 1935-10-25")

        self.datum_entry.focus_set()

    def _lista_megjelenit(self, kerdes):
        tk.Label(
            self.valasz_terulet,
            text="Adj meg legfeljebb 5 elemet (egy sor = egy elem):",
        ).pack(anchor="w")

        self.lista_entryk = []

        for i in range(5):
            e = tk.Entry(self.valasz_terulet, width=30)
            e.pack(anchor="w", pady=2)
            self.lista_entryk.append(e)

        self.lista_entryk[0].focus_set()

    def kovetkezo(self):
        kerdes = self.kerdesek[self.aktualis_index]

        if kerdes.tipus == "feleletvalasztos":
            valasztott_id = self.valasztott_valasz_id_var.get()
            if valasztott_id == 0:
                messagebox.showerror("Hiba", "Válassz egy opciót!")
                return

            eredmeny = kerdes.ertekel(valasztott_id)

            adatbazis.valasz_mentese(
                self.kapcsolat,
                futas_id=self.futas_id,
                kerdes_id=kerdes.kerdes_id,
                valasztott_valasz_id=eredmeny.get("valasztott_valasz_id"),
                adott_szoveg=None,
                adott_szam=None,
                adott_datum=None,
                helyes=eredmeny["helyes"],
                pont=eredmeny["pont"],
                elteres_szam=None,
                elteres_nap=None,
            )

            self.ossz_pont += float(eredmeny["pont"])
            self.visszajelzes.config(text=eredmeny["uzenet"])

            self.ablak.after(2000, self._kovetkezo_kerdesre_lep)

        elif kerdes.tipus == "szam":
            szoveg = self.szam_entry.get().strip()

            try:
                adott_szam = float(szoveg)
            except (TypeError, ValueError):
                messagebox.showerror("Hiba", "Számot kellett volna beírni")
                return

            eredmeny = kerdes.ertekel(adott_szam)

            adatbazis.valasz_mentese(
                self.kapcsolat,
                futas_id=self.futas_id,
                kerdes_id=kerdes.kerdes_id,
                valasztott_valasz_id=None,
                adott_szoveg=None,
                adott_szam=eredmeny.get("adott_szam"),
                adott_datum=None,
                helyes=eredmeny["helyes"],
                pont=eredmeny["pont"],
                elteres_szam=eredmeny.get("elteres_szam"),
                elteres_nap=None,
            )

            self.ossz_pont += float(eredmeny["pont"])
            self.visszajelzes.config(text=eredmeny["uzenet"])

            self.ablak.after(2000, self._kovetkezo_kerdesre_lep)

        elif kerdes.tipus == "datum":
            szoveg = self.datum_entry.get().strip()

            if szoveg == "":
                messagebox.showerror("Hiba", "Add meg a dátumot (éééé-hh-nn)!")
                return

            eredmeny = kerdes.ertekel(szoveg)

            if eredmeny.get("adott_datum") is None:
                messagebox.showerror("Hiba", eredmeny["uzenet"])
                return

            adatbazis.valasz_mentese(
                self.kapcsolat,
                futas_id=self.futas_id,
                kerdes_id=kerdes.kerdes_id,
                valasztott_valasz_id=None,
                adott_szoveg=None,
                adott_szam=None,
                adott_datum=eredmeny.get("adott_datum"),
                helyes=eredmeny["helyes"],
                pont=eredmeny["pont"],
                elteres_szam=None,
                elteres_nap=eredmeny.get("elteres_nap"),
            )

            self.ossz_pont += float(eredmeny["pont"])
            self.visszajelzes.config(text=eredmeny["uzenet"])

            self.ablak.after(2000, self._kovetkezo_kerdesre_lep)

        elif kerdes.tipus == "lista":
            valasz_lista = [
                e.get().strip() for e in self.lista_entryk if e.get().strip() != ""
            ]

            if not valasz_lista:
                messagebox.showerror("Hiba", "Adj meg legalább egy elemet!")
                return

            eredmeny = kerdes.ertekel(valasz_lista)

            adatbazis.valasz_mentese(
                self.kapcsolat,
                futas_id=self.futas_id,
                kerdes_id=kerdes.kerdes_id,
                valasztott_valasz_id=None,
                adott_szoveg=", ".join(valasz_lista),
                adott_szam=None,
                adott_datum=None,
                helyes=eredmeny["helyes"],
                pont=eredmeny["pont"],
                elteres_szam=None,
                elteres_nap=None,
            )

            self.ossz_pont += float(eredmeny["pont"])
            self.visszajelzes.config(text=eredmeny["uzenet"])

            self.ablak.after(2000, self._kovetkezo_kerdesre_lep)

        else:
            messagebox.showinfo(
                "Info", f"Ezt a típust még nem kötöttük rá: {kerdes.tipus}"
            )

    def _kovetkezo_kerdesre_lep(self):
        self.aktualis_index += 1

        if self.aktualis_index >= len(self.kerdesek):
            max_pont = len(self.kerdesek)
            szazalek = (self.ossz_pont / max_pont) * 100 if max_pont else 0
            self.eredmeny_label.config(
                text=f"Vége!\nPont: {self.ossz_pont}/{max_pont}\n{szazalek:.1f}%"
            )
            self.eredmeny_nezet_mutat()
            if self.kapcsolat:
                self.kapcsolat.close()
            return

        self.kerdes_megjelenit()

    def fut(self):
        self.ablak.mainloop()


if __name__ == "__main__":
    KvizAblak().fut()
