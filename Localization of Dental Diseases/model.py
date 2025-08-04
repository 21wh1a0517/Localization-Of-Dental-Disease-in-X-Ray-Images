# from ultralytics import YOLO
# from PIL import Image, ImageDraw, ImageFont
# import io
# import base64

# # Load the YOLO model
# model = YOLO("dental_model.pt")

# def predict_image(image_file):
#     image = Image.open(image_file).convert("RGB")
#     results = model.predict(image)
#     result = results[0]

#     draw = ImageDraw.Draw(image)

#     try:
#         font_path = "static/arial.ttf"
#         font_size = 20
#         font = ImageFont.truetype(font_path, font_size)
#     except IOError:
#         font = ImageFont.load_default()

#     output = []
#     for idx, box in enumerate(result.boxes, start=1):
#         x1, y1, x2, y2 = [round(x) for x in box.xyxy[0].tolist()]
#         class_id = int(box.cls[0].item())
#         prob = round(box.conf[0].item(), 2)
#         prob_percentage = f"{prob * 100:.2f}%"

#         # Draw only the serial number on the image
#         draw.rectangle([(x1, y1), (x2, y2)], outline="green", width=4)
#         draw.text((x1 + 2, y1 - 20), str(idx), fill="white", font=font)

#         # Collect detailed info for UI
#         output.append({
#             # "serial": idx,
#             "class": result.names[class_id],
#             "confidence": prob_percentage
#         })

#     img_byte_arr = io.BytesIO()
#     image.save(img_byte_arr, format='PNG')
#     img_byte_arr.seek(0)
#     image_data = base64.b64encode(img_byte_arr.read()).decode('utf-8')

#     return image_data, output

from ultralytics import YOLO
from PIL import Image, ImageDraw, ImageFont
import io
import base64
import random

# Load the YOLO model
model = YOLO("dental_model.pt")

# Generate a consistent color for each class
def get_color_map(class_names):
    random.seed(42)  # For consistent colors
    color_map = {}
    for cls in class_names:
        color_map[cls] = tuple(random.choices(range(50, 256), k=3))
    return color_map

def predict_image(image_file):
    image = Image.open(image_file).convert("RGB")
    results = model.predict(image)
    result = results[0]
    class_names = result.names

    color_map = get_color_map(class_names.values())
    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype("static/arial.ttf", 20)
    except IOError:
        font = ImageFont.load_default()

    detections = []
    for idx, box in enumerate(result.boxes, start=1):
        x1, y1, x2, y2 = [round(x) for x in box.xyxy[0].tolist()]
        class_id = int(box.cls[0].item())
        class_name = class_names[class_id]
        prob = round(box.conf[0].item(), 2)
        prob_percentage = f"{prob * 100:.2f}%"

        color = color_map[class_name]

        # Draw bounding box and only the serial number
        draw.rectangle([(x1, y1), (x2, y2)], outline=color, width=4)
        draw.text((x1 + 2, y1 - 20), str(idx), fill="white", font=font)

        detections.append({
            # "serial": idx,
            "class": class_name,
            "confidence": prob_percentage
        })

    # Encode final image to base64
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    encoded_img = base64.b64encode(img_byte_arr.read()).decode('utf-8')

    return encoded_img, detections
