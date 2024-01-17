from flask import Flask, request, jsonify

app = Flask(__name__)
save_path = "../results/downloaded_file.zip"


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        file.save(save_path)
        response_data = {'message': 'File saved!'}

        # Creating a Flask response with a 200 status code
        response = jsonify(response_data)
        response.status_code = 200
        return response


if __name__ == '__main__':
    app.run(debug=True, port=8001)
