import time
import psutil
import os
# from memory_profiler import profile


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

# ----------------------------------------------------------
# Runtime Measurement Functions
# ----------------------------------------------------------

def test_runtime(input_path, output_path, shift, mode='encrypt', iterations=5):
    times = []
    for _ in range(iterations):
        start_time = time.time()
        if mode == 'encrypt':
            encrypt_file(input_path, output_path, shift)
        elif mode == 'decrypt':
            decrypt_file(input_path, output_path, shift)
        else:
            raise ValueError("Mode must be either 'encrypt' or 'decrypt'")
        end_time = time.time()
        times.append(end_time - start_time)
    average_time = sum(times) / len(times)
    print(f"Average {mode} time for {input_path}: {average_time:.4f} seconds")
    return average_time

# ----------------------------------------------------------
# Memory Measurement Functions (Using psutil)
# ----------------------------------------------------------

def get_memory_usage():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 ** 2  # Return memory usage in MB

def test_memory_psutil(input_path, output_path, shift, mode='encrypt'):
    mem_before = get_memory_usage()
    if mode == 'encrypt':
        encrypt_file(input_path, output_path, shift)
    elif mode == 'decrypt':
        decrypt_file(input_path, output_path, shift)
    else:
        raise ValueError("Mode must be either 'encrypt' or 'decrypt'")
    mem_after = get_memory_usage()
    memory_increase = mem_after - mem_before
    print(f"Memory usage increased by {memory_increase:.4f} MB during {mode}")
    return memory_increase
# ----------------------------------------------------------
# Experiment Function to Run Tests on Multiple Files
# ----------------------------------------------------------
def run_experiments(shift_value):
    # Define a list with tuples: (input file, encrypted file, decrypted file)
    test_files = [
        ("text_10KB.txt", "encrypted_10KB.txt", "decrypted_10KB.txt"),
        ("text_100KB.txt", "encrypted_100KB.txt", "decrypted_100KB.txt"),
        ("text_1MB.txt", "encrypted_1MB.txt", "decrypted_1MB.txt")
    ]
    
    iterations = 3  # Number of runs to average runtime measurements

    for input_file, encrypted_file, decrypted_file in test_files:
        print("\n===============================================")
        print(f"Testing file: {input_file}")
        
        # Test Encryption
        print("\n--- Encryption ---")
        avg_enc_time = test_runtime(input_file, encrypted_file, shift_value, mode='encrypt', iterations=iterations)
        mem_enc_usage = test_memory_psutil(input_file, encrypted_file, shift_value, mode='encrypt')

        # Test Decryption (using the already encrypted file)
        print("\n--- Decryption ---")
        avg_dec_time = test_runtime(encrypted_file, decrypted_file, shift_value, mode='decrypt', iterations=iterations)
        mem_dec_usage = test_memory_psutil(encrypted_file, decrypted_file, shift_value, mode='decrypt')
        
        # Print a summary of the results for the current file
        print("\n------ Summary for", input_file, "------")
        print(f"Encryption: Average runtime = {avg_enc_time:.4f} s, Memory increase = {mem_enc_usage:.4f} MB")
        print(f"Decryption: Average runtime = {avg_dec_time:.4f} s, Memory increase = {mem_dec_usage:.4f} MB")
        print("===============================================\n")

# Main program starts here
if __name__ == "__main__":
    try:
        # Ask user to enter the shift value (must be an integer)
        shift_value = int(input("Enter the shift value (integer): "))

        # Menu to let user choose between encryption and decryption
        print("\nChoose an option:")
        print("1. Encrypt a file")
        print("2. Decrypt a file")
        print("3. Run experiments on multiple test files")
        choice = input("Enter your choice (1, 2, or 3): ")

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
        elif choice == '3':
            run_experiments(shift_value)
            
        else:
            print("Invalid choice. Please enter 1 or 2.")

    except ValueError:
        # Handle case where user doesn't enter a valid number
        print("Invalid input. Please enter a valid integer for the shift.")
