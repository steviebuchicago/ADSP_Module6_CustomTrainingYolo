import csv
import os
from PIL import Image

def custom_eval(s):
    try:
        return eval(s)
    except:
        return None

# Set your paths
input_csv_path = 'FindSteve_csv.csv'
image_directory = 'steve/'
output_directory = 'steveannotations/'

# Create the output directory if it doesn't exist
try:
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
except Exception as e:
    print(f"Error creating output directory: {e}")
    exit(1)  # Exit the script if the directory cannot be created

# Define a dictionary for classes
class_dict = {"name": 0}  # Adjusted to match the CSV data

processed_files = 0  # To count how many files have been processed

with open(input_csv_path, 'r') as csv_file:
    reader = csv.reader(csv_file)
    next(reader)  # Skip the header
    
    for row in reader:
        filename = row[0]
        region_shape_attributes = custom_eval(row[5])
        region_attributes = custom_eval(row[6])

        # Skip rows without the necessary attributes
        if not region_shape_attributes or not region_attributes:
            continue
        
        # Check for specific name and process if exists
        if 'name' in region_attributes and region_attributes['name'] == "Steve":
            processed_files += 1
            # Calculate bounding box for YOLO
            x = int(region_shape_attributes['x'])
            y = int(region_shape_attributes['y'])
            width = int(region_shape_attributes['width'])
            height = int(region_shape_attributes['height'])
            img_path = os.path.join(image_directory, filename)
            
            try:
                with Image.open(img_path) as img:
                    img_width, img_height = img.size
                    x_center = (x + width / 2) / img_width
                    y_center = (y + height / 2) / img_height
                    width_norm = width / img_width
                    height_norm = height / img_height

                    # Write annotations to txt file
                    output_file_path = os.path.join(output_directory, f"{os.path.splitext(filename)[0]}.txt")
                    with open(output_file_path, 'w') as file:
                        file.write(f"{class_dict['name']} {x_center} {y_center} {width_norm} {height_norm}\n")
            except IOError:
                print(f"Cannot open image file: {img_path}")

# Check if any files were processed
if processed_files == 0:
    print("No valid data found to process. Check CSV format and content.")
