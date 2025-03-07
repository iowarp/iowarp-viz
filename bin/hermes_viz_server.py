from mock_mdm import MetadataSnapshot
from flask import Flask, jsonify
import threading
import time

mdm = MetadataSnapshot()
mdm.collect()

def periodic_collect():
    while True:
        mdm.collect()
        time.sleep(5)

app = Flask(__name__)

@app.route('/api/tags', methods=['GET'])
def get_tags():
    return jsonify(mdm.tag_info)

@app.route('/api/targets', methods=['GET'])
def get_targets():
    return jsonify(mdm.target_info)

@app.route('/api/blobs', methods=['GET'])
def get_blobs():
    return jsonify(mdm.blob_info)

if __name__ == '__main__':
    collect_thread = threading.Thread(target=periodic_collect, daemon=True)
    collect_thread.start()
    app.run(debug=True)
    