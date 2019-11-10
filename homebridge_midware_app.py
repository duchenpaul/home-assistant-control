# A midware to connect homeassistant to homebridge

#!/usr/bin/env python3
import logging
import logging_manager

import time

from flask import Flask, render_template, make_response, request
from flask_compress import Compress

import homeassistant

app = Flask(__name__)

compress = Compress()


@app.route('/')
def index_html():
    print('Index')
    response_msg, code = 'API looks good', 200
    return response_msg, code


@app.route('/midware/<entity_id>', methods=['POST', 'GET'])
# e.g.: http://localhost:5001/midware/switch.phicomm_dc1_switch0?action=on
def api(entity_id):
    try:
        if request.method == 'GET':
            action = request.args.get('action', default = 'toggle', type = str)
            logging.info('entity_id: {}'.format(entity_id))
            logging.info('action: {}'.format(action))

            if action in ['on', 'off']:
                homeassistant.switch_control(entity_id, action=action)
                time.sleep(1)
            response_msg = str(homeassistant.switch_status(entity_id))
        else:
            response_msg, code = 'Method not allowed', 405
    except Exception as e:
        logging.error('Method: {}'.format(request.method))
        logging.error('url: {}'.format(request.url))
        logging.error('Message: {}'.format(request.get_data().decode()))
        logging.exception("Failed to handle this post")
        response_msg, code = 'Error', 500
    else:
        response_msg, code = response_msg, 200
    finally:
        return response_msg, code


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
    compress.init_app(app)
