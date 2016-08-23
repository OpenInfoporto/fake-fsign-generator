from flask import Flask, render_template, flash, request, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import Form, RecaptchaField
from flask_wtf.file import FileField
from flask_appconfig import AppConfig
from wtforms import TextField, HiddenField, ValidationError, RadioField,\
    BooleanField, SubmitField, IntegerField, FormField, validators
from wtforms.validators import Required
from generator import FCodeGenerator
from PIL import Image, ImageDraw
import random

# straight from the wtforms docs:
class GenerationForm(Form):
    companyName = TextField('Company Name', [validators.required()])
    
    submit_button = SubmitField('Submit Form')

def create_app(configfile=None):
    app = Flask(__name__)
    AppConfig(app, configfile)
    Bootstrap(app)

    # in a real app, these should be configured through Flask-Appconfig
    app.config['SECRET_KEY'] = 'f1ng3rpr1nt2016'

    @app.route('/')
    def index():
        form = GenerationForm()
        return render_template('index.html', form=form)
        
    @app.route('/result', methods=['POST'])
    def result():
        data = request.form['companyName']
        
        g = FCodeGenerator(image_size=50, image_border=4, density=200)
        filepath = 'test.png'
        image = g.make()
        image.save(filepath)
        img = Image.open(filepath).resize((500,500))
        img.save(filepath)
        g.merge_pictures(filepath, "finger.png", "static/out.png")
            
        return render_template('result.html')

    return app

if __name__ == '__main__':
    create_app().run(debug=True)
