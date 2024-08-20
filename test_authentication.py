import json
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

class Authentication():
    def __init__(self, key: str) -> None:
        # AES key needs to be 16, 24, or 32 bytes long
        self.key = key.ljust(32)[:32]  # Ensure key length is valid

    def base64_encode(self, data):
        json_str = json.dumps(data)
        json_bytes = json_str.encode('utf-8')
        base64_encoded = base64.b64encode(json_bytes)
        return base64_encoded

    def base64_decode(self, encoded_str):
        decoded_bytes = base64.b64decode(encoded_str)
        decoded_str = decoded_bytes.decode('utf-8')
        decoded_data = json.loads(decoded_str)
        return decoded_data

    def generate_key(self, data):
        # Base64 encode the dictionary data
        base64_encoded = self.base64_encode(data)
        
        # Create AES cipher in ECB mode
        cipher = AES.new(self.key.encode('utf-8'), AES.MODE_ECB)
        
        # Encrypt the base64 encoded data
        encrypted = cipher.encrypt(pad(base64_encoded, AES.block_size))
        
        # Return the Base64 encoded encrypted data
        return base64.b64encode(encrypted).decode('utf-8')

    def decode_key(self, encoded_key):
        # Decode the base64 encoded encrypted data
        encrypted_data = base64.b64decode(encoded_key)
        
        # Create AES cipher in ECB mode
        cipher = AES.new(self.key.encode('utf-8'), AES.MODE_ECB)
        
        # Decrypt the data and unpad it
        decrypted = unpad(cipher.decrypt(encrypted_data), AES.block_size)
        
        # Base64 decode to get the original data
        original_data = base64.b64decode(decrypted).decode('utf-8')
        
        # Convert JSON string back to dictionary
        return json.loads(original_data)

if __name__ == "__main__":
    auth = Authentication("wei.wang")

    data = {
        "user": "605686962Qqq.com",
        "password": "12345",
        "duration": 120,
        "init_date":"12324232"
    }

    # Generate the encrypted key
    encrypted_key = auth.generate_key(data)
    print(f"Encrypted key: {encrypted_key}")
    
    # Decode the encrypted key to retrieve the original data
    decoded_data = auth.decode_key(encrypted_key)
    print(f"Decoded data: {decoded_data}")
