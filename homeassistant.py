import logging 
import logging_manager
import requests
import json

import toolkit_config

config_file = 'config.ini'

config = toolkit_config.read_config_general(configFile=config_file)
API_URL = config['home assistant']['api_url']
TOKEN = config['home assistant']['token']


headers = {
    'Authorization': 'Bearer ' + TOKEN,
    'content-type': 'application/json',
}

def switch_control(entity_id, action='toggle'):
    # action can be: on, off, toggle
    if action == 'on':
        action = 'turn_on'
    elif action == 'off':
        action = 'turn_off'
    else:
        action = 'toggle'

    logging.info('Entity: {}'.format(entity_id))
    logging.info('Action: {}'.format(action))

    ENDPOINT = '/api/services/switch/' + action
    ENDPOINT = ENDPOINT.strip()
    ENDPOINT = '/' + ENDPOINT if not ENDPOINT.startswith('/') else ENDPOINT

    data = {'entity_id': entity_id}

    response = requests.post(API_URL + ENDPOINT, headers=headers, data=json.dumps(data), timeout=5)
    api_resp = response.text
    print(api_resp)

    try:
        assert api_resp == '[]'
    except Exception as e:
        logging.error("Failed to do the action")
        logging.error('Response: {}'.format(api_resp))
        logging.exception('Raise: ', e)
    else:
        logging.info('Success')
    finally:
        pass


def switch_status(entity_id):
    ENDPOINT = '/api/states/<entity_id>'.replace('<entity_id>', entity_id)
    logging.info('Check the status: {}'.format(entity_id))

    try:
        response = requests.get(API_URL + ENDPOINT, headers=headers, timeout=5)
        api_resp = response.text
        logging.error('Response: {}'.format(api_resp))
        resp_dict = json.loads(api_resp)
        logging.info('Status: {}'.format(resp_dict['state']))
    except Exception as e:
        logging.error('Response: {}'.format(api_resp))
        logging.exception('Raise: ', e)

    if resp_dict['state'] == 'off':
        return 0
    elif resp_dict['state'] == 'on':
        return 1


if __name__ == '__main__':
    import time

    for x in range(4):
        time.sleep(2)
        entity_id = 'switch.phicomm_dc1_switch' + str(x)
        print('----------------------------')
        print(entity_id)
        switch_control(entity_id, action='toggle')
        status = switch_status(entity_id)
        print(status)
