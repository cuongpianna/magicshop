from flask_wtf import FlaskForm
from wtforms import StringField,ValidationError,DecimalField,SelectField,FileField,TextField
from wtforms.validators import DataRequired,Length,InputRequired,NumberRange
from app.models import Category
from flask_ckeditor import CKEditorField

class AdminAddCategory(FlaskForm):
    name = StringField('Tên tài khoản', validators=[DataRequired(), Length(1, 255)])

class ProductAdmin(FlaskForm):
    name = StringField('Tên sản phẩm',validators=[DataRequired()])
    price = DecimalField('Giá', validators=[InputRequired(), NumberRange(min=(0.0))])
    description = CKEditorField('Mô tả')
    image = FileField('Ảnh minh họa')
    cagetory = SelectField('Loại sản phẩm',coerce=int)

    def __init__(self):
        super(ProductAdmin, self).__init__()
        self.cagetory.choices = [(c.id,c.name) for c in Category.query.all()]

