from django.db import models


class Kerdes(models.Model):
    id = models.AutoField(primary_key=True)
    tipus = models.CharField(max_length=20)
    szoveg = models.TextField()
    aktiv = models.IntegerField(default=1)

    helyes_szam = models.FloatField(null=True, blank=True)
    helyes_datum = models.DateField(null=True, blank=True)

    class Meta:
        db_table = "kerdes"
        managed = False

    def __str__(self):
        return f"{self.id} | {self.tipus} | {self.szoveg[:50]}"


class Valaszlehetoseg(models.Model):
    id = models.AutoField(primary_key=True)
    kerdes = models.ForeignKey(
        Kerdes,
        on_delete=models.CASCADE,
        db_column="kerdes_id",
        related_name="valaszlehetosegek",
    )
    szoveg = models.CharField(max_length=255)
    helyes = models.IntegerField(default=0)

    class Meta:
        db_table = "valaszlehetoseg"
        managed = False

    def __str__(self):
        return self.szoveg


class ListaHelyes(models.Model):
    id = models.AutoField(primary_key=True)
    kerdes = models.ForeignKey(
        Kerdes,
        on_delete=models.CASCADE,
        db_column="kerdes_id",
        related_name="lista_elemek",
    )
    elem = models.CharField(max_length=100)

    class Meta:
        db_table = "lista_helyes"
        managed = False

    def __str__(self):
        return self.elem
