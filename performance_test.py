# performance_tests.py
import time                   # Import time module for measuring runtime
import psutil                 # Import psutil for measuring memory usage
import os                     # Import os for file handling (if needed)
from CeaserCipherAlgorithm import encrypt_file, decrypt_file  # Import the file I/O functions

# Returns the current memory usage of the process in MB.

def get_memory_usage():
    process = psutil.Process(os.getpid())  # Get the current process object
    return process.memory_info().rss / 1024 ** 2  # Convert RSS (in bytes) to MB

# Measures and prints the average runtime for encryption or decryption.
# Parameters:
#   - input_path:  Path to the input file.
#   - output_path: Path to the output file (encrypted/decrypted).
#   - shift:       The shift value for the cipher.
#   - mode:        Either 'encrypt' or 'decrypt'.
#   - iterations:  Number of times to run the test to average the results.
# Returns:       The average time taken in seconds.

def test_runtime(input_path, output_path, shift, mode='encrypt', iterations=5):
    times = []  # List to store runtime for each iteration
    for _ in range(iterations):
        start_time = time.time()  # Record the start time
        if mode == 'encrypt':
            encrypt_file(input_path, output_path, shift)  # Call encryption function
        elif mode == 'decrypt':
            decrypt_file(input_path, output_path, shift)  # Call decryption function
        else:
            raise ValueError("Mode must be either 'encrypt' or 'decrypt'")
        # Calculate the elapsed time for the operation
        elapsed_time = time.time() - start_time
        times.append(elapsed_time)  # Append the elapsed time to our list
    # Calculate the average runtime from all iterations
    avg_time = sum(times) / len(times)
    print(f"Average {mode} time for {input_path}: {avg_time:.4f} seconds")
    return avg_time

# Measures and prints the memory usage difference before and after running encryption or decryption.
# Parameters are the same as in test_runtime.
# Returns: The difference in memory usage in MB.

def test_memory(input_path, output_path, shift, mode='encrypt'):
    mem_before = get_memory_usage()  # Get memory usage before running the function
    if mode == 'encrypt':
        encrypt_file(input_path, output_path, shift)  # Encrypt the file
    elif mode == 'decrypt':
        decrypt_file(input_path, output_path, shift)  # Decrypt the file
    else:
        raise ValueError("Mode must be either 'encrypt' or 'decrypt'")
    mem_after = get_memory_usage()   # Get memory usage after the operation
    mem_diff = mem_after - mem_before  # Calculate the difference
    print(f"Memory usage increased by {mem_diff:.4f} MB during {mode} of {input_path}")
    return mem_diff

# Runs runtime and memory tests on a set of test files.
# Iterates over a predefined list of files and prints a summary for each.
# Parameters:
#   - shift_value: The shift value to be used for all tests.

def run_performance_tests(shift_value):
    # List of test files: each tuple consists of (input file, encrypted file, decrypted file)
    test_files = [
        ("text_10KB.txt", "encrypted_10KB.txt", "decrypted_10KB.txt"),
        ("text_100KB.txt", "encrypted_100KB.txt", "decrypted_100KB.txt"),
        ("text_1MB.txt", "encrypted_1MB.txt", "decrypted_1MB.txt")
    ]
    iterations = 3  # Number of iterations for runtime averaging

    # Iterate over each test file tuple in our list
    for input_file, encrypted_file, decrypted_file in test_files:
        print("\n===============================================")
        print(f"Testing file: {input_file}")

        # -------------------------------
        # Run Encryption Tests
        # -------------------------------
        print("\n--- Encryption ---")
        # Measure average runtime for encryption and capture the result
        avg_enc_time = test_runtime(input_file, encrypted_file, shift_value, mode='encrypt', iterations=iterations)
        # Measure memory usage change during encryption
        mem_enc_usage = test_memory(input_file, encrypted_file, shift_value, mode='encrypt')

        # -------------------------------
        # Run Decryption Tests
        # -------------------------------
        print("\n--- Decryption ---")
        # Measure average runtime for decryption (using the encrypted file)
        avg_dec_time = test_runtime(encrypted_file, decrypted_file, shift_value, mode='decrypt', iterations=iterations)
        # Measure memory usage change during decryption
        mem_dec_usage = test_memory(encrypted_file, decrypted_file, shift_value, mode='decrypt')

        # -------------------------------
        # Print Summary for the current test file
        # -------------------------------
        print("\n------ Summary for", input_file, "------")
        print(f"Encryption: Average runtime = {avg_enc_time:.4f} s, Memory increase = {mem_enc_usage:.4f} MB")
        print(f"Decryption: Average runtime = {avg_dec_time:.4f} s, Memory increase = {mem_dec_usage:.4f} MB")
        print("===============================================\n")


# Execution starts here when the script is run directly.
# It prompts the user for a shift value and then runs the performance tests.
if __name__ == '__main__':
    # Prompt the user for the shift value
    shift_value = int(input("Enter the shift value (integer): "))
    # Run the performance tests with the provided shift value
    run_performance_tests(shift_value)
