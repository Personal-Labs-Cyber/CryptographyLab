from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from functools import wraps
from classical import caesar, atbash, vigenere, playfair, affine, rail_fence
from modules.symmetric import aes
from modules.symmetric import advanced_sym
from modules.asymmetric import rsa_module
from modules.asymmetric import ecc_module
from modules.asymmetric import signatures
from modules.hashing import hash_module
from modules.attacks import bruteforce
from modules import pki_module
from modules import database

app = Flask(__name__)
app.secret_key = 'super_secret_cryptolab_key_for_viva'

# Initialize database
database.init_db()

# --- Decorators ---
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def study_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        if not session.get('study_completed'):
            # Double check DB in case session is stale
            if database.has_completed_study(session['user_id']):
                session['study_completed'] = True
            else:
                flash('You must complete the Study Mode before accessing the labs!', 'error')
                return redirect(url_for('study_view'))
        return f(*args, **kwargs)
    return decorated_function

# --- Auth Routes ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = database.login_user(username, password)
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['study_completed'] = user['study_completed']
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="Invalid username or password")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user_id = database.register_user(username, password)
        if user_id:
            session['user_id'] = user_id
            session['username'] = username
            session['study_completed'] = False
            return redirect(url_for('index'))
        else:
            return render_template('register.html', error="Username already exists")
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/complete_study', methods=['POST'])
@login_required
def complete_study():
    database.mark_study_completed(session['user_id'])
    session['study_completed'] = True
    return redirect(url_for('encryption_view'))

# --- Application Routes ---
# Dictionary to map cipher names to their modules
CIPHERS = {
    'caesar': {'name': 'Caesar Cipher', 'module': caesar, 'has_key': True, 'key_type': 'int'},
    'atbash': {'name': 'Atbash Cipher', 'module': atbash, 'has_key': False},
    'vigenere': {'name': 'Vigenère Cipher', 'module': vigenere, 'has_key': True, 'key_type': 'str'},
    'playfair': {'name': 'Playfair Cipher', 'module': playfair, 'has_key': True, 'key_type': 'str'},
    'affine': {'name': 'Affine Cipher', 'module': affine, 'has_key': True, 'key_type': 'tuple'},
    'rail_fence': {'name': 'Rail Fence Cipher', 'module': rail_fence, 'has_key': True, 'key_type': 'int'}
}

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/study')
@login_required
def study_view():
    return render_template('study.html')

@app.route('/encryption')
@study_required
def encryption_view():
    return render_template('encryption.html')

@app.route('/hashing')
@study_required
def hashing_view():
    return render_template('hashing.html')

@app.route('/attacks')
@study_required
def attacks_view():
    return render_template('attacks.html')

@app.route('/comparison')
@study_required
def comparison_view():
    return render_template('comparison.html')

@app.route('/advanced/symmetric')
@study_required
def adv_symmetric_view():
    return render_template('advanced_symmetric.html')

@app.route('/advanced/asymmetric')
@study_required
def adv_asymmetric_view():
    return render_template('advanced_asymmetric.html')

@app.route('/advanced/pki')
@study_required
def pki_view():
    return render_template('pki.html')

@app.route('/api/advanced/pki/fetch', methods=['POST'])
def api_adv_pki_fetch():
    data = request.json
    domain = data.get('domain')
    if not domain:
        return jsonify({'error': 'Domain required'}), 400
        
    res = pki_module.fetch_certificate(domain)
    if 'error' in res:
        return jsonify({'error': res['error']}), 400
    return jsonify(res)

@app.route('/api/advanced/asymmetric/dh', methods=['GET'])
def api_adv_dh():
    try:
        simulator = ecc_module.DHSimulator()
        pubs = simulator.get_public_keys()
        alice_sec, bob_sec = simulator.compute_secrets()
        
        return jsonify({
            'alice_pub': pubs['alice_pub'],
            'bob_pub': pubs['bob_pub'],
            'alice_secret': alice_sec,
            'bob_secret': bob_sec
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/advanced/asymmetric/sign', methods=['POST'])
def api_adv_sign():
    data = request.json
    msg = data.get('message')
    priv = data.get('private_key')
    try:
        sig = signatures.sign_data(msg, priv)
        return jsonify({'signature': sig})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/advanced/asymmetric/verify', methods=['POST'])
def api_adv_verify():
    data = request.json
    msg = data.get('message')
    pub = data.get('public_key')
    sig = data.get('signature')
    try:
        is_valid = signatures.verify_signature(msg, sig, pub)
        return jsonify({'valid': is_valid})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/advanced/symmetric', methods=['POST'])
def api_adv_symmetric():
    data = request.json
    cipher = data.get('cipher')
    text = data.get('text')
    key = data.get('key')
    
    if not text or not key:
        return jsonify({'error': 'Missing text or key'}), 400
        
    try:
        if cipher == 'ecb':
            res = advanced_sym.process_aes_ecb(text, key)
        elif cipher == 'gcm' or cipher == 'aes-gcm':
            res = advanced_sym.process_aes_gcm(text, key)
        elif cipher == 'chacha20':
            res = advanced_sym.process_chacha20(text, key)
        elif cipher == '3des':
            res = advanced_sym.process_3des(text, key)
        else:
            return jsonify({'error': 'Unknown cipher'}), 400
            
        return jsonify({'result': res})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/attacks/bruteforce', methods=['POST'])
def run_bruteforce():
    data = request.json
    ciphertext = data.get('ciphertext')
    
    if not ciphertext:
        return jsonify({'error': 'Ciphertext required'}), 400
        
    try:
        results = bruteforce.bruteforce_caesar(ciphertext)
        return jsonify({'results': results})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/asymmetric/rsa/keygen', methods=['GET'])
def rsa_keygen():
    try:
        priv, pub = rsa_module.generate_keypair()
        return jsonify({'private_key': priv, 'public_key': pub})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/asymmetric/rsa/process', methods=['POST'])
def rsa_process():
    data = request.json
    action = data.get('action')
    text = data.get('text')
    key = data.get('key')
    
    if not text or not key:
        return jsonify({'error': 'Missing text or key'}), 400
        
    try:
        if action == 'encrypt':
            result = rsa_module.rsa_encrypt(text, key)
            return jsonify({'result': result})
        elif action == 'decrypt':
            result = rsa_module.rsa_decrypt(text, key)
            return jsonify({'result': result})
        else:
            return jsonify({'error': 'Invalid action'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/hashing/process', methods=['POST'])
def hashing_process():
    data = request.json
    password = data.get('password')
    salt = data.get('salt', '')
    
    if not password:
        return jsonify({'error': 'Password required'}), 400
        
    try:
        # Run all three to compare
        sha256_hash, sha256_time = hash_module.hash_sha256(password)
        pbkdf2_hash, pbkdf2_time = hash_module.hash_pbkdf2(password, salt)
        bcrypt_hash, bcrypt_time = hash_module.hash_bcrypt(password)
        
        return jsonify({
            'sha256': {'hash': sha256_hash, 'time': round(sha256_time, 2)},
            'pbkdf2': {'hash': pbkdf2_hash, 'time': round(pbkdf2_time, 2)},
            'bcrypt': {'hash': bcrypt_hash, 'time': round(bcrypt_time, 2)}
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/symmetric/aes/keygen', methods=['GET'])
def aes_keygen():
    key, iv = aes.generate_key_iv()
    return jsonify({'key': key, 'iv': iv})

@app.route('/api/symmetric/aes/process', methods=['POST'])
def aes_process():
    data = request.json
    action = data.get('action')
    text = data.get('text', '')
    key = data.get('key')
    iv = data.get('iv')
    mode = data.get('mode', 'ECB')
    
    if not key or len(key) != 64: # 32 bytes = 64 hex chars
        return jsonify({'error': 'Invalid key length. Must be 64 hex characters (256-bit).'}), 400
        
    try:
        if action == 'encrypt':
            result = aes.encrypt_aes(text, key, mode, iv)
            return jsonify(result)
        elif action == 'decrypt':
            result = aes.decrypt_aes(text, key, mode, iv)
            return jsonify({'plaintext': result})
        else:
            return jsonify({'error': 'Invalid action'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/process', methods=['POST'])
def process_cipher():
    data = request.json
    cipher_id = data.get('cipher_id')
    action = data.get('action') # 'encrypt', 'decrypt', 'learn'
    text = data.get('text', '')
    
    if cipher_id not in CIPHERS:
        return jsonify({'error': 'Invalid cipher'}), 400
        
    info = CIPHERS[cipher_id]
    module = info['module']
    
    # Process key
    key = None
    if info['has_key']:
        raw_key = data.get('key')
        if not raw_key:
             return jsonify({'error': 'Key is required'}), 400
             
        try:
            if info['key_type'] == 'int':
                key = int(raw_key)
            elif info['key_type'] == 'str':
                key = str(raw_key)
            elif info['key_type'] == 'tuple':
                parts = raw_key.split(',')
                key = (int(parts[0].strip()), int(parts[1].strip()))
        except Exception as e:
            return jsonify({'error': 'Invalid key format'}), 400

    try:
        if action == 'encrypt':
            result = module.encrypt(text, key) if info['has_key'] else module.encrypt(text)
            return jsonify({'result': result})
        elif action == 'decrypt':
            result = module.decrypt(text, key) if info['has_key'] else module.decrypt(text)
            return jsonify({'result': result})
        else:
            return jsonify({'error': 'Invalid action'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response

if __name__ == '__main__':
    # Running in production mode (debug=False) for security
    app.run(host='127.0.0.1', port=5000, debug=False)
