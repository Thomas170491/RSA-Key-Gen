import os 
import sys 

sys.path.append(os.path.join(os.getcwd(), 'lib', 'math_engine'))

from src import generate_prime

def extended_gcd(a, b):
    """Returns (gcd, x, y) such that ax + by = gcd(a, b)"""
    if a == 0:
        return b, 0, 1
    d, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return d, x, y

def mod_inverse(e, phi):
    """Calculates the modular multiplicative inverse of e mod phi"""
    d, x, y = extended_gcd(e, phi)
    if d != 1:
        raise ValueError("Modular inverse does not exist")
    return x % phi

def generate_rsa_keys(bits=1024):
    print(f"[*] Generating a {bits}-bit RSA Keypair...")
    
    # Using Miller-Rabin library for prime generation
    p = generate_prime(bits)
    q = generate_prime(bits)
    
    n = p * q
    phi = (p - 1) * (q - 1)
    
    # Industry standard public exponent
    e = 65537
    
    # Calculating the private exponent
    d = mod_inverse(e, phi)
    
    return (e, n), (d, n)

def main():
    try:
        public, private = generate_rsa_keys(1024)
        
        print("\n" + "="*50)
        print("RSA KEY GENERATION SUCCESSFUL")
        print("="*50)
        print(f"Public Key (e, n): \ne: {public[0]} \nn: {hex(public[1])[:60]}...")
        print("-" * 50)
        print(f"Private Key (d, n): \nd: {hex(private[0])[:60]}...")
        print("="*50)
        
        # Simple proof of concept: Encryption/Decryption
        message = 123456789
        cipher = pow(message, public[0], public[1])
        decrypted = pow(cipher, private[0], private[1])
        
        print(f"\nVerifying math: Original {message} -> Decrypted {decrypted}")
        if message == decrypted:
            print("[STATUS] RSA Math Verified: Success!")

    except Exception as error:
        print(f"[ERROR] {error}")

if __name__ == "__main__":
    main()
                
