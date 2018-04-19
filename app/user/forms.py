from flask_wtf import FlaskForm
from wtforms import StringField,BooleanField,PasswordField,ValidationError,DateField,FileField,validators,widgets
from wtforms.validators import DataRequired,Length,Email

from ..models import User

class ProfileForm(FlaskForm):
    address = StringField('Địa chỉ',validators=[DataRequired(message='Địa chỉ không được trống!'), Length(1, 255)])
    phone_number = StringField('Số điện thoại',validators=[DataRequired(message='Địa chỉ không được trống!'), Length(1, 255)])
    avartar = FileField('Ảnh đại diện')
