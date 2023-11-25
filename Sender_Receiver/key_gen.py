from RSA import generate_keys
from Crypto.PublicKey import RSA

def save_keys_to_pem(public_key_components, private_key_components, p, q):
    public_key = RSA.construct((public_key_components[1], public_key_components[0]))
    private_key = RSA.construct((private_key_components[1], public_key_components[0], private_key_components[0], p, q))

    with open('public.pem', 'wb') as pub_file:
        pub_file.write(public_key.export_key())

    with open('private.pem', 'wb') as priv_file:
        priv_file.write(private_key.export_key())


if __name__ == "__main__":
    pu, pr, p, q = generate_keys()
    save_keys_to_pem(pu, pr, p, q)