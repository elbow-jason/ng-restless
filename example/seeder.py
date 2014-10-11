import requests
import time
import json
import logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

headers = {'Content-Type': 'application/json'}


def send_seed(api_endpoint, payload):
    url = 'http://localhost:5000/api/' + api_endpoint
    try:
        r = requests.post(url, data=json.dumps(payload),
                          headers=headers,
                          timeout=1)
        logger.info('post response status was ok:',
                    r.ok,
                    'for payload:',
                    payload
                    )

    except Exception as e:
        raise e



def seeder():
    with open('seeds.json', 'r') as f:
            seed_data = json.loads(f.read())
            for api_endpoint, seed_list in seed_data.items():
                for item in seed_list:
                    print api_endpoint, "is sent" , '\n', item
                    send_seed(api_endpoint, item)


def hobby_to_person():
    persons_hobbies = [
                        {"person_id": 1, "hobby_id": 1},
                        {"person_id": 1, "hobby_id": 2},
                        {"person_id": 2, "hobby_id": 1},
                        {"person_id": 2, "hobby_id": 2},
                        {"person_id": 2, "hobby_id": 3},
                        {"person_id": 3, "hobby_id": 1},
                        {"person_id": 3, "hobby_id": 3},
                        {"person_id": 4, "hobby_id": 4}
                      ]
    for item in persons_hobbies:
        get_and_put(item['hobby_id'], item['person_id'])


def add_hobby(person_dict, hobby_dict):
    del hobby_dict['persons']
    hobbies = person_dict['hobbies']
    hobbies.append(hobby_dict)
    return person_dict


def get_and_put(hobby_id, person_id):
    hobby_url = 'http://localhost:5000/api/hobby/{}'
    hobby_url = hobby_url.format(hobby_id)
    person_url = 'http://localhost:5000/api/person/{}'
    person_url = person_url.format(person_id)
    #person_rel = json.dumps({"persons_hobbies.hobby_id": hobby_id, "id":person_id})
    #hobby_rel = json.dumps({"persons_hobbies.person_id": person_id, "id":hobby_id})

    hobby_data  = requests.get(hobby_url,
                               headers=headers,
                               timeout=1)


    person_data = requests.get(person_url.format(person_id),
                               headers=headers,
                               timeout=1)

    person_data = person_data.json()
    hobby_data  = hobby_data.json()

    person_data['hobbies'].append(hobby_data)
    #person_json = json.dumps(add_hobby(person_data.json(), hobby_data.json()))

    """
    hobby  = requests.put(hobby_url.format(hobby_id),
        data=hobby_rel,
        headers={'Content-Type': 'application/json'},
        timeout=1)
    """

    person = requests.put(person_url.format(person_id),
        data=json.dumps(person_data),
        headers=headers,
        timeout=1)

    logger.debug(person.content)
    logger.debug(person.json())

if __name__ == '__main__':
    time.sleep(1)
    #try:
    seeder()
    hobby_to_person()
    logger.info('Seeded Database Successfully')
    logger.info('Exiting seeder...')

    #except Exception as e:
    #    logger.warning('Seeder Failed')
    #    raise e
