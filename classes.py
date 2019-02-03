from flask_wtf import FlaskForm
from wtforms import TextField, IntegerField, SubmitField

class RdvCreate(FlaskForm):
    date = TextField('Date')
    description = TextField('Description')
    heure = TextField('Heure')
    creer = SubmitField('Creer')

class RdvSupprimer(FlaskForm):
    id = TextField('ID')
    supprimer = SubmitField('Supprimer')

class RdvModifier(FlaskForm):
    id = TextField('ID')
    description = TextField('Description')
    modifier = SubmitField('Modifier')

class Reinit(FlaskForm):
    reinit = SubmitField('Reinitialiser')
