#!/usr/bin/env python

import os

from flask import Flask, request, Response, render_template

from signer import CertificateGenerator

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_certificate():
    cert_generator = CertificateGenerator(2048, request.form)
    response = ''.join([cert_generator.certificate, cert_generator.private_key])
    return Response(response, mimetype='text/plain')

if __name__ == '__main__':
    port = int(os.environ.get('FLASK_PORT', 5555))
    app.run(host='0.0.0.0', port=port)
