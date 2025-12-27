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

## 📦 Installation & Setup
To clone this project along with its dependencies:
```bash
git clone --recursive [https://github.com/Thomas170491/RSA-Key-Gen.git](https://github.com/Thomas170491/RSA-Key-Gen.git)
