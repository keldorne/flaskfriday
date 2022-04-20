from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField
from wtforms.validators import DataRequired, Email
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from datetime import datetime

# Initialisation du framework Flask
app = Flask(__name__)

# Chargement de la base de donnée
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test3.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialisation de la clef secrete pour sécuriser la communication entre backend et fontend
app.config['SECRET_KEY'] = "jackstone"

# Initialisation de SQLalchemy et traitement de la base de donnée objet
db = SQLAlchemy(app)



"""
#Create Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    #Create A String
    def __repr__(self):
        return '<Name %r>' % self.name


#Create a form with WTF
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = EmailField("Email", validators=[Email()])
    submit = SubmitField('Submit')
"""

#Création des modèles de tables avec SQLAlchemy
class INFO_MAISON_RETRAITE(db.Model):
    ID_MAISON_RETRAITE = db.Column(db.Integer, primary_key=True)
    NOM_MAISON_RETRAITE = db.Column(db.String(100), nullable=False, unique=True)
    ADRESSE_MAISON_RETRAITE = db.Column(db.String(100), nullable=False, unique=True)
    info_humain = db.relationship('INFO_HUMAIN', backref='INFO_MAISON_RETRAITE', lazy=True)

    #Create A String
    def __repr__(self):
        return '<INFO_MAISON_RETRAITE %r>' % self.NOM_MAISON_RETRAITE

class INFO_HUMAIN(db.Model):
    ID_INFO_HUMAIN = db.Column(db.Integer, primary_key=True)
    ID_INFO_MAISON_RETRAITE = db.Column(db.Integer, db.ForeignKey('INFO_MAISON_RETRAITE.ID_MAISON_RETRAITE'),
        nullable=False)
    TYPE_HUMAIN = db.Column(db.Integer, nullable=False)
    NOM_HUMAIN = db.Column(db.String(100), nullable=False)
    PRENOM_HUMAIN = db.Column(db.String(100))
    SEXE_HUMAIN = db.Column(db.String(100))
    TELEPHONE_HUMAIN = db.Column(db.String(100), nullable=False)
    EMAIL_HUMAIN = db.Column(db.String(100), nullable=False)

    # Create A String
    def __repr__(self):
        return '<INFO_HUMAIN %r>' % self.NOM_HUMAIN

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

class FICHE_PATIENT(db.Model):
    ID_FICHE_PATIENT = db.Column(db.Integer, primary_key=True)
    ID_INFO_PATIENT = db.Column(db.Integer, db.ForeignKey('INFO_HUMAIN.ID_INFO_HUMAIN'))
    INFO_PATIENT = db.relationship('INFO_HUMAIN', backref=sqlalchemy.orm.backref('INFO_HUMAIN'), lazy=True)
    #ID_INFO_PATIENT = db.Column(db.Integer)
    ID_INFO_ACCOMPAGNANT = db.Column(db.Integer)
    ID_INFO_CDS = db.Column(db.Integer)
    ID_INFO_DIRECTEUR = db.Column(db.Integer)
    ID_ANAMNESE = db.Column(db.Integer)
    DATE_DEPISTAGE = db.Column(db.String(100))
    DATE_ACCEPTATION_APPAREILLAGE = db.Column(db.String(100))
    DATE_COMMANDE_EMBOUT = db.Column(db.String(100))
    DATE_RECEPTION_EMBOUT = db.Column(db.String(100))
    DATE_RECEPTION_APPAREIL = db.Column(db.String(100))
    DATE_ADAPTATION = db.Column(db.String(100))

    # Create A String
    def __repr__(self):
        return '<FICHE_PATIENT %r>' % self.DATE_DEPISTAGE


#Création des modèles Flaskform pour vérifier l'intégrité des données



@app.route('/displaymaisonretraite')
def displaymaisonretraite():
    maison_retraite = INFO_MAISON_RETRAITE.query
    return render_template('displaymaisonretraite.html',
                           title='MaisonRetraite',
                           maison_retraite=maison_retraite)

@app.route('/displaypatient')
def displaypatient():
    patient = FICHE_PATIENT.query
    maison_retraite = INFO_MAISON_RETRAITE.query
    humain = INFO_HUMAIN.query
    return render_template('displaypatient.html',
                           title='SuiviPatient',
                           patient=patient,
                           maison_retraite=maison_retraite,
                           humain=humain)


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





#def index():
#    return "<h6>Hello World!</h6>"


#safe
#trim
#striptags

@app.route('/')
def index():
    first_name = "Gary"
    favorite_pizza = ["olive", "fromage", "poivron", 41]
    stuff = "This is bold text"
    return render_template("index.html",
                           name=first_name,
                           stuff = stuff,
                           favorite_pizza = favorite_pizza)

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

#BooleanFIeld
#DateField / DataTimeField / DecimalField /FloatField PasswordField RadioFielld SelectField SelectMultipleFIeld TextAreaField

#Validator  Email/ Regexp /AnyOf NoneOf etc / InputRequired / URL / NumberRange

#Create Name Page
@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = NamerForm()
    #Validate Form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''

    return render_template("name.html",
                           name=name,
                           form=form)









class MaisonRetraiteForm(FlaskForm):
    nom_maison_retraite = StringField("Nom de l'établissement", validators = [DataRequired()])
    nom_responsableA = StringField("Nom cadre santé")
    nom_responsableB = StringField("Nom du directeur")
    telephone = StringField("Téléphone")
    adresse_mail = EmailField("Adresse Email", validators=[Email()])
    submit = SubmitField('Enregistrer')


@app.route('/maisonretraite', methods=['GET', 'POST'])
def maisonretraite():
    nom_maison_retraite = None
    nom_responsableA = None
    nom_responsableB = None
    telephone = None
    adresse_mail = None
    form = MaisonRetraiteForm()
    # Validation du formulaire
    if form.validate_on_submit():
        nom_maison_retraite = form.nom_maison_retraite.data
        nom_responsableA = form.nom_responsableA.data
        nom_responsableB = form.nom_responsableB.data
        telephone = form.telephone.data
        adresse_mail = form.adresse_mail.data
        form.nom_maison_retraite.data = ''
        form.nom_responsableA.data = ''
        form.nom_responsableB.data = ''
        form.telephone.data = ''
        form.adresse_mail.data = ''
        flash("a bien été crée")

    return render_template("maisonretraite.html",
                           nom_maison_retraite=nom_maison_retraite,
                           nom_responsableA=nom_responsableA,
                           nom_responsableB=nom_responsableB,
                           telephone=telephone,
                           adresse_mail=adresse_mail,
                           form=form)





app.run(debug=True)




