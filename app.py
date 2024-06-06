import sys
print(sys.executable)

import PDFExtractor
from flask import Flask, request, jsonify, flash, redirect
from flask_restful import Api, Resource
from combined_lease_extractor import get_results
import json


app = Flask(__name__)
api= Api(app)
ALLOWED_EXTENSIONS = {'pdf'}


data_stored = {}

@app.route('/api/data', methods=['POST'])
def combined_api():
        app.logger.debug("Handling POST request")

        try:
            file = request.files['file']
            form_recognizer = request.form.get('form_recognizer')

            #use the doc intelligence model
            if form_recognizer == 'true':
                response = handle_form_recognizer(file)
            #use the gpt 4.o model
            else:
                filepath = ""
                file_stream = ""
                if request.method == 'POST':
                    # check if the post request has the file part
                    if 'file' not in request.files:
                        flash('No file part')
                        return redirect(request.url)
                    file = request.files['file']
                    # If the user does not select a file, the browser submits an
                    # empty file without a filename.
                    if file.filename == '':
                        flash('No selected file')
                        return redirect(request.url)
                    if file and allowed_file(file.filename):
                        file_stream = file.stream
                else:
                    # if given file path 
                    filepath = request.args.get('file')
                response = handle_pdf_extractor(filepath, file_stream)

            return response

        except Exception as e:
            app.logger.error(f"Error: {str(e)}")
            return jsonify({"error": str(e)}), 400
        

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def handle_form_recognizer(file):
    global data_stored

    try:    
        extracted_dict = get_results(file)

        app.logger.debug(f"Data Extracted: \t{extracted_dict}")
        data_stored = extracted_dict

        return jsonify(extracted_dict)

    except Exception as e:
        app.logger.error(f"Error in handle_form_recognizer: {str(e)}")
        return jsonify({"error": str(e)}), 400
    

def handle_pdf_extractor(filepath, file_stream):
    global data_stored

    try:
        response = PDFExtractor.upload_file(filepath, file_stream)  # Assuming you need to pass request_data
        data_stored = response

        return response

    except Exception as e:
        app.logger.error(f"Error in handle_pdf_extractor: {str(e)}")
        return jsonify({"error": str(e)}), 400



# def api_data(method, request_data):
#     global data_stored

#     if method == "POST":
#         app.logger.debug("Handling POST request")

#         try:
            
#             request_data = json.loads(request.data)

#             filepath = request_data['filepath']

#             extracted_dict = get_results(filepath)

#             app.logger.debug(f"Data Extracted: \t{extracted_dict}")

#             data_stored = extracted_dict

#             return jsonify(extracted_dict)
        
#         except Exception as e:
#             print(f"Error: {str(e)}")
#             return jsonify({"error": str(e)}), 400
        
#     elif method == "GET":
#         return jsonify(data_stored)
        


if __name__ == "__main__":
    app.run(debug=True, port=8000)
