from flask_wtf import FlaskForm
from wtforms import StringField,BooleanField,PasswordField,ValidationError
from wtforms.validators import DataRequired,Length,EqualTo,Email

from ..models import User

class RegisterForm(FlaskForm):
    user_name = StringField('Tên tài khoản',validators=[DataRequired(message='Tài khoản không được trống!'),Length(1,255)])
    email = StringField("Email",validators=[DataRequired(message='Email không được trống!'),Length(1,255),Email()])
    password = PasswordField('Password', validators=[
        DataRequired(message='Mật khẩu không được trống!'), EqualTo('password2', message='Nhập lại khẩu không khớp!')])
    password2 = PasswordField('Confirm password', validators=[DataRequired('Nhập lại mật khẩu không được trống!')])

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(f'Email đã tổn tại')

    def validate_user_name(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(f'Tài khoản đã tồn tại')

class LoginForm(FlaskForm):
    email = StringField("Email",validators=[DataRequired(message='Email không được trống!'),Length(1,255)])
    password = PasswordField('Password',validators=[DataRequired(message='Mật khẩu không được trống!')])
    remember_me = BooleanField('rememberme',default=False)

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old password', validators=[DataRequired(message='Không được bỏ trống trường này!')])
    password = PasswordField('New password', validators=[
        DataRequired(message='Không được bỏ trống trường này!'), EqualTo('password2', message='Nhập lại mật khẩu không khớp!')])
    password2 = PasswordField('Confirm new password', validators=[DataRequired(message='Không được bỏ trống trường này!')])



