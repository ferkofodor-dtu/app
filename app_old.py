from flask import Flask, render_template, url_for, request, redirect, session
import os

app = Flask(__name__)
app.secret_key = 'some_secret_key'  # Needed for session handling

# Folder where images are stored
IMAGE_FOLDER = os.path.join('static', 'images')

@app.route('/')
@app.route('/<int:image_index>')
def index(image_index=0):
    # List all images in the folder
    image_list = os.listdir(IMAGE_FOLDER)
    total_images = len(image_list)
    
    # Make sure the index is within bounds
    if image_index < 0:
        image_index = 0
    elif image_index >= total_images:
        image_index = total_images - 1
    
    # Load the current image
    current_image = url_for('static', filename=f'images/{image_list[image_index]}')
    
    # Initialize session for rated images if it doesn't exist
    if 'rated_images' not in session:
        session['rated_images'] = []
    
    # Calculate progress based on rated images
    progress = session.get('progress', 0)
    
    # Check if the user is on the last image
    is_last_image = True
    
    # Render the image and pass progress, image index, etc.
    return render_template('index.html', 
                           image=current_image, 
                           image_index=image_index, 
                           total_images=total_images, 
                           progress=progress,
                           is_last_image=is_last_image)

@app.route('/rate', methods=['POST'])
def rate():
    # Get the rating and the current image index
    rating = request.form['mood']
    image_index = int(request.form['image_index'])
    
    # Track rated images in the session
    if 'rated_images' not in session:
        session['rated_images'] = []

    if 'ratings' not in session:
        session['ratings'] = []
    
    # Add current image to rated_images if not already rated
    if image_index not in session['rated_images']:
        session['rated_images'].append(image_index)
        progress = len(session['rated_images']) / len(os.listdir(IMAGE_FOLDER)) * 100
        session['progress'] = progress
        session['ratings'].append(rating)
    
    # Print the rating and image index (for debug purposes)
    # print(f'User rated image {image_index} with a mood of: {rating}')
    print(f'Rated images: {session["rated_images"]}')
    print(f"Ratings: {session['ratings']}")

    
    # Redirect to the next image or stay on the same one
    if image_index < len(os.listdir(IMAGE_FOLDER)) - 1:
        return redirect(f'/{image_index + 1}')
    else:
        return redirect(f'/{image_index}')  # Stay on the last image

@app.route('/reset', methods=['POST'])
def reset():
    # Clear rated images for testing purposes
    # session.pop('rated_images', None)
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
