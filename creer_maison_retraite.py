# coding: utf-8
import tkinter as tk
from pathlib import Path
from ttkthemes import ThemedStyle
from tkinter import ttk
from tkinter import END
import sqlite3
from files.Google import create_service

class fenetreCreationContact(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.nom_maison_retraite = str()
        self.numero_telephone_etablissement = str()
        self.adresse_postale = str()
        self.nom_cadre_sante = str()
        self.numero_telephone_cadre_sante = str()
        self.adresse_email_cadre_sante = str()
        self.nom_directeur = str()
        self.numero_telephone_directeur = str()
        self.adresse_email_directeur = str()
        self.creer_fenetre()

    def bouton_reinitialiser_token(self):
        print("test")
        print(self.entry_nom_maison_retraite.get().upper())
        print(self.entry_nom_cadre_sante.get().upper())
        print(self.entry_nom_directeur.get().upper())
        print(self.entry_numero_telephone_etablissement.get())
        pass

    def bouton_enregistrer(self):
        try:
            self.nom_maison_retraite = "MR " + self.entry_nom_maison_retraite.get().upper()
            self.nom_cadre_sante = "CDS " + self.entry_nom_cadre_sante.get().upper()
            self.nom_directeur = "DIR " + self.entry_nom_directeur.get().upper()
            self.numero_telephone_etablissement = self.entry_numero_telephone_etablissement.get()
            self.numero_telephone_cadre_sante = self.entry_numero_telephone_cadre_sante.get()
            self.numero_telephone_directeur = self.entry_numero_telephone_directeur.get()
            self.adresse_postale = self.entry_adresse_postale.get()
            self.adresse_email_cadre_sante = self.entry_adresse_email_cadre_sante.get()
            self.adresse_email_directeur = self.entry_adresse_email_directeur.get()
        except:
            print("Erreur d'enregistrement dans la classe")

        # On enregistre dans la base de donnée
        """
        try:
            connection = sqlite3.connect(Path("files", "files/test3.db"))
            cursor_maison_retraite = connection.cursor()
            cursor_referent = connection.cursor()
            db_maison_retraite = (cur    sor_maison_retraite.lastrowid, self.nom_maison_retraite, self.adresse_postale)
            cursor_maison_retraite.execute('INSERT INTO INFO_MAISON_RETRAITE VALUES(?,?,?)', db_maison_retraite)
            id_maison_retraite = cursor_maison_retraite.lastrowid

            db_referent = (cursor_referent.lastrowid, id_maison_retraite, 2, self.nom_cadre_sante, "", "",
                           self.numero_telephone, self.adresse_email)
            cursor_referent.execute('INSERT INTO INFO_HUMAIN VALUES(?,?,?,?,?,?,?,?)', db_referent)
            id_referent = cursor_referent.lastrowid
            connection.commit()
            connection.close()
            print("enregistrement réussi")
        except Exception as e:
            print("erreur enregistrment base de donnée", e)
            connection.rollback()
            connection.close()
        """

        # On enregistre le contact sur google contacts
        # Paramètres d'authentification
        CLIENT_SECRET_FILE = Path("tolkienetjason", "client_creercontact.json")
        API_NAME = 'people'
        API_VERSION = 'v1'
        SCOPES = ['https://www.googleapis.com/auth/contacts']

        # Appel de la fonction d'authentification
        service = create_service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

        prebody = {}
        prebody["organizations"] = [{'name': self.nom_maison_retraite}]
        prebody["memberships"] = [{'contactGroupMembership': {
            "contactGroupResourceName": "contactGroups/1c576d7f8bd43294"}}]
        prebody["addresses"] = [{'formattedValue': f"{self.adresse_postale}"}]
        if self.numero_telephone_cadre_sante == "" and self.numero_telephone_directeur == "" and self.nom_cadre_sante != "" and self.nom_directeur != "":
            prebody["phoneNumbers"] = [
                {'value': f"{self.numero_telephone_etablissement}", 'type': f"Acceuil Etablissement"},
                {'value': f"no num", 'type': f"{self.nom_cadre_sante}"},
                {'value': f"no num", 'type': f"{self.nom_directeur}"}]
            prebody["emailAddresses"] = [
                {'value': f"{self.adresse_email_cadre_sante}", 'type': f"{self.adresse_email_cadre_sante}"},
                {'value': f"{self.adresse_email_directeur}", 'type': f"{self.adresse_email_directeur}"}]

        elif self.numero_telephone_cadre_sante == "" and self.nom_cadre_sante != "":
            prebody["phoneNumbers"] = [
                {'value': f"{self.numero_telephone_etablissement}", 'type': f"Acceuil Etablissement"},
                {'value': f"no num", 'type': f"{self.nom_cadre_sante}"},
                {'value': f"{self.numero_telephone_directeur}", 'type': f"{self.nom_directeur}"}]
            prebody["emailAddresses"] = [
                {'value': f"{self.adresse_email_cadre_sante}", 'type': f"{self.adresse_email_cadre_sante}"},
                {'value': f"{self.adresse_email_directeur}", 'type': f"{self.adresse_email_directeur}"}]

        elif self.numero_telephone_directeur == "" and self.nom_directeur != "":
            prebody["phoneNumbers"] = [
                {'value': f"{self.numero_telephone_etablissement}", 'type': f"Acceuil Etablissement"},
                {'value': f"{self.numero_telephone_cadre_sante}", 'type': f"{self.nom_cadre_sante}"},
                {'value': f"no num", 'type': f"{self.nom_directeur}"}]
            prebody["emailAddresses"] = [
                {'value': f"{self.adresse_email_cadre_sante}", 'type': f"{self.adresse_email_cadre_sante}"},
                {'value': f"{self.adresse_email_directeur}", 'type': f"{self.adresse_email_directeur}"}]
        else:
            prebody["phoneNumbers"] = [
                {'value': f"{self.numero_telephone_etablissement}", 'type': f"Acceuil Etablissement"},
                {'value': f"{self.numero_telephone_cadre_sante}", 'type': f"{self.nom_cadre_sante}"},
                {'value': f"{self.numero_telephone_directeur}", 'type': f"{self.nom_directeur}"}]
            prebody["emailAddresses"] = [
                {'value': f"{self.adresse_email_cadre_sante}", 'type': f"{self.adresse_email_cadre_sante}"},
                {'value': f"{self.adresse_email_directeur}", 'type': f"{self.adresse_email_directeur}"}]

        service.people().createContact(body=prebody).execute()


        # On efface les entrées pour eviter les doublons
        self.entry_nom_maison_retraite.delete(0, END)
        self.entry_numero_telephone_etablissement.delete(0, END)
        self.entry_adresse_postale.delete(0, END)
        self.entry_nom_cadre_sante.delete(0, END)
        self.entry_numero_telephone_cadre_sante.delete(0, END)
        self.entry_adresse_email_cadre_sante.delete(0, END)
        self.entry_nom_directeur.delete(0, END)
        self.entry_numero_telephone_directeur.delete(0, END)
        self.entry_adresse_email_directeur.delete(0, END)

    def bouton_effacer(self):
        self.entry_nom_maison_retraite.delete(0, END)
        self.entry_numero_telephone_etablissement.delete(0, END)
        self.entry_adresse_postale.delete(0, END)
        self.entry_nom_cadre_sante.delete(0, END)
        self.entry_numero_telephone_cadre_sante.delete(0, END)
        self.entry_adresse_email_cadre_sante.delete(0, END)
        self.entry_nom_directeur.delete(0, END)
        self.entry_numero_telephone_directeur.delete(0, END)
        self.entry_adresse_email_directeur.delete(0, END)

    def creer_fenetre(self):
        # Theme fenetre
        #self.title(bg = "white")
        style = ThemedStyle(self)
        style.theme_use('equilux')
        bg = style.lookup('TLabel', 'background')
        fg = style.lookup('TLabel', 'foreground')
        self.configure(bg=style.lookup('TLabel', 'background'))
        self.title("Panneau d'enregistrment des maisons de retraite")

        label_nom_maison_retraite = ttk.Label(self, text="Nom de la maison de retraite :")
        label_adresse_postale = ttk.Label(self, text="Adresse de la maison de retraite")
        label_numero_telephone_etablissement = ttk.Label(self, text="Téléphone établissement")
        label_nom_cadre_sante = ttk.Label(self, text="Nom cadre santé")
        label_numero_telephone_cadre_sante = ttk.Label(self, text="Numéro de téléphone")
        label_adresse_email_cadre_sante = ttk.Label(self, text="Adresse E-mail cadre santé")
        label_nom_directeur = ttk.Label(self, text="Nom directeur")
        label_numero_telephone_directeur = ttk.Label(self, text="Numéro de téléphone")
        label_adresse_email_directeur = ttk.Label(self, text="Adresse E-mail directeur")

        self.entry_nom_maison_retraite = ttk.Entry(self, width=50)
        self.entry_adresse_postale = ttk.Entry(self, width=50)
        self.entry_numero_telephone_etablissement = ttk.Entry(self, width=50)
        self.entry_nom_cadre_sante = ttk.Entry(self, width=50)
        self.entry_numero_telephone_cadre_sante = ttk.Entry(self, width=50)
        self.entry_adresse_email_cadre_sante = ttk.Entry(self, width=50)
        self.entry_nom_directeur = ttk.Entry(self, width=50)
        self.entry_numero_telephone_directeur = ttk.Entry(self, width=50)
        self.entry_adresse_email_directeur = ttk.Entry(self, width=50)

        bouton_effacer = ttk.Button(self, text="EFFACER", command=self.bouton_effacer)
        bouton_enregistrer = ttk.Button(self, text="ENREGISTRER", command=self.bouton_enregistrer)
        bouton_reinitialiser_token = ttk.Button(self, text="Effacer Token", command=self.bouton_reinitialiser_token)

        label_nom_maison_retraite.grid(row=0, column=0)
        label_adresse_postale.grid(row=1, column=0)
        label_numero_telephone_etablissement.grid(row=2, column=0)
        label_nom_cadre_sante.grid(row=3, column=0)
        label_numero_telephone_cadre_sante.grid(row=4, column=0)
        label_adresse_email_cadre_sante.grid(row=5, column=0)
        label_nom_directeur.grid(row=6, column=0)
        label_numero_telephone_directeur.grid(row=7, column=0)
        label_adresse_email_directeur.grid(row=8, column=0)

        self.entry_nom_maison_retraite.grid(row=0, column=1)
        self.entry_adresse_postale.grid(row=1, column=1)
        self.entry_numero_telephone_etablissement.grid(row=2, column=1)
        self.entry_nom_cadre_sante.grid(row=3, column=1)
        self.entry_numero_telephone_cadre_sante.grid(row=4, column=1)
        self.entry_adresse_email_cadre_sante.grid(row=5, column=1)
        self.entry_nom_directeur.grid(row=6, column=1)
        self.entry_numero_telephone_directeur.grid(row=7, column=1)
        self.entry_adresse_email_directeur.grid(row=8, column=1)

        bouton_effacer.grid(row=9, column=0)
        bouton_enregistrer.grid(row=9, column=1)
        bouton_reinitialiser_token.grid(row=10, column=0)


albert = fenetreCreationContact()
albert.mainloop()



