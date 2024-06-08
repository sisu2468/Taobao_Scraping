from PIL import Image

# Open the .ico file
ico = Image.open('./favicon_4.ico')

# Save as .png
ico.save('./file.png')