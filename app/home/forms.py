from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    search = StringField('Tìm kiếm',validators=[DataRequired()])

class CheckOutForm(FlaskForm):
    user_adress = StringField('Địa chỉ nhận hàng',validators=[DataRequired(message='Không được bỏ trống trường này')])
    message = TextAreaField('Tin nhắn',validators=[DataRequired(message='Không được bỏ trống trường này')])