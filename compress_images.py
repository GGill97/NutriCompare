import os
from dotenv import load_dotenv
import tinify
from tinify.errors import ClientError
from PIL import Image
import io

# Load environment variables
load_dotenv()

# Set your API key
tinify.key = os.getenv('TINIFY_API_KEY')

def compress_images(directory):
    compressed_sizes = {}
    original_sizes = {}
    skipped_files = []
    
    for filename in os.listdir(directory):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            filepath = os.path.join(directory, filename)
            
            # Get original file size
            original_size = os.path.getsize(filepath)
            original_sizes[filename] = original_size

            try:
                # Open and re-save the image using Pillow
                with Image.open(filepath) as img:
                    buffer = io.BytesIO()
                    img.save(buffer, format=img.format)
                    buffer.seek(0)

                # Compress the image
                source = tinify.from_buffer(buffer.getvalue())
                source.to_file(filepath)

                # Get compressed file size
                compressed_size = os.path.getsize(filepath)
                compressed_sizes[filename] = compressed_size
            except Exception as e:
                print(f"Skipping {filename}: {str(e)}")
                skipped_files.append(filename)

    return original_sizes, compressed_sizes, skipped_files

# Compress images
original, compressed, skipped = compress_images('app/static/images')

# Print results
print("Compression results:")
for filename in original:
    if filename in compressed:
        original_size = original[filename]
        compressed_size = compressed[filename]
        saving = original_size - compressed_size
        saving_percent = (saving / original_size) * 100
        
        print(f"{filename}:")
        print(f"  Original size: {original_size/1024:.2f} KB")
        print(f"  Compressed size: {compressed_size/1024:.2f} KB")
        print(f"  Saved: {saving/1024:.2f} KB ({saving_percent:.2f}%)")
        print()

total_original = sum(original.values())
total_compressed = sum(compressed.values())
total_saving = total_original - total_compressed
total_saving_percent = (total_saving / total_original) * 100

print("Total savings:")
print(f"  Original total: {total_original/1024:.2f} KB")
print(f"  Compressed total: {total_compressed/1024:.2f} KB")
print(f"  Total saved: {total_saving/1024:.2f} KB ({total_saving_percent:.2f}%)")

if skipped:
    print("\nSkipped files:")
    for file in skipped:
        print(f"  {file}")