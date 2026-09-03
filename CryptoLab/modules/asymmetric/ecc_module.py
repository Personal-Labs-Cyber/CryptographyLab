from cryptography.hazmat.primitives.asymmetric import dh, ec
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.backends import default_backend
import base64

# Global parameters for demo purposes
# In a real app, these are generated securely or pre-shared
DH_PARAMETERS = dh.generate_parameters(generator=2, key_size=512, backend=default_backend())

def generate_dh_keys():
    """Generates DH private and public keys."""
    private_key = DH_PARAMETERS.generate_private_key()
    public_key = private_key.public_key()
    return private_key, public_key

def derive_shared_secret(private_key, peer_public_key):
    """Derives the shared secret using DH."""
    shared_key = private_key.exchange(peer_public_key)
    # Use HKDF to derive a symmetric key from the shared secret
    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'handshake data',
    ).derive(shared_key)
    return base64.b64encode(derived_key).decode('utf-8')

# We'll use a simplified class for the web demo
class DHSimulator:
    def __init__(self):
        self.alice_priv, self.alice_pub = generate_dh_keys()
        self.bob_priv, self.bob_pub = generate_dh_keys()

    def get_public_keys(self):
        # We'll just return arbitrary strings representing the public keys for the UI
        return {
            'alice_pub': "DH_PUB_ALICE_..." + str(hash(self.alice_pub))[:8],
            'bob_pub': "DH_PUB_BOB_..." + str(hash(self.bob_pub))[:8]
        }

    def compute_secrets(self):
        alice_shared = derive_shared_secret(self.alice_priv, self.bob_pub)
        bob_shared = derive_shared_secret(self.bob_priv, self.alice_pub)
        return alice_shared, bob_shared
