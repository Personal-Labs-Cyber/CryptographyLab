# 🔐 CryptoLab — Complete Project Documentation
### "Cryptographic Algorithm Demonstration & Security Analysis Toolkit"
### Final Year Cybersecurity Project

---

## 📅 Project Timeline — Starting se Lekar Ab Tak Kya Kya Kiya

---

### Phase 1: Classical Cryptography (Foundation)
**Goal:** Purane zamane ke ciphers implement karna — manually, bina library ke, taaki maths samajh aaye.

| Algorithm | File | Kya karta hai |
|-----------|------|---------------|
| Caesar Cipher | `classical/caesar.py` | Har letter ko fixed number se shift karta hai (e.g., A+3=D) |
| Atbash Cipher | `classical/atbash.py` | Alphabet ulta karta hai (A↔Z, B↔Y) — koi key nahi chahiye |
| Vigenère Cipher | `classical/vigenere.py` | Multiple Caesar ciphers — har letter ka shift alag keyword se aata hai |
| Playfair Cipher | `classical/playfair.py` | 5×5 grid based — 2-2 letters ke pairs encrypt hote hain |
| Affine Cipher | `classical/affine.py` | Math formula: E(x) = (a*x + b) mod 26 |
| Rail Fence Cipher | `classical/rail_fence.py` | Zigzag pattern mein likhte hain, phir rows padh ke ciphertext banate hain |

**Result:** 6 classical ciphers with encrypt + decrypt + study mode + flowcharts ✅

---

### Phase 2: Modern Symmetric Encryption (AES)
**Goal:** Real-world encryption standard implement karna using Python `cryptography` library.

| Feature | File | Kya karta hai |
|---------|------|---------------|
| AES-256-CBC | `modules/symmetric/aes.py` | 256-bit key + IV se encrypt/decrypt karta hai |
| Key Generation | API `/api/symmetric/aes/keygen` | Random secure key + IV generate karta hai |
| AES Modes | `modules/symmetric/advanced_sym.py` | ECB, GCM modes + ChaCha20 + 3DES support |

**Result:** AES with key gen, CBC mode, and multiple cipher support ✅

---

### Phase 3: Asymmetric Cryptography (RSA)
**Goal:** Public-Private key pair ka concept implement karna.

| Feature | File | Kya karta hai |
|---------|------|---------------|
| RSA-2048 Key Generation | `modules/asymmetric/rsa_module.py` | 2048-bit public/private key pair banata hai |
| RSA Encrypt/Decrypt | Same file | Public key se encrypt, private key se decrypt |
| Diffie-Hellman | `modules/asymmetric/ecc_module.py` | Alice aur Bob ke beech secure key exchange simulate karta hai |
| Digital Signatures | `modules/asymmetric/signatures.py` | RSA-PSS se document sign/verify karta hai |

**Result:** RSA + DH Key Exchange + Digital Signatures ✅

---

### Phase 4: Hashing & Password Security
**Goal:** Hash functions ka comparison dikhana — SHA-256 (fast, weak for passwords) vs PBKDF2 vs bcrypt (slow, strong).

| Feature | File | Kya karta hai |
|---------|------|---------------|
| SHA-256 | `modules/hashing/hash_module.py` | Fast hash — milliseconds mein compute hota hai |
| PBKDF2 | Same file | 100,000 iterations — slow & secure for passwords |
| bcrypt | Same file | Built-in salt — password hashing ka gold standard |
| Performance Comparison | `/hashing` page | Teeno ka time (ms) side-by-side compare karta hai |

**Result:** Hash comparison with live timing metrics ✅

---

### Phase 5: Advanced Symmetric Lab (ECB Visualizer + ChaCha20)
**Goal:** ECB mode ki vulnerability visually dikhana, aur modern ciphers add karna.

| Feature | File/Page | Kya karta hai |
|---------|-----------|---------------|
| ECB Pattern Leakage | `/advanced/symmetric` | Dikhata hai ki identical blocks → identical ciphertext (INSECURE!) |
| AES-GCM | `modules/symmetric/advanced_sym.py` | Authenticated encryption — tamper-proof |
| ChaCha20-Poly1305 | Same file | Modern stream cipher — fast + authenticated |
| 3DES (Legacy) | Same file | Historical comparison — slow & outdated |
| Authenticated Encryption Explanation | UI panel | Explains: Encryption ≠ Authentication |

**Result:** ECB vulnerability visualizer + 3 modern ciphers + auth encryption education ✅

---

### Phase 6: Advanced Asymmetric Lab (DH + Signatures)
**Goal:** Interactive key exchange simulator aur digital signature verification lab banana.

| Feature | Page | Kya karta hai |
|---------|------|---------------|
| Diffie-Hellman Simulator | `/advanced/asymmetric` | Alice & Bob public values exchange karke same secret generate karte hain |
| RSA Digital Signatures | Same page | Document sign karo → modify karo → verify fail hota hai! |

**Result:** Live DH key exchange + Interactive signature tampering demo ✅

---

### Phase 7: PKI & Digital Certificates
**Goal:** Real-world HTTPS ka connection dikhana — Google.com ka asli certificate fetch karke inspect karna.

| Feature | File | Kya karta hai |
|---------|------|---------------|
| Live Certificate Fetch | `modules/pki_module.py` | Kisi bhi domain (google.com) ka SSL certificate download karta hai |
| Certificate Inspector | `/advanced/pki` | Subject, Issuer, Validity, Public Key, Signature Algorithm, Fingerprint dikhata hai |
| TLS/HTTPS Explanation | UI panel | Samjhata hai ki Handshake → Verification → Key Exchange → Secure Channel kaise kaam karta hai |

**Result:** Live PKI certificate inspector + TLS education ✅

---

### Phase 8: Attack Lab (Cryptanalysis)
**Goal:** Controlled educational demos — ciphers ko todna sikhana.

| Feature | File | Kya karta hai |
|---------|------|---------------|
| Caesar Brute Force | `modules/attacks/bruteforce.py` | All 25 shifts try karta hai + dictionary scoring se best guess dikhata hai |
| Attack Lab UI | `/attacks` | Ciphertext paste karo → automated brute force results dikhata hai |

**Result:** Caesar brute force with scoring heuristic ✅

---

### Phase 9: Interactive Study Mode (Visual Flowcharts)
**Goal:** Har algorithm ka step-by-step visual flowchart banana — boxes, arrows, data flow, aur Hinglish code comments.

| Feature | Page | Kya karta hai |
|---------|------|---------------|
| Dedicated Study Page | `/study` | Caesar, AES, RSA, SHA-256 ke flowcharts ek jagah |
| Inline Study Mode | Encryption page (right panel) | Har algorithm ke liye: Input Box → Process Box → Output Box + Step-by-step breakdown + Python code with Hinglish comments |
| Study Lock | All lab pages | Jab tak Study Mode complete nahi karoge, labs unlock nahi honge! |

**Result:** 8 algorithm flowcharts + Hinglish code explanations + progress gate ✅

---

### Phase 10: User Authentication & Database
**Goal:** Local SQLite database se login system banana — progress track karna.

| Feature | File | Kya karta hai |
|---------|------|---------------|
| SQLite Database | `modules/database.py` + `users.db` | Users table (id, username, password_hash, study_completed) |
| Login Page | `templates/login.html` | Dark-themed login wall |
| Registration | `templates/register.html` | New account create karo — password securely hashed |
| Route Protection | `app.py` (`@login_required`, `@study_required`) | Bina login ke koi page accessible nahi, bina study ke labs locked |
| User Profile | Sidebar | Username, avatar, "Labs Locked/Unlocked" status dikhata hai |
| Logout | `/logout` | Session clear karke login page pe bhejta hai |

**Result:** Full auth system with SQLite + study progress tracking ✅

---

### Phase 11: Security Hardening
**Goal:** Project khud secure hona chahiye — cybersecurity project hai!

| Feature | Where | Kya karta hai |
|---------|-------|---------------|
| Security Headers | `app.py` (`@after_request`) | X-Content-Type-Options, X-Frame-Options, X-XSS-Protection, HSTS |
| Debug Mode Off | `app.py` | `debug=False` — Werkzeug debugger disabled |
| Secure Password Hashing | `modules/database.py` | `werkzeug.security.generate_password_hash` used |
| Secure Random Salts | `modules/hashing/hash_module.py` | `os.urandom(16)` instead of hardcoded salt |

**Result:** Production-grade security headers + secure password storage ✅

---

## 📁 Final Project Structure

```
CryptoLab/
├── app.py                          # Main Flask controller (all routes + auth)
├── users.db                        # SQLite database (auto-generated)
├── requirements.txt                # Python dependencies
│
├── classical/                      # Phase 1: Classical Ciphers
│   ├── caesar.py
│   ├── atbash.py
│   ├── vigenere.py
│   ├── playfair.py
│   ├── affine.py
│   └── rail_fence.py
│
├── modules/                        # Phase 2-10: Modern Modules
│   ├── database.py                 # SQLite auth logic
│   ├── pki_module.py               # PKI certificate fetcher
│   ├── symmetric/
│   │   ├── aes.py                  # AES-256-CBC
│   │   └── advanced_sym.py         # ECB, GCM, ChaCha20, 3DES
│   ├── asymmetric/
│   │   ├── rsa_module.py           # RSA-2048
│   │   ├── ecc_module.py           # Diffie-Hellman
│   │   └── signatures.py           # Digital Signatures
│   ├── hashing/
│   │   └── hash_module.py          # SHA-256, PBKDF2, bcrypt
│   └── attacks/
│       └── bruteforce.py           # Caesar brute force
│
├── templates/                      # HTML UI Pages
│   ├── base.html                   # Shared layout (sidebar + nav)
│   ├── login.html                  # Login wall
│   ├── register.html               # Registration
│   ├── index.html                  # Dashboard
│   ├── study.html                  # Interactive Study Mode
│   ├── encryption.html             # Unified Encryption Workspace
│   ├── hashing.html                # Hash Comparison
│   ├── attacks.html                # Attack Lab
│   ├── comparison.html             # Algorithm Comparison Table
│   ├── advanced_symmetric.html     # ECB Visualizer + Modern Ciphers
│   ├── advanced_asymmetric.html    # DH + Digital Signatures
│   └── pki.html                    # Certificate Inspector
│
└── static/
    └── css/
        └── style.css               # Global dark-theme styling
```

---

## 🛠 Tech Stack

| Technology | Purpose |
|------------|---------|
| **Python 3** | Backend logic |
| **Flask** | Web framework + routing |
| **SQLite3** | Local user database |
| **cryptography** | AES, RSA, DH, Signatures, x509 parsing |
| **bcrypt** | Password hashing |
| **werkzeug** | Secure password hashing for auth |
| **HTML/CSS/JS** | Frontend UI |
| **Font Awesome** | Icons |
| **Google Fonts (Inter, JetBrains Mono)** | Typography |

---

## 🎯 Viva Presentation Flow (Recommended)

1. **Login Page** — Show the auth system
2. **Study Mode** — Show flowcharts → Click "Unlock Labs"
3. **Caesar Cipher** — Encrypt "HELLO" with key 3 → Show study mode panel
4. **AES-256** — Generate key → Encrypt → Decrypt
5. **RSA** — Generate keypair → Encrypt with public → Decrypt with private
6. **Hashing** — Compare SHA-256 vs PBKDF2 vs bcrypt timing
7. **Attack Lab** — Brute force a Caesar ciphertext
8. **ECB Visualizer** — Show pattern leakage vulnerability
9. **Digital Signatures** — Sign → Modify text → Verify fails!
10. **PKI Certificate** — Inspect google.com live certificate
11. **Grand Finale** — Explain how all these concepts combine to secure HTTPS!

---

**Project by:** Sumit  
**Date:** September 2026  
**Status:** ✅ COMPLETE & READY FOR VIVA
