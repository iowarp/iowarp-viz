from mock_mdm import MetadataSnapshot
from flask import Flask, jsonify

mdm = MetadataSnapshot()
mdm.collect()

app = Flask(__name__)

@app.route('/api/tags', methods=['GET'])
def get_tags():
    return jsonify(mdm.tags)

@app.route('/api/targets', methods=['GET'])
def get_targets():
    return jsonify(mdm.targets)

@app.route('/api/blobs', methods=['GET'])
def get_blobs():
    return jsonify(mdm.blobs)

if __name__ == '__main__':
    app.run(debug=True)