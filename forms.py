from flask_wtf import FlaskForm
from wtforms import IntegerField



class GameForm(FlaskForm):
    up = IntegerField('up')
    left = IntegerField('left')
    right = IntegerField('right')
    down = IntegerField('down')
    take = IntegerField('take')
    drop = IntegerField('drop')