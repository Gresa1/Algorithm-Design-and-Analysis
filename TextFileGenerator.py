import os

def generate_text_file(filename, target_kb, paragraph):
    """
    Generate a text file with approximately target_kb kilobytes.
    
    :param filename: Name of the file to create.
    :param target_kb: Desired file size in kilobytes.
    :param paragraph: A string paragraph to be repeated in the file.
    """
    # Calculate the target size in bytes
    target_bytes = target_kb * 1024
    text = ""
    
    # Keep adding the paragraph (plus a newline) until we reach or exceed the target size
    while len(text.encode('utf-8')) < target_bytes:
        text += paragraph + "\n"
    
    # Write the generated text to the file
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)
    
    # Print file size info
    actual_size = os.path.getsize(filename) / 1024
    print(f"{filename} generated, size ~ {actual_size:.2f} KB")

# A sample understandable paragraph to be repeated.
sample_paragraph = (
    "The quick brown fox jumps over the lazy dog. "
    "This sentence is commonly used to test fonts and keyboards because it contains every letter of the alphabet. "
    "Reading through sentences like this can help improve typing speed and accuracy."
)

# Generate text files of different sizes
generate_text_file("text_10KB.txt", 10, sample_paragraph)
generate_text_file("text_100KB.txt", 100, sample_paragraph)
generate_text_file("text_1MB.txt", 1024, sample_paragraph)
