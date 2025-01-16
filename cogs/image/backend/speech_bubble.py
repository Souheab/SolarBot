from PIL import Image, ImageOps
import sys

SPEECH_BUBBLE_IMAGE_PATH = "./assets/speechbubble_template.png"

def create_speech_bubble(input_image):
    if input_image.mode != "RGBA":
        input_image = input_image.convert("RGBA")

    speech_bubble = Image.open(SPEECH_BUBBLE_IMAGE_PATH).convert("L")
    speech_bubble_resized = speech_bubble.resize(input_image.size, Image.Resampling.LANCZOS)
    inverted_mask = ImageOps.invert(speech_bubble_resized)
    input_image_speech_bubble = Image.composite(Image.new("RGBA", input_image.size, (255, 255, 255, 0)), 
                                              input_image, 
                                              inverted_mask)
    return input_image_speech_bubble

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_image_path> <output_image_path>")
        sys.exit(1)
    
    input_image_path = sys.argv[1]
    output_image_path = sys.argv[2]

    input_image = Image.open(input_image_path).convert("RGBA")
    output_image = create_speech_bubble(input_image)
    output_image.save(output_image_path, "PNG")
    print(f"Output saved to {output_image_path}")
