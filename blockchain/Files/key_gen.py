import nacl, nacl.secret, nacl.utils, nacl.pwhash, base64

kdf = nacl.pwhash.argon2i.kdf

salt_size = nacl.pwhash.argon2i.SALTBYTES
salt = nacl.utils.random(salt_size)

passw = "greekyogurt25".encode("utf-8")

key = kdf(nacl.secret.SecretBox.KEY_SIZE, passw, salt)

with open('key_file.bin', 'wb') as f:
    f.write(key)
