import random

def generate_sbox(secret_key: str):
    """
    Generates a deterministic 95-character S-box permutation 
    and its inverse based on a secret key/passphrase.
    """
    indices = list(range(95))
    rng = random.Random(secret_key)
    rng.shuffle(indices)
    
    forward = indices
    inverse = [0] * 95
    for std_idx, sub_idx in enumerate(indices):
        inverse[sub_idx] = std_idx
        
    return forward, inverse


def encrypt(plaintext, secret_key="SuperSecretPassphrase", initial_shift=45):
    forward, inverse = generate_sbox(secret_key)
    previous = initial_shift
    result = []

    for char in plaintext:
        std_val = ord(char) - 32
        if not 0 <= std_val < 95:
            raise ValueError(f"Unsupported character: {char!r}")

        # 1. Map through the keyed S-box substitution
        value = forward[std_val]

        # 2. Apply autokey arithmetic
        encrypted_val = (value + previous) % 95
        
        # 3. Map back through the inverse S-box to get the ciphertext character
        cipher_std_val = inverse[encrypted_val]
        result.append(chr(cipher_std_val + 32))
        
        # 4. Advance the rolling state using the substituted value
        previous = value

    return "".join(result)


def decrypt(ciphertext, secret_key="SuperSecretPassphrase", initial_shift=45):
    forward, inverse = generate_sbox(secret_key)
    previous = initial_shift
    result = []

    for char in ciphertext:
        std_val = ord(char) - 32
        if not 0 <= std_val < 95:
            raise ValueError(f"Unsupported character: {char!r}")

        # 1. Map ciphertext character through the keyed S-box
        cipher_val = forward[std_val]

        # 2. Reverse autokey arithmetic
        decrypted_val = (cipher_val - previous) % 95
        
        # 3. Map back through the inverse S-box to get the original plaintext index
        plain_std_val = inverse[decrypted_val]
        result.append(chr(plain_std_val + 32))
        
        # 4. Advance the rolling state using the recovered substituted value
        previous = decrypted_val

    return "".join(result)


# --- Test & Verification ---
message = 'test text'
secret = 'erxxdmjfirc6mk5dfrf86jsi'

encrypted = encrypt(message, secret_key=secret)
recovered = decrypt(encrypted, secret_key=secret)

assert recovered == message

print("Secret Key:", secret)
print("Encrypted:", encrypted)
print("Decrypted:", recovered)
print("Verified:", recovered == message)
