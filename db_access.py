from flask_sqlalchemy import SQLAlchemy
from flask import Flask

# postgresql://ferkofodor:vYbU5PTZtOaIS31IG0NrTIYW4k6g8VAe@dpg-crg3lsaj1k6c739cbolg-a.frankfurt-postgres.render.com/cognitive_faces

# Initialize Flask app and SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///local.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Rating model
class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    image_index = db.Column(db.Integer, nullable=False)
    mood = db.Column(db.Integer, nullable=False)

# Function to query all ratings
def query_all_ratings():
    with app.app_context():
        ratings = Rating.query.all()
        for rating in ratings:
            print(f"ID: {rating.id}, Username: {rating.username}, Image Index: {rating.image_index}, Mood: {rating.mood}")

# Function to add a new rating
def add_rating(username, image_index, mood):
    with app.app_context():
        new_rating = Rating(username=username, image_index=image_index, mood=mood)
        db.session.add(new_rating)
        db.session.commit()
        print(f"Added rating for user {username}, image index {image_index}, mood {mood}")

# Function to delete all ratings for a specific user
def delete_ratings_by_user(username):
    with app.app_context():
        Rating.query.filter_by(username=username).delete()
        db.session.commit()
        print(f"Deleted all ratings for user {username}")

# Example usage
if __name__ == '__main__':
    # Query all ratings
    print("All Ratings:")
    query_all_ratings()