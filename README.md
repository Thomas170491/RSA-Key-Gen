# RSA Key Generator

A modular implementation of the RSA (Rivest–Shamir–Adleman) cryptosystem, powered by a custom-built Miller-Rabin Primality Test engine.

## 🛠 Architecture
This project is designed with **Separation of Concerns**. The core mathematical primitives are maintained in a separate repository and integrated here as a Git Submodule.

* **RSA Logic:** Handles keypair generation $(e, n)$ and $(d, n)$ using the Extended Euclidean Algorithm.
* **Math Engine:** [Prime-Logic-MillerRabin](https://github.com/Thomas170491/Prime-Logic-MillerRabin) - used for cryptographically secure prime generation.

## 🚀 Features
- **Secure Randomness:** Uses Python's `secrets` module for industry-standard entropy.
- **Miller-Rabin Primality Test:** Implements probabilistic testing to find large 1024-bit primes.
- **Modular Inverse:** Calculates the private exponent $d$ using the Extended Euclidean Algorithm.


## 🧮 Mathematical Background

The security of RSA is based on the **Integer Factorization Problem**. While it is computationally easy to multiply two large prime numbers, it is functionally impossible to factor the result back into the original primes using classical computers.

### 1. Key Generation
The algorithm follows these mathematical steps:

1.  **Select Primes:** Choose two distinct large primes, $p$ and $q$ (verified via our **Miller-Rabin** engine).
2.  **Compute Modulus ($n$):** $$n = p \times q$$
    The bit-length of $n$ defines the "key size."
3.  **Compute Euler's Totient ($\phi(n)$):**
    $$\phi(n) = (p - 1)(q - 1)$$
4.  **Choose Public Exponent ($e$):** We use $65537$ (the 4th Fermat prime) as it is the industry standard for balancing speed and security. It must satisfy:
    $$1 < e < \phi(n) \text{ and } \gcd(e, \phi(n)) = 1$$
5.  **Compute Private Exponent ($d$):** This is the modular multiplicative inverse of $e$ modulo $\phi(n)$. We calculate this using the **Extended Euclidean Algorithm**:
    $$d \cdot e \equiv 1 \pmod{\phi(n)}$$



### 2. Encryption & Decryption
RSA uses modular exponentiation to transform data. 

* **Encryption:** To encrypt a message $M$, we calculate the ciphertext $C$:
    $$C = M^e \pmod{n}$$
* **Decryption:** To recover the message, we use the private key $d$:
    $$M = C^d \pmod{n}$$



### 3. Proof of Correctness
The decryption works because of **Euler's Theorem**. Since $d$ is the modular inverse of $e \pmod{\phi(n)}$, we know that $ed = 1 + k\phi(n)$ for some integer $k$. Therefore:

$$C^d \equiv (M^e)^d \equiv M^{ed} \equiv M^{1 + k\phi(n)} \equiv M \cdot (M^{\phi(n)})^k \equiv M \cdot 1^k \equiv M \pmod{n}$$

## 🛡️ Security Considerations

### Why OAEP Padding?
This implementation uses **RSA-OAEP (Optimal Asymmetric Encryption Padding)** rather than "Textbook RSA." In a production environment, Textbook RSA is vulnerable to several attacks:

1. **Deterministic Encryption:** Without padding, the same plaintext always produces the same ciphertext. This allows attackers to perform frequency analysis or use "rainbow tables" to guess messages. OAEP introduces a random **seed** for every encryption, ensuring probabilistic encryption.
2. **Malleability:** RSA is mathematically malleable; an attacker could potentially modify the ciphertext in a way that creates a predictable change in the plaintext. OAEP's **Feistel Network** structure ensures that any tampering with the ciphertext results in an invalid decryption.
3. **Small Exponent Attacks:** If a message is small, an attacker might be able to recover it by taking the $e$-th root. OAEP pads the message to the full length of the modulus, neutralizing this risk.

### Implementation Details
- **Hash Function:** SHA-256 is used for both the mask generation function (MGF1) and the label hashing.
- **Entropy:** We utilize Python's `secrets` module (instead of `random`) to ensure cryptographically secure random seeds.
- **Side-Channel Resistance:** While this is a software implementation, the modular exponentiation uses Python's built-in `pow(m, e, n)`, which is optimized for efficiency.

## 📦 Installation & Setup
To clone this project along with its dependencies:
```bash
git clone --recursive [https://github.com/Thomas170491/RSA-Key-Gen.git](https://github.com/Thomas170491/RSA-Key-Gen.git)
```

This project is open-source and available under the MIT License. SeeLICENSE file for more info.