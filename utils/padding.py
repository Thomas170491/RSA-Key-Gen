import hashlib
import secrets

def mgf1(seed, length, hash_func=hashlib.sha256):
    mask = b""
    counter = 0
    while len(mask) < length:
        C = counter.to_bytes(4, byteorder='big')
        mask += hash_func(seed + C).digest()
        counter += 1
    return mask[:length]

def oaep_pad(message_bytes, k, label=b""):
    h_len = hashlib.sha256().digest_size
    if len(message_bytes) > k - 2 * h_len - 2:
        raise ValueError("Message too long")
    
    seed = secrets.token_bytes(h_len)
    l_hash = hashlib.sha256(label).digest()
    padding = b"\x00" * (k - len(message_bytes) - 2 * h_len - 2)
    db = l_hash + padding + b"\x01" + message_bytes
    
    db_mask = mgf1(seed, k - h_len - 1)
    masked_db = bytes(a ^ b for a, b in zip(db, db_mask))
    
    seed_mask = mgf1(masked_db, h_len)
    masked_seed = bytes(a ^ b for a, b in zip(seed, seed_mask))
    return b"\x00" + masked_seed + masked_db

def oaep_unpad(padded_bytes, k, label=b""):
    h_len = hashlib.sha256().digest_size
    masked_seed = padded_bytes[1:1+h_len]
    masked_db = padded_bytes[1+h_len:]
    
    seed_mask = mgf1(masked_db, h_len)
    seed = bytes(a ^ b for a, b in zip(masked_seed, seed_mask))
    
    db_mask = mgf1(seed, k - h_len - 1)
    db = bytes(a ^ b for a, b in zip(masked_db, db_mask))
    
    if db[:h_len] != hashlib.sha256(label).digest():
        raise ValueError("OAEP integrity check failed")
        
    separator_index = db.find(b"\x01", h_len)
    return db[separator_index + 1:]     