import pickle
import os
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request
import datetime
from pathlib import Path
#from odikev import MaisonRetraite

# Module d'identification API GOOGLE
def create_service(client_secret_file, api_name, api_version, *scopes):
    print(client_secret_file, api_name, api_version, scopes, sep='-')
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]
    print(SCOPES)

    cred = None

    pickle_file = Path("tolkienetjason", f'token_{API_SERVICE_NAME}_{API_VERSION}.pickle')
    # print(pickle_file)

    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            cred = flow.run_local_server()

        with open(pickle_file, 'wb') as token:
            pickle.dump(cred, token)

    
    service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
    print(API_SERVICE_NAME, 'service created successfully')
    return service


# Enregistrment API GOOGLE PEOPLE
def enregistrement_google_people(info: list):
    nom_maison_retraite = "Mr " + info[0].upper()
    adresse_postale = info[1]
    numero_telephone_etablissement = info[2]
    nom_cadre_sante = "CDS " + info[3].upper()
    numero_telephone_cadre_sante = info[4]
    adresse_email_cadre_sante = info[5]
    nom_directeur = "DIR " + info[6].upper()
    numero_telephone_directeur = info[7]
    adresse_email_directeur = info[8]

    # On enregistre le contact sur google contacts
    # Paramètres d'authentification
    CLIENT_SECRET_FILE = Path("tolkienetjason", "client_creercontact.json")
    API_NAME = 'people'
    API_VERSION = 'v1'
    SCOPES = ['https://www.googleapis.com/auth/contacts']

    # Appel de la fonction d'authentification
    service = create_service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    prebody = {}
    prebody["names"] = [{'givenName': nom_maison_retraite}]
    prebody["organizations"] = [{'name': nom_maison_retraite}]
    prebody["memberships"] = [{'contactGroupMembership': {
        "contactGroupResourceName": "contactGroups/1c576d7f8bd43294"}}]
    prebody["addresses"] = [{'formattedValue': f"{adresse_postale}"}]
    if numero_telephone_cadre_sante == "" and numero_telephone_directeur == "" and nom_cadre_sante != "" and nom_directeur != "":
        prebody["phoneNumbers"] = [
            {'value': f"{numero_telephone_etablissement}", 'type': f"Acceuil Etablissement"},
            {'value': f"no num", 'type': f"{nom_cadre_sante}"},
            {'value': f"no num", 'type': f"{nom_directeur}"}]
        prebody["emailAddresses"] = [
            {'value': f"{adresse_email_cadre_sante}", 'type': f"{adresse_email_cadre_sante}"},
            {'value': f"{adresse_email_directeur}", 'type': f"{adresse_email_directeur}"}]

    elif numero_telephone_cadre_sante == "" and nom_cadre_sante != "":
        prebody["phoneNumbers"] = [
            {'value': f"{numero_telephone_etablissement}", 'type': f"Acceuil Etablissement"},
            {'value': f"no num", 'type': f"{nom_cadre_sante}"},
            {'value': f"{numero_telephone_directeur}", 'type': f"{nom_directeur}"}]
        prebody["emailAddresses"] = [
            {'value': f"{adresse_email_cadre_sante}", 'type': f"{adresse_email_cadre_sante}"},
            {'value': f"{adresse_email_directeur}", 'type': f"{adresse_email_directeur}"}]

    elif numero_telephone_directeur == "" and nom_directeur != "":
        prebody["phoneNumbers"] = [
            {'value': f"{numero_telephone_etablissement}", 'type': f"Acceuil Etablissement"},
            {'value': f"{numero_telephone_cadre_sante}", 'type': f"{nom_cadre_sante}"},
            {'value': f"no num", 'type': f"{nom_directeur}"}]
        prebody["emailAddresses"] = [
            {'value': f"{adresse_email_cadre_sante}", 'type': f"{adresse_email_cadre_sante}"},
            {'value': f"{adresse_email_directeur}", 'type': f"{adresse_email_directeur}"}]
    else:
        prebody["phoneNumbers"] = [
            {'value': f"{numero_telephone_etablissement}", 'type': f"Acceuil Etablissement"},
            {'value': f"{numero_telephone_cadre_sante}", 'type': f"{nom_cadre_sante}"},
            {'value': f"{numero_telephone_directeur}", 'type': f"{nom_directeur}"}]
        prebody["emailAddresses"] = [
            {'value': f"{adresse_email_cadre_sante}", 'type': f"{adresse_email_cadre_sante}"},
            {'value': f"{adresse_email_directeur}", 'type': f"{adresse_email_directeur}"}]

    service.people().createContact(body=prebody).execute()

# Enregistrement base de donnée
def enregistrement_database(info: list, db, form):
    nom_maison_retraite = "Mr " + info[0].upper()
    adresse_maison_retraite = info[1]
    telephone_maison_retraite = info[2]
    nom_cadre_sante = info[3].upper()
    telephone_cadre_sante = info[4]
    email_cadre_sante = info[5]
    nom_directeur = info[6].upper()
    telephone_directeur = info[7]
    email_directeur = info[8]
    unemaisonretraite = form(nom_maison_retraite=nom_maison_retraite,
                                       adresse_maison_retraite=adresse_maison_retraite,
                                       telephone_maison_retraite=telephone_maison_retraite,
                                       nom_cadre_sante=nom_cadre_sante,
                                       telephone_cadre_sante=telephone_cadre_sante,
                                       email_cadre_sante=email_cadre_sante,
                                       nom_directeur=nom_directeur,
                                       telephone_directeur=telephone_directeur,
                                       email_directeur=email_directeur
                                       )
    db.session.add(unemaisonretraite)
    db.session.commit()
    return 0
    
