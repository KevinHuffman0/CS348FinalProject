from flask import Flask, render_template, request, jsonify
from database import init_db, get_db_session
from models import Band, Album
import sqlite3
from sqlalchemy import func


app = Flask(__name__)

# Initialize the database
with app.app_context():
    init_db()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/reports")
def reports():
    sort_by = request.args.get("sort", "band_name")  # default sort
    session = get_db_session()

    # Build base query: join Band and Album
    query = session.query(Band, Album).join(Album, Band.band_id == Album.band_id)

    # Add sort order
    if sort_by == "band_name":
        query = query.order_by(Band.name)
    elif sort_by == "title":
        query = query.order_by(Album.title)
    elif sort_by == "release_year":
        query = query.order_by(Album.release_year)
    elif sort_by == "band_country":
        query = query.order_by(Band.country)

    results = query.all()
    session.close()

    return render_template("reports.html", data=results, sort_by=sort_by)

@app.route("/aggregation")
def aggregation():
    session = get_db_session()

    # 1. Count of bands per country
    bands_per_country = session.query(Band.country, func.count(Band.band_id)) \
                               .group_by(Band.country) \
                               .all()

    # 2. Count of albums per band
    albums_per_band = session.query(Band.name, func.count(Album.album_id)) \
                             .join(Album, Band.band_id == Album.band_id) \
                             .group_by(Band.band_id) \
                             .all()

    session.close()
    return render_template("aggregation.html",
                           bands_per_country=bands_per_country,
                           albums_per_band=albums_per_band)


# band routes
@app.route("/bands", methods=["GET"])
def get_bands():
    """Fetch all bands."""
    session = get_db_session()
    bands = session.query(Band).all()
    session.close()
    return jsonify([{"id": b.band_id, "name": b.name, "country": b.country} for b in bands])

@app.route("/add_band", methods=["POST"])
def add_band():
    """Add a new band."""
    data = request.json
    session = get_db_session()
    new_band = Band(name=data["name"], country=data["country"])
    session.add(new_band)
    session.commit()
    session.close()
    return jsonify({"message": "Band added successfully!"})

@app.route("/edit_band/<int:band_id>", methods=["PUT"])
def edit_band(band_id):
    """Edit an existing band."""
    data = request.json
    session = get_db_session()
    band = session.query(Band).filter_by(band_id=band_id).first()
    if band:
        band.name = data["name"]
        band.country = data["country"]
        session.commit()
        session.close()
        return jsonify({"message": "Band updated successfully!"})
    session.close()
    return jsonify({"error": "Band not found"}), 404

@app.route("/delete_band/<int:band_id>", methods=["DELETE"])
def delete_band(band_id):
    """Delete a band."""
    session = get_db_session()
    band = session.query(Band).filter_by(band_id=band_id).first()
    if band:
        session.delete(band)
        session.commit()
        session.close()
        return jsonify({"message": "Band deleted successfully!"})
    session.close()
    return jsonify({"error": "Band not found"}), 404

# album routes

@app.route('/albums', methods=['GET'])
def get_albums():
    try:
        # Connect to the SQLite database
        connection = sqlite3.connect('bands.db')
        cursor = connection.cursor()

        # Fetch all albums
        cursor.execute('SELECT album_id, title, release_year, band_id FROM albums')
        albums = cursor.fetchall()

        # Close the connection
        connection.close()
        # Format the response as JSON
        albums_list = [
            {
                "id": album[0],
                "title": album[1],
                "release_year": album[2],
                "band_id": album[3]
            }
            for album in albums
        ]

        # Return the albums as JSON
        return jsonify(albums_list), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/add_album', methods=['POST'])
def add_album():
    try:
        # Get data from the request
        data = request.get_json()
        title = data.get('title')
        release_year = data.get('release_year')
        band_id = data.get('band_id')

        # Check if all fields are provided
        if not title or not release_year or not band_id:
            return jsonify({'error': 'Missing required fields'}), 400

        # Connect to the SQLite database
        connection = sqlite3.connect('bands.db')
        cursor = connection.cursor()

        # Insert the new album into the albums table
        cursor.execute('''
            INSERT INTO albums (title, release_year, band_id) 
            VALUES (?, ?, ?)
        ''', (title, release_year, band_id))

        connection.commit()
        connection.close()
        return jsonify({'message': 'Album added successfully'}), 201

    except Exception as e:
        # Handle any errors
        return jsonify({'error': str(e)}), 500


@app.route("/edit_album/<int:album_id>", methods=["PUT"])
def edit_album(album_id):
    """Edit an existing album."""
    data = request.json
    session = get_db_session()
    album = session.query(Album).filter_by(album_id=album_id).first()
    if album:
        album.title = data["title"]
        album.release_year = data["release_year"]
        album.band_id = data["band_id"]
        session.commit()
        session.close()
        return jsonify({"message": "Album updated successfully!"})
    session.close()
    return jsonify({"error": "Album not found"}), 404

@app.route("/delete_album/<int:album_id>", methods=["DELETE"])
def delete_album(album_id):
    """Delete an album."""
    session = get_db_session()
    album = session.query(Album).filter_by(album_id=album_id).first()
    if album:
        session.delete(album)
        session.commit()
        session.close()
        return jsonify({"message": "Album deleted successfully!"})
    session.close()
    return jsonify({"error": "Album not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
