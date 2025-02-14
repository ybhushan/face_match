from flask import Flask, render_template, request, redirect, url_for
import os
from fs_module import *

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_images():
    
    if request.method == 'POST':
        images = []
        file_for_check = []
        for key in ['image1', 'image2']:
            file = request.files.get(key)
            
            if file and file.filename != '':
                if allowed_file(file.filename):
                    try:
                        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                        
                        file.save(filepath)
                        images.append(file.filename)
                        file_for_check.append(filepath)
                    except Exception as e:
                        return render_template('index.html', images=None, error=f"Error uploading {file.filename}: {str(e)}" ,result=None)
                else:
                    return render_template('index.html', images=None, error=f"Invalid file type for {file.filename}" ,result=None)
        print(file_for_check)
        result = check_similarity(file_for_check[0],file_for_check[1])
        return render_template('index.html', images=images ,result=result)
    return render_template('index.html', images=None, error=None ,result=None)

if __name__ == '__main__':
    app.run(debug=True)
