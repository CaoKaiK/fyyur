import sys
import json
import dateutil.parser
import babel
from datetime import datetime

from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify
from flask import render_template
from sqlalchemy import func

from app import db
from app.main import bp
from .models import Venue, Artist, Show
from .models import VenueSchema, VenueSearchSchema, ArtistSearchSchema
from .forms import VenueForm, ArtistForm, ShowForm





@bp.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@bp.route('/venues')
def venues():
  # get locations with distinct city and state
  venue_locations = Venue.query.distinct(Venue.city, Venue.state).all()
  return render_template('pages/venues.html', areas=venue_locations)

@bp.route('/venues/search', methods=['POST'])
def search_venues():
  # venues filtered by search term
  search_term = request.form.get('search_term', '')
  data = Venue.query.filter(Venue.name.ilike(f'%{search_term}%')).all()
  
  response={
    "count": len(data),
    "data": data
  }
  return render_template('pages/search_venues.html', results=response, search_term=search_term)

@bp.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  venue = Venue.query.filter_by(id=venue_id).first()
  return render_template('pages/show_venue.html', venue=venue)

#  CRUD Venue
#  ----------------------------------------------------------------

@bp.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@bp.route('/venues/create', methods=['POST'])
def create_venue_submission():
  form = VenueForm(request.form)

  try:
    # could be done with wtf-forms populate?
    venue = Venue(
      name=form.name.data,
      city=form.city.data,
      state=form.state.data,
      address=form.address.data,
      phone=form.phone.data,
      #image_link=form['image_link'],
      facebook_link=form.facebook_link.data,
      genres=form.genres.data,
      #website=form['website'],
      #seeking_talent=form['seeking_talent'],
      #seeking_description=form['seeking_description'],
    )

    db.session.add(venue)
    db.session.commit()

    flash('Venue ' + request.form['name'] + ' was successfully listed!')

    return render_template('pages/home.html')
  except:
    #print(sys.exc_info())

    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.', category="error")
    #db.session.rollback()
    return render_template('pages/home.html')

  finally:
    db.session.close()



@bp.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  # get venue and populate form  
  venue = Venue.query.filter_by(id=venue_id).first()
  form = VenueForm(obj=venue)

  return render_template('forms/edit_venue.html', form=form, venue=venue)

@bp.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  form = VenueForm(request.form)
  venue = Venue.query.filter_by(id=venue_id).first()
  try:
    form.populate_obj(venue)
    db.session.commit()
    flash('Venue updated', category="error")
  except:
    flash('An error occurred. Venue could not be updated.', category="error")

  finally:
    db.session.close()
    return redirect(url_for('main.show_venue', venue_id=venue_id))



@bp.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  try:
    venue = Venue.query.filter_by(id=venue_id)
    db.session.delete(venue)

    flash('Venue was removed')
    return render_template('pages/home.html')

  except:
    flash('Venue was not removed', category="error")
    db.session.rollback()
    return None

#  Artists
#  ----------------------------------------------------------------
@bp.route('/artists')
def artists():
  artists = Artist.query.all()
  return render_template('pages/artists.html', artists=artists)

@bp.route('/artists/search', methods=['POST'])
def search_artists():
  # venues filtered by search term
  search_term = request.form.get('search_term', '')
  data = Artist.query.filter(Artist.name.ilike(f'%{search_term}%')).all()
  
  response={
    "count": len(data),
    "data": data
  }
  return render_template('pages/search_artists.html', results=response, search_term=search_term)

@bp.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  artist = Artist.query.filter_by(id=artist_id).first()
  return render_template('pages/show_artist.html', artist=artist)


#  CRUD Artist
#  ----------------------------------------------------------------

@bp.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@bp.route('/artists/create', methods=['POST'])
def create_artist_submission():
  form = ArtistForm(request.form)

  try:
    artist = Artist(
      name=form.name.data,
      city=form.city.data,
      state=form.state.data,
      phone=form.phone.data,
      #image_link=form['image_link'],
      facebook_link=form.facebook_link.data,
      genres=form.genres.data,
      #website=form['website'],
      #seeking_talent=form['seeking_talent'],
      #seeking_description=form['seeking_description'],
    )

    db.session.add(artist)
    db.session.commit()

    flash('Artist ' + request.form['name'] + ' was successfully listed!')

    return render_template('pages/home.html')
  except:
    #print(sys.exc_info())

    flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.', category="error")
    db.session.rollback()
    return render_template('pages/home.html')

  finally:
    db.session.close()



@bp.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  # get artist and populate form  
  artist = Artist.query.filter_by(id=artist_id).first()
  form = ArtistForm(obj=artist)

  return render_template('forms/edit_artist.html', form=form, artist=artist)

@bp.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  form = ArtistForm(request.form)
  artist = Artist.query.filter_by(id=artist_id).first()
  try:
    form.populate_obj(artist)
    db.session.commit()
    flash('Artist updated', category="error")
  except:
    flash('An error occurred. Artist could not be updated.', category="error")

  finally:
    db.session.close()
    return redirect(url_for('main.show_artist', artist_id=artist_id))


#  Shows
#  ----------------------------------------------------------------

@bp.route('/shows')
def shows():
  shows = Show.query.all()
  return render_template('pages/shows.html', shows=shows)

@bp.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@bp.route('/shows/create', methods=['POST'])
def create_show_submission():
  form = ShowForm(request.form)

  try:
    show = Show(
      start_time=form.start_time.data,
      artist_id=form.artist_id.data,
      venue_id=form.venue_id.data,
    )

    db.session.add(show)
    db.session.commit()
    
    flash('Show was successfully listed!')

    return render_template('pages/home.html')
  
  except:
    #print(sys.exc_info())

    flash('An error occurred. Show could not be listed.', category="error")
    db.session.rollback()

    return render_template('pages/home.html')

  finally:
    db.session.close()

