from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Section(db.Model):
    
    __tablename__ = 'Section'
    
    id = db.Column(db.Integer, primary_key=True)
    SectionTitle = db.Column(db.String)
    sccontent = db.relationship('SectionContent', backref='Section', lazy='select')
    def __repr__(self):
        return '<Section {:d} {}>'.format(self.id, self.SectionTitle)

    def __str__(self):
        return self.SectionTitle


class SectionContent(db.Model):
   
    __tablename__ = 'SectionContent'
    id = db.Column(db.Integer, primary_key=True)
    ScenarioName = db.Column(db.String)
    Description = db.Column(db.String)
        
    section_id = db.Column(db.Integer, db.ForeignKey('Section.id'))
    doc = db.relationship('Docs', backref='SectionContent', lazy='select')
    gap = db.relationship('Gaps', backref='SectionContent', lazy='select')

    def __repr__(self):
       return '<SectionContent {:d} {} >'.format(self.id,self.ScenarioName)

    def __str__(self):
        return self.ScenarioName   

class Docs(db.Model):

    __tablename__ = 'Docs'
    id = db.Column(db.Integer, primary_key=True)
    Name =  db.Column(db.String)
    Link =  db.Column(db.String)

    sectioncontent_id = db.Column(db.Integer, db.ForeignKey('SectionContent.id'))

    def __repr__(self):
       return '<Docs {:d} {} >'.format(self.id,self.Name)

class Gaps(db.Model):

    __tablename__ = 'Gaps'
    id = db.Column(db.Integer, primary_key=True)
    Description =  db.Column(db.String)
    Url =  db.Column(db.String)

    sectioncontent_id = db.Column(db.Integer, db.ForeignKey('SectionContent.id'))

    def __repr__(self):
       return '<Gaps {:d} {} >'.format(self.id,self.Description)
       
       
def query_to_list(query, include_field_names=True):
    """Turns a SQLAlchemy query into a list of data values."""
    
    column_names = []
    for i, obj in enumerate(query.all()):
        if i == 0:
            column_names = [c.name for c in obj.__table__.columns]
            if include_field_names:
                yield column_names
        yield obj_to_list(obj, column_names)

def obj_to_list(sa_obj, field_order):
    """Takes a SQLAlchemy object - returns a list of all its data"""
    return [getattr(sa_obj, field_name, None) for field_name in field_order]


