from PIL import Image

# Your PNG file
png_file = "logo.png"  # Replace with your image name

# Automatically create ICO file name based on PNG name
ico_file = png_file.rsplit(".", 1)[0] + ".ico"

# Open and convert
img = Image.open(png_file)
img.save(ico_file, format='ICO')

print(f"Icon created successfully: {ico_file}")