#from flask.ext.wtf import Form
# from wtforms import fields,validators,Form
# from flask_wtf import FlaskForm
from flask_wtf import FlaskForm
from flask.ext.wtf import Form
from wtforms import fields, validators,Form
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from .models import Section,SectionContent,Docs,Gaps

class SectionForm(Form):
    SectionTitle = fields.StringField()
   
    #section = QuerySelectField(query_factory=lambda: Section.query.all())


class SectionContentForm(Form):
    section = QuerySelectField(query_factory=lambda: Section.query.all())
    
    ScenarioName = fields.StringField()
   
    
   
    Description = fields.StringField()

    scenario = QuerySelectField(query_factory=lambda: SectionContent.query.all())
    

    
class DocsForm(Form):
    Name = fields.StringField()
    Link = fields.StringField()

class GapsForm(Form):
    Description = fields.StringField()
    Url = fields.StringField()    