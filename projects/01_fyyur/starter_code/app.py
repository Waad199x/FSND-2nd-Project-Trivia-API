# 12/20

#[[DONE]] TODO: connect to a local postgresql database
#[[DONE]] TODO: implement any missing fields, as a database migration using Flask-Migrate

#[[DONE]]TODO: implement any missing fields, as a database migration using Flask-Migrate

# [[DONE]]TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration. 

 #[[DONE]] TODO: replace with real venues data.  
 # [[DONE]]TODO:  num_shows should be aggregated based on number of upcoming shows per venue.

 #[[DONE]]TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"  

 #[[DONE]] TODO: replace with real venue data from the venues table, using venue_id 

 # [[DONE]] TODO: insert form data as a new Venue record in the db, instead
 # [[DONE]]TODO: modify venue data to be the data object returned from db insertion  

  # [[DONE]] TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  # [[DONE]] BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage

  #[[DONE]] TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".

  #[[DONE]] TODO: replace with real artist data from the artist table, using artist_id 

  #[[DONE]]TODO: populate form with fields from artist with ID <artist_id>
   # [[DONE]]TODO: modify artists data to be the data object returned from db insertion  

  #[[DONE]] TODO: take values from the form submitted, and update existing

  # [[DONE]] TODO: insert form data as a new Venue record in the db, instead
  # [[DONE]]TODO: modify data to be the data object returned from db insertion

  # [[DONE]] TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
 # [[DONE]]TODO: modify shows data to be the data object returned from db insertion  

  # displays list of shows at /shows
  # [[DONE]]TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
from datetime import datetime 
import dateutil.parser
import babel
from flask import Flask, render_template, request, flash, redirect, url_for,abort,jsonify
from sqlalchemy import func
from sqlalchemy.orm import Session
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate 
import sys
from django.db import models
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# TODO: connect to a local postgresql database [[DONE]]

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
from Models import *
#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  if isinstance(value, str):
        date = dateutil.parser.parse(value)
  else:
        date = value

  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime



#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues(): #[[DONE]] num shows left
  # TODO: replace with real venues data. 
  #       num_shows should be aggregated based on number of upcoming shows per venue.
    #num_shows = Venue.query.all()
 
    venues =  Venue.query.all()

    area_list = []
    for a in venues :
        area_list.append(a.city)
    area_list = list(dict.fromkeys(area_list))


    return render_template('pages/venues.html', areas = venues , area_list=area_list  )
        

@app.route('/venues/search', methods=[ 'POST'])
def search_venues():
  # TODO: implement search on venues with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  #request.form.get('<name>'),by the name attribute on the input HTML element
        search_term = request.form.get('search_term', '')
        format = "%{}%".format(search_term)
        objects = Venue.name
        venues = Venue.query.filter(objects.ilike(format)).all()

        return render_template('pages/search_venues.html', results=venues, search_term=search_term)

import datetime
@app.route('/venues/<int:venue_id>') #[[DONE]] data left
def show_venue(venue_id):
  venue = Venue.query.get(venue_id)
 
  all_upcoming_shows = db.session.query(Show).join(Artist).filter(Show.venue_id==venue_id).filter(Show.start_date>datetime.datetime.now()).all()
  upcoming_shows = []

  all_past_shows = db.session.query(Show).join(Artist).filter(Show.venue_id==venue_id).filter(Show.start_date<datetime.datetime.now()).all()
  past_shows = []
  
  for show in all_upcoming_shows:
    upcoming_shows.append({
      "artist_id": show.Artist_id,
      "artist_name": show.artist.name,
      "artist_image_link": show.artist.image_link,
      "start_date": show.start_date
    })

  for show in all_past_shows:
    past_shows.append({
      "artist_id": show.Artist_id,
      "artist_name": show.artist.name,
      "artist_image_link": show.artist.image_link,
      "start_date": show.start_date    
    })

  gen_query = db.session.query(Venue.genres).filter(Venue.id==venue_id)
 
  genres_list=[]
  for g in gen_query :
      genres_list.append(g) #  genres_list is list with one string
  genres = str(genres_list[0])
  b = genres[3:-4]
  genres = str(b)
  glist = list(genres.split(","))


  return render_template('pages/show_venue.html',genres=glist, venue=venue,past_shows=past_shows,upcoming_shows=upcoming_shows)
  # if null object is not itterable error happens its just that the data base have null value where HTML has python iteration statment like geners so i have to make is notnull 

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission(): # [[DONE]] Data left
  # TODO: insert form data as a new Venue record in the db, instead  [[DONE]]
  # TODO: modify data to be the data object returned from db insertion


    error = False
    try:
      name = request.form.get('name','')
      city = request.form.get('city','')
      address = request.form.get('address','')
      state = request.form.get('state','')
      phone = request.form.get('phone','')
      genres = request.form.getlist('genres')
  
      #genre_s = request.form.getlist('genres','')
      facebook_link = request.form.get('facebook_link','')
      website_link = request.form.get('website_link','')
      image_link = request.form.get('image_link','')
      seeking_description = request.form.get('seeking_description','')
      ven = Venue(name=name,city= city,state=state,genres=genres,seeking_description=seeking_description,website_link=website_link, address=address, phone=phone,image_link=image_link, facebook_link=facebook_link)
      db.session.add(ven)
      db.session.commit()


 

    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
        abort (400)
    else:
       flash('Venue ' + request.form['name'] + ' was successfully listed!')
       return render_template('pages/home.html')
 
     # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')



@app.route('/venues/<venue_id>', methods=['POST'])
def delete_venue(venue_id): #[[DONE]]
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage

  error = False
  try:
    Venue.query.filter_by(id=venue_id).delete()
    db.session.commit()
  except:
        error = True
        db.session.rollback()
        print(sys.exc_info())  
  finally:
        db.session.close()
  if error:
        flash('An error occurred. Venue could not be deleted.')
        abort (400)
  else:
       flash('Venue was successfully deleted!')
       return render_template('pages/home.html')

 

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists') #[[DONE]]
def artists():
  # TODO: replace with real data returned from querying the database 
  
  return render_template('pages/artists.html', artists=Artist.query.all())#upcoming_shows_count=upcoming_shows_count)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
    search_term = request.form.get('search_term', '')
    format = "%{}%".format(search_term)
    objects = Artist.name
    artists = Artist.query.filter(objects.ilike(format)).all()

    return render_template('pages/search_artists.html', results=artists, search_term=search_term)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id): #[[DONE]]
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  
  ar = Artist.query.get(artist_id)
  all_upcoming_shows = db.session.query(Show).join(Venue).filter(Show.Artist_id==artist_id).filter(Show.start_date>datetime.datetime.now()).all()
  upcoming_shows = []
  all_past_shows = db.session.query(Show).join(Venue).filter(Show.Artist_id==artist_id).filter(Show.start_date<datetime.datetime.now()).all()
  past_shows = []

  for show in all_upcoming_shows:
    upcoming_shows.append ({
      "venue_id": show.venue_id,
      "venue_name": show.venue.name,
      "venue_image_link": show.venue.image_link,
      "start_date": show.start_date
    })
    
  for show in all_past_shows:
    past_shows.append ({
      "venue_id": show.venue_id,
      "venue_name": show.venue.name,
      "venue_image_link": show.venue.image_link,
      "start_date": show.start_date
    })

  #data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]
  return render_template('pages/show_artist.html', artist=ar,past_shows=past_shows,upcoming_shows=upcoming_shows)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):#[[DONE]]
  form = ArtistForm()
  a={
    "id": 4,
    "name": "Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  }
  # TODO: populate form with fields from artist with ID <artist_id>
  artist=Artist.query.get(artist_id)


  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):#[[DONE]]
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  artist = Artist.query.get(artist_id)
  artist.name = request.form.get('name','')
  artist.city = request.form.get('city','')
  artist.state = request.form.get('state','')
  artist.phone = request.form.get('phone','')
  artist.genres = request.form.get('genres','')
  artist.facebook_link = request.form.get('facebook_link','')
  artist.website_link = request.form.get('website_link','')
  artist.image_link = request.form.get('image_link','')
  artist.seeking_description = request.form.get('seeking_description','')

  db.session.commit()
  flash('Artist ' + request.form['name'] + ' was successfully edited!')
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):#[[DONE]]
  form = VenueForm()
  v={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  }
  # TODO: populate form with values from venue with ID <venue_id>
  venue=Venue.query.get(venue_id)

  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):#[[DONE]]
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  venue = Venue.query.get(venue_id)
  venue.name = request.form.get('name','')
  venue.city = request.form.get('city','')
  venue.address = request.form.get('address','')
  venue.state = request.form.get('state','')
  venue.phone = request.form.get('phone','')
  venue.genres = request.form.get('genres','')
  venue.facebook_link = request.form.get('facebook_link','')
  venue.website_link = request.form.get('website_link','')
  venue.image_link = request.form.get('image_link','')
  venue.seeking_description = request.form.get('seeking_description','')


  db.session.commit()
  flash('Venue ' + request.form['name'] + ' was successfully edited!')
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])#[[DONE]]
def create_artist_submission():  #[[DONE]] data object left
  #called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead [[DONE]]
  # TODO: modify data to be the data object returned from db insertion

    error = False
    try:
      name = request.form.get('name','')
      city = request.form.get('city','')
      state = request.form.get('state','')
      phone = request.form.get('phone','')
      genres = request.form.get('genres','')
      facebook_link = request.form.get('facebook_link','') 
      image_link = request.form.get('image_link','')
      website_link = request.form.get('website_link','')
      seeking_description = request.form.get('seeking_description','')
    
      ven = Artist(name=name,genres=genres,city= city,state=state, phone=phone,website_link=website_link,image_link=image_link, facebook_link=facebook_link,seeking_description=seeking_description)
      db.session.add(ven)
      db.session.commit()


    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:  # TODO: on unsuccessful db insert, flash an error instead.
        flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
        abort (400)
    else:  # on successful db insert, flash success
       flash('Artist ' + request.form['name'] + ' was successfully listed!')
       return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():# [[DONE]] data yet
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
    #query = Task.query.filter(completed=True)
    #query.count()

  return render_template('pages/shows.html', shows=Show.query.all())

@app.route('/shows/search', methods=['POST'])
def search_shows():


    search_term = request.form.get('search_term', '')
    format = "%{}%".format(search_term)
    objects = Artist.name
    results = Artist.query.filter(objects.ilike(format)).all()

    return render_template('pages/search_shows.html', results=results, search_term=search_term,show=Show.query.all())

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission(): #[[DONE]] Data yet
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
    error = False
    try:
      Artist_id = request.form.get('artist_id','')
      venue_id =  request.form.get('venue_id','')
      start_date = request.form.get('start_time','')
      new = datetime.datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
      formatted = new.strftime('%Y-%m-%d %H:%M:%S')

      #start_date=start_date.strftime('%Y-%m-%d %H:%M:%S')
      sh = Show(Artist_id=Artist_id,venue_id = venue_id,start_date=formatted)
      db.session.add(sh)
      db.session.commit()
  
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        flash('An error occurred. Show could not be listed.')
        abort (400)
    else:
       flash('Show was successfully listed!')
       return render_template('pages/home.html')

  # on successful db insert, flash success
  #flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  #return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500



if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
