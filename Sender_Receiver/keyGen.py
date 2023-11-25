from RSA import*

import json

def save_keys_to_file(public_key, private_key, p, q, filename="rsa_keys.json"):
    keys_data = {
        "public_key": public_key,
        "private_key": private_key,
        "p": p,
        "q": q
    }
    with open(filename, 'w') as file:
        json.dump(keys_data, file)

def load_keys_from_file(filename="rsa_keys.json"):
    with open(filename, 'r') as file:
        keys_data = json.load(file)
    return keys_data["public_key"], keys_data["private_key"], keys_data["p"], keys_data["q"]


public_key, private_key, p, q = generate_keys()
save_keys_to_file(public_key, private_key, p, q)
