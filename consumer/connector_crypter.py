from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
import pathlib
import os

class Crypter:
    def generate_keys(self):
        key = RSA.generate(2048)
        private_key = key.export_key()
        with open("private.pem", "wb") as file_out:
            file_out.write(private_key)
        public_key = key.publickey().export_key()
        with open("receiver.pem", "wb") as file_out:
            file_out.write(public_key)

    def encrypt_config(self, file_name:str):
        out = "encrypted_"+str(file_name)
        with open(out, "wb") as file_out:
            with open(file_name,"r") as file_in:
                data = file_in.read().encode("utf-8")
            os.remove(file_name)
            public_key = None
            path = pathlib.Path("receiver.pem")
            if path.is_file():
                public_key = open("receiver.pem").read()
            else:
                return None
            recipient_key = RSA.import_key(public_key)
            session_key = get_random_bytes(16)
            # Encrypt the session key with the public RSA key
            cipher_rsa = PKCS1_OAEP.new(recipient_key)
            enc_session_key = cipher_rsa.encrypt(session_key)
            # Encrypt the data with the AES session key
            cipher_aes = AES.new(session_key, AES.MODE_EAX)
            ciphertext, tag = cipher_aes.encrypt_and_digest(data)
            [ file_out.write(x) for x in (enc_session_key, cipher_aes.nonce, tag, ciphertext) ]

    def decrypt_config(self, file_name:str, private_key="") -> str:
        file_in = open(file_name, "rb")
        key = None
        if private_key != "":
            key = RSA.import_key(private_key)
        else:
            path = pathlib.Path("private.pem")
            if path.is_file():
                key = RSA.import_key(open(path.read()))
            else:
                return None
        enc_session_key, nonce, tag, ciphertext = [ file_in.read(x) for x in (key.size_in_bytes(), 16, 16, -1) ]
        # Decrypt the session key with the private RSA key
        cipher_rsa = PKCS1_OAEP.new(key)
        session_key = cipher_rsa.decrypt(enc_session_key)
        # Decrypt the data with the AES session key
        cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
        data = cipher_aes.decrypt_and_verify(ciphertext, tag)
        return data.decode("utf-8")