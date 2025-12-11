import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import scrolledtext
import re

cle=["DTSTART","DTEND","SUMMARY","LOCATION"]

def lire_ics(fichier):
    with open(fichier, "r", encoding="utf-8") as f:
        contenu = f.readlines()
    return [ligne.strip() for ligne in contenu]

def extraire_valeur(lignes, cle):
    for ligne in lignes:
        if ligne.startswith(cle):
            return ligne.split(":", 1)[1]
    return None

def convertir_date_heure(ics_datetime):
    annee = ics_datetime[0:4]
    mois = ics_datetime[4:6]
    jour = ics_datetime[6:8]
    heure = ics_datetime[9:11]
    minute = ics_datetime[11:13]
    return f"{jour}-{mois}-{annee}", f"{heure}:{minute}"

def calculer_duree(dtstart, dtend):
    from datetime import datetime

    fmt = "%Y%m%dT%H%M%S"
    debut = datetime.strptime(dtstart.replace("Z",""), fmt)
    fin = datetime.strptime(dtend.replace("Z",""), fmt)
    diff = fin - debut
    heures, reste = divmod(diff.seconds, 3600)
    minutes = reste // 60
    return f"{heures:02d}:{minutes:02d}"

def programme1(fichier):
    lignes = lire_ics(fichier)

    uid = extraire_valeur(lignes, "UID")
    dtstart = extraire_valeur(lignes, "DTSTART")
    dtend = extraire_valeur(lignes, "DTEND")
    summary = extraire_valeur(lignes, "SUMMARY")
    location = extraire_valeur(lignes, "LOCATION")
    profs = extraire_valeur(lignes, "DESCRIPTION") 
    date, heure = convertir_date_heure(dtstart)
    duree = calculer_duree(dtstart, dtend)
    modalite = "CM" if "CM" in summary else "TD"

    pseudo_csv = f"{uid};{date};{heure};{duree};{modalite};{summary};{location};{profs};S1"
    return pseudo_csv

def choisir_fichier():
    fichier = filedialog.askopenfilename(
        title="Sélectionner un fichies",
        filetypes=[("Fichier", "*.ics")]
    )
    if fichier:
        try:
            result = programme1(fichier)
            zone_resultat.delete(1.0, tk.END)
            zone_resultat.insert(tk.END, result)
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de lire le fichier : {e}")

fenetre = tk.Tk()
fenetre.title("Convertisseur")
fenetre.geometry("700x400")
lbl = tk.Label(fenetre, text="Choisissez un fichier .ics à convertir :", font=("Arial", 10))
lbl.pack(pady=10)

btn = tk.Button(fenetre, text="Choisir un fichier", font=("Arial", 12), command=choisir_fichier)
btn.pack(pady=10)

zone_resultat = scrolledtext.ScrolledText(fenetre, width=140, height=30, font=("Courier", 0))
zone_resultat.pack(pady=10)

fenetre.mainloop()
