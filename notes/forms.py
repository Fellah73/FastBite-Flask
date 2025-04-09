from flask_wtf import FlaskForm
from wtforms import DateTimeField, IntegerField, StringField,SubmitField,EmailField,PasswordField
from wtforms.validators import DataRequired,EqualTo,ValidationError,Length,Email,NumberRange
from notes.models import User

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),Length(min=4,max=20)])
    email = EmailField('Email', validators=[DataRequired(),Email()])
    password1 = PasswordField('Password', validators=[DataRequired(),Length(min=8)]) 
    password2 = PasswordField('Confirm Password', validators=[DataRequired(),EqualTo('password1')])
    submit= SubmitField('Submit')
    def validate_username(self,username):
        user=User.query.filter_by(name=username.data).first()
        if user:
            raise ValidationError('Username already exists')
        
    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already exists')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired(),Length(min=8)])
    submit= SubmitField('Submit')
    
    
class PurchaseItemForm(FlaskForm):
    submit=SubmitField(label='Purchase Item')

class CancelItemForm(FlaskForm):
    submit=SubmitField(label='Cancel Item')
    
class ReservationForm(FlaskForm):
    reservation_day=IntegerField('Jour de la reservation',validators=[DataRequired(),NumberRange(min=1,max=31)])
    reservation_mois=IntegerField('Mois de la reservation',validators=[DataRequired(),NumberRange(min=1,max=12)])
    reservation_annee=IntegerField('Annee de la reservation',validators=[DataRequired(),NumberRange(min=2024,max=2100)])
    reservation_horaire_hour=IntegerField('Heure de la reservation',validators=[DataRequired(),NumberRange(min=0,max=23)])
    reservation_horaire_minute=IntegerField('Heure de la reservation',validators=[DataRequired(),NumberRange(min=0,max=59)])
    
    guests = IntegerField('Nombre de personnes invitées', validators=[DataRequired(),NumberRange(min=2,max=6)])
    submit = SubmitField('Réserver')
    
class AddPromoCodeForm(FlaskForm):
    promo_code = StringField('Code Promo', validators=[DataRequired()])
    submit = SubmitField('Ajouter')
    
    