from flask import Flask, render_template, request
import exifread

app = Flask(__name__,template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    image = request.files['image']
    image.save('static/images/' + image.filename)

    with open('static/images/' + image.filename, 'rb') as f:
        tags = exifread.process_file(f)
        lat = tags.get('GPS GPSLatitude')
        lon = tags.get('GPS GPSLongitude')
        latitude = convert_to_degrees(lat)
        longitude = convert_to_degrees(lon)
        f_path = './static/images/' + image.filename
    
    return render_template('map.html', image_filename=image.filename, latitude=latitude, longitude=longitude,usr_img = f_path)

def convert_to_degrees(value):
    d = float(value.values[0].num) / float(value.values[0].den)
    m = float(value.values[1].num) / float(value.values[1].den)
    s = float(value.values[2].num) / float(value.values[2].den)
    return d + (m / 60.0) + (s / 3600.0)

if __name__ == '__main__':
    app.run(debug=True)
