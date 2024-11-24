from PIL import Image, ImageDraw

# Create a new image with a white background
size = (256, 256)
icon = Image.new('RGBA', size, (255, 255, 255, 0))

# Create a drawing object
draw = ImageDraw.Draw(icon)

# Draw a simple converter icon
# Main rectangle
draw.rectangle([(50, 50), (206, 206)], fill=(65, 105, 225), outline=(0, 0, 139), width=3)
# Arrow
draw.polygon([(90, 128), (166, 80), (166, 176)], fill=(255, 255, 255))

# Save the icon
icon.save('app_icon.ico', format='ICO')
