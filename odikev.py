from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField
from wtforms.validators import DataRequired, Email
from flask_sqlalchemy import SQLAlchemy
from fonctionannexes import enregistrement_google_people
from fonctionannexes import enregistrement_database
import os
import sqlalchemy
from sqlalchemy.orm import scoped_session, sessionmaker
from datetime import datetime

# Initialisation du framework Flask
app = Flask(__name__)

# Chargement de la base de donnée
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Users\Kevin\\SynologyDrive\\Docs\CommondB\\db5-29-03.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialisation de la clef secrete pour sécuriser la communication entre backend et fontend
app.config['SECRET_KEY'] = "jackstone"

# Initialisation de SQLalchemy et traitement de la base de donnée objet
db = SQLAlchemy(app)


# TEST compréhension suite


# Création des modèles de tables avec SQLAlchemy
class MaisonRetraite(db.Model):
    __tablename__ = 'maison_retraite'
    id_maison_retraite = db.Column(db.Integer, primary_key=True)
    nom_maison_retraite = db.Column(db.String(100), nullable=False)
    adresse_maison_retraite = db.Column(db.String(100), nullable=False)
    telephone_maison_retraite = db.Column(db.String(100))
    nom_cadre_sante = db.Column(db.String(100))
    telephone_cadre_sante = db.Column(db.String(100))
    email_cadre_sante = db.Column(db.String(100))
    nom_directeur = db.Column(db.String(100))
    telephone_directeur = db.Column(db.String(100))
    email_directeur = db.Column(db.String(100))
    #id_cadre_sante = db.Column(db.Integer, db.ForeignKey('Personne.id_personne'))
    #id_directeur = db.Column(db.Integer, db.ForeignKey('Personne.id_personne'))
    #cadre_sante = db.relationship("Personne", foreign_keys=[id_cadre_sante], back_populates="cadre_sante_mr")
    #directeur = db.relationship("Personne", foreign_keys=[id_directeur], back_populates="directeur_mr")


    # Create A String
    def __repr__(self):
        return '<ADRESSE_MAISON_RETRAITE %r>' % self.ADRESSE_MAISON_RETRAITE
        return '<INFO_MAISON_RETRAITE %r>' % self.NOM_MAISON_RETRAITE


class FichePatient(db.Model):
    __tablename__ = 'fiche_patient'
    id_fiche_patient = db.Column(db.Integer, primary_key=True)
    id_statut_actuel = db.Column(db.Integer)
    id_maison_retraite = db.Column(db.Integer)
    date_depistage = db.Column(db.String(100))
    date_acceptation = db.Column(db.String(100))
    date_commande_embout = db.Column(db.String(100))
    date_reception_embout = db.Column(db.String(100))
    date_adaptation_appareillage = db.Column(db.String(100))
    date_facturation = db.Column(db.String(100))
    nom_patient = db.Column(db.String(100))
    prenom_patient = db.Column(db.String(100))
    telephone_patient = db.Column(db.String(100))
    email_patient = db.Column(db.String(100))
    conseil_appareillage_od = db.Column(db.String(100))
    conseil_appareillage_og = db.Column(db.String(100))
    couplage_od = db.Column(db.String(100))
    couplage_og = db.Column(db.String(100))

"""
class Personne(db.Model):
    __tablename__ = 'personne'
    id_personne = db.Column(db.Integer, primary_key=True)
    id_type_personne = db.Column(db.Integer, db.ForeignKey('type_personne_tablesecondaire.id_type_personne'),
                                 nullable=False)
    type = db.relationship("TypePersonne")
    nom_personne = db.Column(db.Integer, nullable=False)
    prenom_personne = db.Column(db.String(100), nullable=False)
    sexe_personne = db.Column(db.String(100))
    telephone_personne = db.Column(db.String(100))
    email_personne = db.Column(db.String(100), nullable=False)

    cadre_sante_mr = db.relationship('MaisonRetraite', foreign_keys='MaisonRetraite.id_cadre_sante', back_populates="cadre_sante", cascade="all, delete")
    directeur_mr = db.relationship('MaisonRetraite', foreign_keys='MaisonRetraite.id_directeur', back_populates="directeur", cascade="all, delete")
    #maisonretraite = db.relationship("MaisonRetraite", backref='MaisonRetraite')

class TypePersonne(db.Model):
    __tablename__ = 'type_personne_tablesecondaire'
    id_type_personne = db.Column(db.Integer, primary_key=True)
    type_personne = db.Column(db.String(100), nullable=False)
"""

"""
untype = TypePersonne(type_personne="test")
db.session.add(untype)
db.session.commit()
print(type(TypePersonne))
"""



noms_maisons_retraite = []
@app.route('/test')
def test():
    """
    untype = Personne(id_type_personne=0, nom_personne="Marley", prenom_personne="Ulrich",
                          telephone_personne="063", email_personne="@")
    db.session.add(untype)
    db.session.commit()
    """
    noms = []
    prenoms = []
    telephones = []
    emails = []
    types = []

    maison_retraite = MaisonRetraite.query
    fiche_patient = FichePatient.query

    """
    personne = Personne.query
    type_personne = TypePersonne.query

    for personner in Personne.query:

        noms.append(personner.nom_personne)
        prenoms.append(personner.prenom_personne)
        telephones.append(personner.telephone_personne)
        emails.append(personner.email_personne)
        id_type = personner.id_type_personne

        for usager in db.session.query(TypePersonne).join(Personne,
            TypePersonne.id_type_personne == Personne.id_type_personne).filter(TypePersonne.id_type_personne == id_type):
            types.append(usager.type_personne)
    lataille = len(noms)
    """




    return render_template('bacasable.html',
                           maison_retraite=maison_retraite,
                           fiche_patient=fiche_patient
                           )

"""
class INFO_ANAMNESE(db.Model):
    ID_ANAMNESE = db.Column(db.Integer, primary_key=True)
    NIVEAU_COGNITION = db.Column(db.String(100))
    EXPERIENCE_APPAREILLAGE = db.Column(db.String(100))
    ID_BOUCHON_OREILLE_DROITE = db.Column(db.Integer)
    ID_BOUCHON_OREILLE_GAUCHE = db.Column(db.Integer)
    REMARQUE = db.Column(db.String(100))
    AVIS_PATIENT = db.Column(db.String(500))
    ID_COUPLAGE_OREILLE_DROITE = db.Column(db.Integer)
    ID_COUPLAGE_OREILLE_GAUCHE = db.Column(db.Integer)
    ID_APPAREIL_OREILLE_DROITE = db.Column(db.Integer)
    ID_APPAREIL_OREILLE_GAUCHE = db.Column(db.Integer)
    ID_EMBOUT_OREILLE_DROITE = db.Column(db.Integer)
    ID_EMBOUT_OREILLE_GAUCHE = db.Column(db.Integer)

    # Create A String
    def __repr__(self):
        return '<INFO_ANAMNESE %r>' % self.REMARQUE




    # Create A String
    def __repr__(self):
        return '<FICHE_PATIENT %r>' % self.DATE_DEPISTAGE

"""


# Création des modèles Flaskform pour vérifier l'intégrité des données


@app.route('/displaymaisonretraite')
def displaymaisonretraite():
    """"""
    noms_maisons_retraite = []
    adresses_maisons_retraite = []
    telephones_maisons_retraite = []
    noms_cadres_sante = []
    telephones_cadres_sante = []
    emails_cadres_sante = []
    noms_directeurs = []
    telephones_directeurs = []
    emails_directeurs = []
    maison_retraite = MaisonRetraite.query
    for maison in MaisonRetraite.query:

        noms_maisons_retraite.append(maison.nom_maison_retraite)
        adresses_maisons_retraite.append(maison.adresse_maison_retraite)
        telephones_maisons_retraite.append(maison.telephone_maison_retraite)
        noms_cadres_sante.append(maison.nom_cadre_sante)
        telephones_cadres_sante.append(maison.telephone_cadre_sante)
        emails_cadres_sante.append(maison.email_cadre_sante)
        noms_directeurs.append(maison.nom_directeur)
        telephones_directeurs.append(maison.telephone_directeur)
        emails_directeurs.append(maison.email_directeur)

        """
        id_cds = maison.id_cadre_sante
        id_dir = maison.id_directeur
        for personnel_cds in db.session.query(Personne).join(MaisonRetraite,
            Personne.id_personne == MaisonRetraite.id_cadre_sante).filter(MaisonRetraite.id_cadre_sante == id_cds):

            noms_cadres_sante.append(personnel_cds.nom_personne)
            telephones_cadres_sante.append(personnel_cds.telephone_personne)
            emails_cadres_sante.append(personnel_cds.email_personne)

        for personnel_dir in db.session.query(Personne).join(MaisonRetraite,
                Personne.id_personne == MaisonRetraite.id_directeur).filter(MaisonRetraite.id_directeur == id_dir):
            noms_directeurs.append(personnel_dir.nom_personne)
            telephones_directeurs.append(personnel_dir.telephone_personne)
            emails_directeurs.append(personnel_dir.email_personne)
        """
    lataille = len(noms_maisons_retraite)





    return render_template('displaymaisonretraite.html',
                           title='MaisonRetraite',
                           maison_retraite=maison_retraite,
                           noms_maisons_retraite=noms_maisons_retraite,
                           adresses_maisons_retraite=adresses_maisons_retraite,
                           telephones_maisons_retraite=telephones_maisons_retraite,
                           noms_cadres_sante=noms_cadres_sante,
                           telephones_cadres_sante=telephones_cadres_sante,
                           emails_cadres_sante=emails_cadres_sante,
                           noms_directeurs=noms_directeurs,
                           telephones_directeurs=telephones_directeurs,
                           emails_directeurs=emails_directeurs,
                           lataille=lataille
                           )


@app.route('/displaypatient', methods=['GET', 'POST'])
def displaypatient():
    nom_patient = []
    prenom_patient = []
    nom_maison_retraite = []
    id_statut_actuel = []
    date_depistage = []
    date_acceptation = []
    date_commande_embout = []
    date_reception_embout = []
    date_adaptation_appareillage = []
    date_facturation = []
    conseil_appareillage_od = []
    conseil_appareillage_og = []
    couplage_od = []
    couplage_og = []

    for patients in db.session.query(FichePatient):
        nom_patient.append(patients.nom_patient)
        prenom_patient.append(patients.prenom_patient)
        id_statut_actuel.append(patients.id_statut_actuel)
        date_depistage.append(patients.date_depistage)
        date_acceptation.append(patients.date_acceptation)
        date_commande_embout.append(patients.date_commande_embout)
        date_reception_embout.append(patients.date_reception_embout)
        date_adaptation_appareillage.append(patients.date_adaptation_appareillage)
        date_facturation.append(patients.date_facturation)
        conseil_appareillage_od.append(patients.conseil_appareillage_od)
        conseil_appareillage_og.append(patients.conseil_appareillage_og)
        couplage_od.append(patients.couplage_od)
        couplage_og.append(patients.couplage_og)

        id_maison_retraite = patients.id_maison_retraite

        for la_maisonretraite in db.session.query(MaisonRetraite).join(FichePatient,
                            MaisonRetraite.id_maison_retraite == FichePatient.id_maison_retraite).filter(
                            MaisonRetraite.id_maison_retraite == id_maison_retraite):
            nom_maison_retraite.append(la_maisonretraite.nom_maison_retraite)

    lataille = len(nom_patient)

    return render_template('displaypatient.html',
                           title='SuiviPatient',
                           nom_patient=nom_patient,
                           prenom_patient=prenom_patient,
                           nom_maison_retraite=nom_maison_retraite,
                           lataille=lataille,
                           )


@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    # Validate Form
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        flash('User Added Sucessfully')
    our_users = Users.query.order_by(Users.date_added)
    return render_template("add_user.html",
                           form=form,
                           name=name,
                           our_users=our_users)


# def index():
#    return "<h6>Hello World!</h6>"


# safe
# trim
# striptags

@app.route('/')
def index():
    first_name = "Gary"
    favorite_pizza = ["olive", "fromage", "poivron", 41]
    stuff = "This is bold text"
    return render_template("index.html",
                           name=first_name,
                           stuff=stuff,
                           favorite_pizza=favorite_pizza)


@app.route('/user/<name>')
def user(name):
    return render_template("user.html", user_name=name)


# Custom error page

# Invalid URL
@app.errorhandler(404)
def page_note_found(e):
    return render_template("404.html"), 404


# Ubterbak server error
@app.errorhandler(500)
def page_note_found(e):
    return render_template("500.html"), 500


# Create a Form Class
class NamerForm(FlaskForm):
    name = EmailField("What's your name", validators=[Email()])
    submit = SubmitField('Submit')


# BooleanFIeld
# DateField / DataTimeField / DecimalField /FloatField PasswordField RadioFielld SelectField SelectMultipleFIeld TextAreaField

# Validator  Email/ Regexp /AnyOf NoneOf etc / InputRequired / URL / NumberRange

# Create Name Page
@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = NamerForm()
    # Validate Form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''

    return render_template("name.html",
                           name=name,
                           form=form)


class MaisonRetraiteForm(FlaskForm):
    nom_maison_retraite = StringField("Nom de l'établissement", validators=[DataRequired()])
    adresse_etablissement = StringField("Adresse postale", validators=[DataRequired()])
    telephone_etablissement = StringField("Téléphone Etablissement")
    nom_cadre_sante = StringField("Nom cadre santé")
    telephone_cadre_sante = StringField("Téléphone cadre santé")
    #adresse_mail_cadre_sante = EmailField("Adresse Email cadre santé", validators=[Email()])
    adresse_mail_cadre_sante = EmailField("Adresse Email cadre santé")
    nom_directeur = StringField("Nom direction")
    telephone_directeur = StringField("Téléphone direction")
    #adresse_mail_directeur = EmailField("Adresse Email direction", validators=[Email()])
    adresse_mail_directeur = EmailField("Adresse Email direction")
    submit = SubmitField('Enregistrer la fiche')


@app.route('/maisonretraite', methods=['GET', 'POST'])
def maisonretraite():
    nom_maison_retraite = None
    adresse_etablissement = None
    telephone_etablissement = None
    nom_cadre_sante = None
    telephone_cadre_sante = None
    adresse_mail_cadre_sante = None
    nom_directeur = None
    telephone_directeur = None
    adresse_mail_directeur = None
    form = MaisonRetraiteForm()
    dbclass = MaisonRetraite

    # Validation du formulaire
    if form.validate_on_submit():
        print("OK")
        # On récupère les données
        nom_maison_retraite = form.nom_maison_retraite.data
        adresse_etablissement = form.adresse_etablissement.data
        telephone_etablissement = form.telephone_etablissement.data
        nom_cadre_sante = form.nom_cadre_sante.data
        telephone_cadre_sante = form.telephone_cadre_sante.data
        adresse_mail_cadre_sante = form.adresse_mail_cadre_sante.data
        nom_directeur = form.nom_directeur.data
        telephone_directeur = form.telephone_directeur.data
        adresse_mail_directeur = form.adresse_mail_directeur.data
        info = []
        info.append(nom_maison_retraite)
        info.append(adresse_etablissement)
        info.append(telephone_etablissement)
        info.append(nom_cadre_sante)
        info.append(telephone_cadre_sante)
        info.append(adresse_mail_cadre_sante)
        info.append(nom_directeur)
        info.append(telephone_directeur)
        info.append(adresse_mail_directeur)

        # On enregistre le contact dans google
        try:
            enregistrement_google_people(info)
        except:
            os.remove("/tolkienetjason/token_people_v1.pickle")
            enregistrement_google_people(info)

        # On enregistre dans la base de donnée
        enregistrement_database(info, db, dbclass)

        # On remet à zéro le formulaire

        form.nom_maison_retraite.data = ''
        form.adresse_etablissement.data = ''
        form.telephone_etablissement.data = ''
        form.nom_cadre_sante.data = ''
        form.telephone_cadre_sante.data = ''
        form.adresse_mail_cadre_sante.data = ''
        form.nom_directeur.data = ''
        form.telephone_directeur.data = ''
        form.adresse_mail_directeur.data = ''
        flash("a bien été crée")



    return render_template("maisonretraite.html",
                           nom_maison_retraite=nom_maison_retraite,
                           adresse_etablissement=adresse_etablissement,
                           telephone_etablissement=telephone_etablissement,
                           nom_cadre_sante=nom_cadre_sante,
                           telephone_cadre_sante=telephone_cadre_sante,
                           adresse_mail_cadre_sante=adresse_mail_cadre_sante,
                           nom_directeur=nom_directeur,
                           telephone_directeur=telephone_directeur,
                           adresse_mail_directeur=adresse_mail_directeur,
                           form=form)


app.run(debug=True)
