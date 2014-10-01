
import requests, time, json

def send_seed(api_endpoint, payload):
    url = 'http://localhost:5000/api/' + api_endpoint
    try:
        r = requests.post(url, data=json.dumps(payload), headers={'Content-Type': 'application/json'}, timeout=1)
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
        get_and_post(item['hobby_id'], item['person_id'])


def add_hobby(person_dict, hobby_dict):
    del hobby_dict['persons']
    hobbies = person_dict['hobbies']
    hobbies.append(hobby_dict)
    return person_dict



def get_and_post(hobby_id, person_id):
    hobby_url   = 'http://localhost:5000/api/hobby/{}'
    person_url  =  'http://localhost:5000/api/person/{}'
    
    hobby_data  = requests.get(hobby_url.format(hobby_id),
        headers={'Content-Type': 'application/json'},
        timeout=1)

    person_data = requests.get(person_url.format(person_id),
        headers={'Content-Type': 'application/json'},
        timeout=1)

    person_json = json.dumps(add_hobby(person_data.json(), hobby_data.json()))


    person = requests.put(person_url.format(person_id),
        data=person_json,
        headers={'Content-Type': 'application/json'},
        timeout=1)


if __name__ == '__main__':
    time.sleep(1)
    try:
        seeder()
        hobby_to_person()
    except:
        pass
