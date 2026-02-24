from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse

from kviz_admin.models import Kerdes, ListaHelyes, Valaszlehetoseg


def _float_vagy_none(szoveg):

    if szoveg in (None, ""):
        return None
    try:
        return float(szoveg)
    except ValueError:
        return None


def index(request):
    kerdesek = Kerdes.objects.all().order_by("id")
    valaszok = Valaszlehetoseg.objects.all().order_by("kerdes", "id")
    lista_elemek = ListaHelyes.objects.all().order_by("kerdes", "id")

    return HttpResponse(
        loader.get_template("index.html").render(
            {
                "kerdesek": kerdesek,
                "valaszok": valaszok,
                "lista_elemek": lista_elemek,
            },
            request,
        )
    )


def add_kerdes(request):
    return HttpResponse(
        loader.get_template("kerdes.html").render({"mod": "add"}, request)
    )


def add_kerdes_record(request):
    tipus = request.POST.get("tipus") or ""
    szoveg = request.POST.get("szoveg") or ""
    aktiv = 1 if request.POST.get("aktiv") == "on" else 0

    helyes_szam = _float_vagy_none(request.POST.get("helyes_szam"))
    helyes_datum = request.POST.get("helyes_datum") or None

    Kerdes(
        tipus=tipus,
        szoveg=szoveg,
        aktiv=aktiv,
        helyes_szam=helyes_szam,
        helyes_datum=helyes_datum,
    ).save()

    return HttpResponseRedirect(reverse("index"))


def update_kerdes(request, id):
    return HttpResponse(
        loader.get_template("kerdes.html").render(
            {"mod": "update", "kerdes": Kerdes.objects.get(id=id)},
            request,
        )
    )


def update_kerdes_record(request, id):
    k = Kerdes.objects.get(id=id)
    k.tipus = request.POST.get("tipus") or k.tipus
    k.szoveg = request.POST.get("szoveg") or k.szoveg
    k.aktiv = 1 if request.POST.get("aktiv") == "on" else 0

    k.helyes_szam = _float_vagy_none(request.POST.get("helyes_szam"))
    helyes_datum = request.POST.get("helyes_datum")
    k.helyes_datum = helyes_datum if (helyes_datum not in (None, "")) else None

    k.save()
    return HttpResponseRedirect(reverse("index"))


def delete_kerdes(request, id):
    Kerdes.objects.get(id=id).delete()
    return HttpResponseRedirect(reverse("index"))


def add_valasz(request, kerdes_id):
    return HttpResponse(
        loader.get_template("valasz.html").render(
            {"mod": "add", "kerdes": Kerdes.objects.get(id=kerdes_id)},
            request,
        )
    )


def add_valasz_record(request, kerdes_id):
    szoveg = request.POST.get("szoveg") or ""
    helyes = 1 if request.POST.get("helyes") == "on" else 0

    if helyes == 1:
        Valaszlehetoseg.objects.filter(kerdes_id=kerdes_id).update(helyes=0)

    Valaszlehetoseg(
        kerdes=Kerdes.objects.get(id=kerdes_id),
        szoveg=szoveg,
        helyes=helyes,
    ).save()

    return HttpResponseRedirect(reverse("index"))


def update_valasz(request, id):
    v = Valaszlehetoseg.objects.get(id=id)
    return HttpResponse(
        loader.get_template("valasz.html").render(
            {"mod": "update", "valasz": v, "kerdes": v.kerdes},
            request,
        )
    )


def update_valasz_record(request, id):
    v = Valaszlehetoseg.objects.get(id=id)
    v.szoveg = request.POST.get("szoveg") or v.szoveg
    helyes = 1 if request.POST.get("helyes") == "on" else 0

    if helyes == 1:
        Valaszlehetoseg.objects.filter(kerdes_id=v.kerdes_id).update(helyes=0)

    v.helyes = helyes
    v.save()
    return HttpResponseRedirect(reverse("index"))


def delete_valasz(request, id):
    Valaszlehetoseg.objects.get(id=id).delete()
    return HttpResponseRedirect(reverse("index"))


def add_listaelem(request, kerdes_id):
    return HttpResponse(
        loader.get_template("listaelem.html").render(
            {"kerdes": Kerdes.objects.get(id=kerdes_id)},
            request,
        )
    )


def add_listaelem_record(request, kerdes_id):
    elem = request.POST.get("elem") or ""
    if elem.strip() != "":
        ListaHelyes(kerdes=Kerdes.objects.get(id=kerdes_id), elem=elem.strip()).save()
    return HttpResponseRedirect(reverse("index"))


def delete_listaelem(request, id):
    ListaHelyes.objects.get(id=id).delete()
    return HttpResponseRedirect(reverse("index"))
