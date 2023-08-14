
import os
from flask import Flask, request, redirect, url_for, send_from_directory, render_template, jsonify
from werkzeug.utils import secure_filename
import matplotlib.pyplot as plt
import numpy as np
import io
import base64

UPLOAD_FOLDER = 'D:/TYLresearch/nakagami_online/upload_data'
RESULT_FOLDER = 'D:/TYLresearch/nakagami_online/QUS/result'
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif', 'bin', 'mat', 'npy'])

app = Flask(__name__, static_folder='QUS/result')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = RESULT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def welcome():
    return render_template('welcome.html')


from flask import send_from_directory

from QUS.QUS_main import calc_image, QUS_fig_save

'''
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    uploaded_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    #upload file proc
    if filename.lower().endswith(('.mat')):
        
        paramap, bmode = calc_image(uploaded_path)
        

        #processed_image = np.flipud(RF)  # flip

        # Base64 encode
        buffered_image = io.BytesIO()
        plt.imsave(buffered_image, processed_image, format='png')
        buffered_image.seek(0)
        encoded_image = base64.b64encode(buffered_image.read()).decode()

        # HTML render
        return render_template('image_template.html', image_data=encoded_image)

    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/upload', methods=['GET', 'POST'])
def uploaded_file():
    if request.method == 'POST':
        # Get the uploaded file
        uploaded_file = request.files['file']

        # Save the uploaded file
        filename = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        uploaded_file.save(filename)

        # Process the uploaded file
        paramap, bmode = calc_image(filename)
        QUS_fig_save(paramap, bmode, './QUS/result/')

        # Encode the B-mode image
        buffered_image = io.BytesIO()
        plt.imsave(buffered_image, bmode, format='png', cmap='gray')
        buffered_image.seek(0)
        encoded_image = base64.b64encode(buffered_image.read()).decode()

        # Render the HTML template
        return render_template('image_template.html', image_data=encoded_image)
    

    return render_template('upload.html')  # Create an HTML form for uploading files

@app.route('/get_coordinates', methods=['POST'])
def get_coordinates():
    if request.method == 'POST':
        bmode_filename = './QUS/fan_b_img.png'
        bmode_image = plt.imread(bmode_filename)

        buffered_image = io.BytesIO()
        plt.imsave(buffered_image, bmode_image, format='png', cmap='gray')
        buffered_image.seek(0)
        encoded_bmode_image = base64.b64encode(buffered_image.read()).decode()

        # Encode the Paramap image
        paramap_filename = './QUS/fan_fusion_img.png'
        paramap = plt.imread(paramap_filename)

        buffered_paramap_image = io.BytesIO()
        plt.imsave(buffered_paramap_image, paramap, format='png', cmap='jet', vmin=0, vmax=2)
        buffered_paramap_image.seek(0)
        encoded_paramap_image = base64.b64encode(buffered_paramap_image.read()).decode()

        # Render the result template with the computed values and encoded images
        return render_template('result_template.html', computed_value=computed_value,
                               bmode_image=encoded_bmode_image, paramap_image=encoded_paramap_image)
'''


@app.route('/upload', methods=['GET', 'POST'])
def uploaded_file():
    if request.method == 'POST':
        # Get the uploaded file
        uploaded_file = request.files['file']

        # Save the uploaded file
        filename = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        uploaded_file.save(filename)

        # Process the uploaded file
        paramap, bmode = calc_image(filename)
        QUS_fig_save(paramap, bmode, './QUS/result/')

        # Calculate values after loading the images
        value1 = np.median(paramap[610:730, 30:95])
        value2 = np.median(paramap[730:850, 30:95])
        value3 = np.median(paramap[610:730, 95:160])
        value4 = np.median(paramap[730:850, 95:160])
        value_L = np.median(paramap[610:850, 30:160])

        # Load processed images
        paramap = plt.imread('./QUS/result/fan_b_img.png')
        bmode = plt.imread('./QUS/result/fan_fusion_img.png')



        return redirect(url_for('result', paramap_path='./QUS/result/fan_fusion_img.png', bmode_path='./QUS/result/fan_b_img.png', 
                                value1=value1, value2=value2, value3=value3, value4=value4, value_L=value_L))
    return render_template('upload.html')

@app.route('/result')
def result():
    paramap_path = request.args.get('paramap_path')
    bmode_path = request.args.get('bmode_path')
    value1 = request.args.get('value1')
    value2 = request.args.get('value2')
    value3 = request.args.get('value3')
    value4 = request.args.get('value4')
    value_L = request.args.get('value_L')

    return render_template('result.html', paramap_path=paramap_path, bmode_path=bmode_path, 
                           value1=value1, value2=value2, value3=value3, value4=value4, value_L=value_L)


'''
@app.route('/upload', methods=['GET', 'POST'])
def uploaded_file():
    if request.method == 'POST':
        # Get the uploaded file
        uploaded_file = request.files['file']

        # Save the uploaded file
        filename = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        uploaded_file.save(filename)

        # Process the uploaded file
        paramap, bmode = calc_image(filename)
        QUS_fig_save(paramap, bmode, './QUS/result/')

        value1 = np.median(paramap[30:95, 610:730])
        value2 = np.median(paramap[30:95, 730:850])
        value3 = np.median(paramap[95:160, 610:730])
        value4 = np.median(paramap[95:160, 730:850])

        paramap = plt.imread('./QUS/result/fan_b_img.png')
        bmode = plt.imread('./QUS/result/fan_fusion_img.png')

        return render_template('upload.html', paramap=paramap, bmode=bmode)
        
    return render_template('upload.html') 


@app.route('/result', methods=['POST'])
def show_result():
    point1 = request.form['point1']
    point2 = request.form['point2']

    # Perform calculations using point1 and point2 if needed
    # Load and process images from the 'QUS/result' folder
    image1_path = './QUS/result/fan_b_img.png'
    image2_path = './QUS/result/fan_fusion_img.png'
    calculated_value = '0.1'

    return render_template('result_template.html', image1_path=image1_path, image2_path=image2_path, calculated_value=calculated_value)


@app.route('/get_coordinates', methods=['POST'])
def get_coordinates():
    point1 = request.form['point1']
    point2 = request.form['point2']
    # Process the selected points' coordinates
    x1, y1 = map(int, point1.split(','))  # Convert string to integers
    x2, y2 = map(int, point2.split(','))  # Convert string to integers

    

    uploaded_filename = request.form['uploaded_filename']  # Get the uploaded filename
    uploaded_file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_filename)
    
    paramap, bmode = calc_image(uploaded_file_path)
    computed_value = np.median(paramap[x1:x2, y1:y2])
    
    # Perform further calculations based on the selected points' coordinates
    # and the processed image data
    
    # Encode the B-mode image
    buffered_image = io.BytesIO()
    plt.imsave(buffered_image, bmode, format='png', cmap='gray')
    buffered_image.seek(0)
    encoded_bmode_image = base64.b64encode(buffered_image.read()).decode()

    # Encode the Paramap image
    buffered_paramap_image = io.BytesIO()
    plt.imsave(buffered_paramap_image, paramap, format='png', cmap='jet', vmin=0, vmax=2)
    buffered_paramap_image.seek(0)
    encoded_paramap_image = base64.b64encode(buffered_paramap_image.read()).decode()

    # Render the result template with the computed values and encoded images
    return redirect(url_for('show_result', computed_value=computed_value,
                            bmode_image=encoded_bmode_image, paramap_image=encoded_paramap_image))

'''


if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug=True)