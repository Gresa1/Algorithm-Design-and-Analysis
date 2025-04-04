# Function to perform Caesar Cipher (both encryption and decryption)
def caesar_cipher(text, shift, mode='encrypt'):
    result = ''  # Final result string (encrypted or decrypted)
    for char in text:
        if char.isalpha():  # Only modify alphabetic characters
            # Use ASCII values: 'A' for uppercase, 'a' for lowercase
            shift_base = ord('A') if char.isupper() else ord('a')

            if mode == 'encrypt':
                # Shift character forward in the alphabet
                result += chr((ord(char) - shift_base + shift) % 26 + shift_base)
            elif mode == 'decrypt':
                # Shift character backward in the alphabet
                result += chr((ord(char) - shift_base - shift) % 26 + shift_base)
        else:
            # Leave spaces, punctuation, and numbers unchanged
            result += char
    return result

# Function to encrypt text from a file and write to a new file
def encrypt_file(input_path, output_path, shift):
    with open(input_path, 'r') as f:
        plaintext = f.read()  # Read original text

    encrypted_text = caesar_cipher(plaintext, shift, mode='encrypt')  # Encrypt the text

    with open(output_path, 'w') as f:
        f.write(encrypted_text)  # Write encrypted text to new file

    print("Encryption complete. Encrypted file saved to:", output_path)

# Function to decrypt text from a file and write to a new file
def decrypt_file(input_path, output_path, shift):
    with open(input_path, 'r') as f:
        encrypted_text = f.read()  # Read encrypted text

    decrypted_text = caesar_cipher(encrypted_text, shift, mode='decrypt')  # Decrypt the text

    with open(output_path, 'w') as f:
        f.write(decrypted_text)  # Write decrypted text to new file

    print("Decryption complete. Decrypted file saved to:", output_path)

# Main program starts here
if __name__ == "__main__":
    try:
        # Ask user to enter the shift value (must be an integer)
        shift_value = int(input("Enter the shift value (integer): "))

        # Menu to let user choose between encryption and decryption
        print("\nChoose an option:")
        print("1. Encrypt a file")
        print("2. Decrypt a file")
        choice = input("Enter your choice (1 or 2): ")

        # Run the appropriate function based on user's choice
        if choice == '1':
            # Print the original text from the input file
            with open('input.txt', 'r') as f:
                original_text = f.read()
                print("\nOriginal file contents:")
                print(original_text)
                
            encrypt_file('input.txt', 'encrypted.txt', shift_value)
            # Open and print the encrypted file contents
            with open('encrypted.txt', 'r') as f:
                print("\nEncrypted file contents:")
                print(f.read())
        elif choice == '2':
            decrypt_file('encrypted.txt', 'decrypted.txt', shift_value)
            # Open and print the decrypted file contents
            with open('decrypted.txt', 'r') as f:
                print("\nDecrypted file contents:")
                print(f.read())
        else:
            print("Invalid choice. Please enter 1 or 2.")

    except ValueError:
        # Handle case where user doesn't enter a valid number
        print("Invalid input. Please enter a valid integer for the shift.")
