import ssl
import socket
from cryptography import x509
from cryptography.hazmat.backends import default_backend
import binascii

def fetch_certificate(hostname, port=443):
    """Fetches the SSL certificate from a domain and parses it using cryptography."""
    context = ssl.create_default_context()
    
    try:
        with socket.create_connection((hostname, port), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                # getpeercert(binary_form=True) returns DER encoded cert
                der_cert = ssock.getpeercert(binary_form=True)
                
                # Parse with cryptography library
                cert = x509.load_der_x509_certificate(der_cert, default_backend())
                
                # Extract Subject attributes
                subject = {}
                for attr in cert.subject:
                    subject[attr.oid._name] = attr.value
                    
                # Extract Issuer attributes
                issuer = {}
                for attr in cert.issuer:
                    issuer[attr.oid._name] = attr.value
                    
                # Format public key info
                pub_key = cert.public_key()
                pub_key_type = pub_key.__class__.__name__
                if hasattr(pub_key, 'key_size'):
                    pub_key_info = f"{pub_key_type} ({pub_key.key_size}-bit)"
                else:
                    pub_key_info = f"{pub_key_type} (Unknown size)"
                    
                fingerprint = binascii.hexlify(cert.fingerprint(cert.signature_hash_algorithm)).decode('utf-8').upper()
                formatted_fingerprint = ':'.join(fingerprint[i:i+2] for i in range(0, len(fingerprint), 2))
                
                return {
                    'subject': subject,
                    'issuer': issuer,
                    'serial_number': str(cert.serial_number),
                    'not_valid_before': cert.not_valid_before.isoformat(),
                    'not_valid_after': cert.not_valid_after.isoformat(),
                    'signature_algorithm': cert.signature_algorithm_oid._name,
                    'public_key': pub_key_info,
                    'fingerprint': formatted_fingerprint
                }
                
    except Exception as e:
        return {'error': str(e)}
