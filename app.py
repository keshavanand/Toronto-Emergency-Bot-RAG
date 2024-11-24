from flask import Flask, request, jsonify

# Create Flask app
app = Flask(__name__)

@app.route('/api/v1/hello', methods=['POST'])
def chat():
    data = request.get_json()
    print(data)
    return jsonify({'message': 'Hello World!'})

@app.route('/api/v1/chat', methods=['GET'])
def chat():
    text = request.get_json()
    #get text, get embemdings, compare embeddings, find similar, send to chatgpt, get response, return response to template
    # add logic to add chat history, change system message, etc
    # instead of csv use azure storage or vector database
    # do caching 


# Run Flask app
if __name__ == '__main__':
    app.run(debug=True)