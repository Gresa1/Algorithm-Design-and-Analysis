# test_cipher.py
import unittest         # Import the unittest framework from the Python standard library
from CeaserCipherAlgorithm import caesar_cipher, encrypt_file, decrypt_file 
import os               

class TestCaesarCipher(unittest.TestCase):

    # Test that encrypting and then decrypting a string returns the original string
    def test_caesar_round_trip(self):
        original = "Hello, World! 123"  # Original text sample
        shift = 4                       # Shift value for the cipher
        # Encrypt the original text
        encrypted = caesar_cipher(original, shift, mode='encrypt')
        # Decrypt the encrypted text
        decrypted = caesar_cipher(encrypted, shift, mode='decrypt')
        # Assert that the decrypted text matches the original text
        self.assertEqual(original, decrypted, "Round-trip encryption/decryption failed.")

    # Test the full file encryption and decryption process (round-trip file test)
    def test_file_round_trip(self):
        shift = 3  # Shift value for file encryption/decryption
        # Define file names for the test:
        input_file = "test_input.txt"
        encrypted_file = "temp_encrypted.txt"
        decrypted_file = "temp_decrypted.txt"
        
        # Define content for the test input file
        test_content = "This is a test file for accuracy checking."
        # Write the test content into the input file
        with open(input_file, "w", encoding="utf-8") as f:
            f.write(test_content)

        # Encrypt the input file into the encrypted file
        encrypt_file(input_file, encrypted_file, shift)
        # Decrypt the encrypted file into the decrypted file
        decrypt_file(encrypted_file, decrypted_file, shift)
        
        # Read the content from the decrypted file
        with open(decrypted_file, "r", encoding="utf-8") as f:
            decrypted_content = f.read()
        
        # Cleanup: Remove the temporary files created during testing
        # os.remove(input_file)
        # os.remove(encrypted_file)
        # os.remove(decrypted_file)
        
        # Assert that the content of the decrypted file matches the original test content
        self.assertEqual(test_content, decrypted_content, "File round-trip test failed.")

# The following code ensures that the tests are executed when the script is run directly.
if __name__ == '__main__':
    unittest.main()
