from datetime import datetime

from app import db, ma

#CURRENT_TIME = datetime.now

class Venue(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    # add missing attributes
    genres = db.Column(db.ARRAY(db.String))
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(120))

    @property
    def venues(self):
        # get venues subset for city and state
        query = self.query.filter_by(city=self.city, state=self.state).all()
        return query

    @property
    def past_shows(self):
        # filter for venue id and check start time in past
        query = Show.query.filter_by(venue_id=self.id).filter(Show.start_time<datetime.now()).all()
        return query
    
    @property
    def past_shows_count(self):
        return len(self.past_shows)

    @property
    def upcoming_shows(self):
        # filter for venue id and check start time in future
        query = Show.query.filter_by(venue_id=self.id).filter(Show.start_time>datetime.now()).all()
        return query

    @property
    def upcoming_shows_count(self):
        return len(self.upcoming_shows)
   

    def __repr__(self):
        return f'<Venue {self.name}>'


class VenueSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Venue
    
    city = ma.auto_field()
    state = ma.auto_field()

class VenueSearchSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Venue
    
    id = ma.auto_field()
    name = ma.auto_field()



class Artist(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    # add missing attributes
    website = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(120))

    
    def __repr__(self):
        return f'<Artist {self.name}>'

class ArtistSearchSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Artist
    
    id = ma.auto_field()
    name = ma.auto_field()


class Show(db.Model):
    __tablename__ = 'show'

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime())

    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
    venue = db.relationship('Venue', backref=db.backref('shows'))
    
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    artist = db.relationship('Artist', backref=db.backref('shows'))

    @property
    def venue_name(self):
        return self.venue.name
    
    @property
    def artist_name(self):
        return self.artist.name
    
    @property
    def artist_image_link(self):
        return self.artist.artist_image_link
    
    def __repr__(self):
        return f'<Show {self.id}>'