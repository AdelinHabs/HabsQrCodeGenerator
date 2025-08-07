from flask import Flask, render_template, request
from qrcode import QRCode, constants
import os
import re

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/generated_qr'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_qr():
    data = request.form.get('qrdata', '').strip()

    if not data:
        error = "Please enter some text or a URL."
        return render_template('index.html', error=error)

    try:
        # Sanitize filename
        safe_name = re.sub(r'[^a-zA-Z0-9_-]', '', data[:10])
        filename = f"qr_{safe_name}.jpg"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # Create QR code object
        qr = QRCode(
            version=1,
            box_size=10,
            error_correction=constants.ERROR_CORRECT_H,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        # Create and save image
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(filepath)

        return render_template('download.html', qr_image=f"generated_qr/{filename}")

    except Exception as e:
        error = f"Error generating QR code: {str(e)}"
        return render_template('download.html', error=error)

if __name__ == '__main__':
    import os
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(host='0.0.0.0', port=10000)

