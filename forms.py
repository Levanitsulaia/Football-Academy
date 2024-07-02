from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, DateField, RadioField, SelectField, SubmitField, IntegerField
from wtforms.validators import DataRequired, length, equal_to, ValidationError
from flask_wtf.file import FileField, FileRequired, FileSize, FileAllowed
from models import User


class RegisterForm(FlaskForm):
    profile_img = FileField("პროფილის სურათი", validators=[
        FileAllowed(["jpg", "png"], message="მხოლოდ სურათების ატვირთვა შიეძლება"), FileSize(1024 * 1024 * 7)])
    username = StringField("შეიყვანეთ იუზერნეიმი", validators=[DataRequired()])
    password = PasswordField("შეიყვანეთ პაროლი", validators=[DataRequired(),length(min=8, max=77, message="პაროლი უნდა იყოს 8-77 ასო")])
    repeat_password = PasswordField("გაიმეორეთ პაროლი", validators=[DataRequired(),
                                                                    equal_to("password", message="პაროლები არ ემთხვევა")])
    birthday = DateField()
    region_number = SelectField(choices=["+995"], validators=[DataRequired()])
    phone_number = IntegerField("შეიყავანეთ ტელეფონის ნომერი", validators=[DataRequired()])
    gender = RadioField("მონიშნეთ სქესი", choices=['კაცი', "ქალი"], validators=[DataRequired()])
    country = SelectField(choices=["აირჩიეთ ქვეყანა", "საქართველო", "ინგლისი", "საბერძნეთი", "ბრაზილია"], validators=[DataRequired()])

    submit = SubmitField("რეგისტრაცია")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('თქვენს მიერ შეყვანილი იუზერნეიმი გამოყენებულია,გთხოვთ შეიყვანთ სხვა იუზერნეიმი')

class LoginForm(FlaskForm):
    username = StringField("შეიყვანეთ იუზერნეიმი")
    password = PasswordField("შეიყვანეთ პაროლი")

    submit = SubmitField("შესვლა")

class ProductForm(FlaskForm):
    img = FileField()
    name = StringField("პროდუქტის სახელი")
    price = IntegerField("ფასი")
    submit = SubmitField("პროდუქტის ატვირთვა")

class ClubForm(FlaskForm):
    img = FileField()
    name = StringField("კლუბის სახელი")
    address = StringField("ადგილმდებარეობა")

    submit = SubmitField("კლუბის ატვირთვა")

class ContactForm(FlaskForm):
    email = StringField("შეიყვანეთ ელ.ფოსტა", validators=[DataRequired()])
    username = StringField ( "შეიყანეთ თვქენი იუზერნეიმი",  validators=[DataRequired()])
    city = StringField("შეიყვანეთ თვქენი ქალაქი", validators=[DataRequired()])
    problem = StringField("შეიყვანეთ თქვენი პრობლემა", validators=[DataRequired(),length(min=20,max=210, message="პრობლემა უნდა შეადგენდეს 20-210 ასოს")])

    submit = SubmitField("პრობლემის გაგზავნა")
