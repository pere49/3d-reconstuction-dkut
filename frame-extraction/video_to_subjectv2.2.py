import os
import glob
import numpy as np
import cv2
from rembg import remove

#make the necessary directories
os.makedirs("clean_images", exist_ok=True)
print("created clean_images folder")
os.makedirs("subject_images",exist_ok=True)
print("created subject_images folder")

#function to remove unnecessary parts of the image
def add_proximity_ring(input_image_path, output_image_path, ring_width=10):
    # Step 1: Remove the background using rembg
    with open(input_image_path, 'rb') as img_file:
        input_img = img_file.read()
    removed_background = remove(input_img)
    
    # Step 2: Read the output from rembg using OpenCV
    nparr = np.frombuffer(removed_background, np.uint8)
    img_no_bg = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)  # Load image with transparency
    
    # Step 3: Extract the alpha channel (the transparency mask)
    if img_no_bg.shape[2] == 4:
        alpha_channel = img_no_bg[:, :, 3]  # Extract the alpha channel (4th channel)
    else:
        print("Image does not have an alpha channel.")
        return
    
    # Step 4: Threshold the alpha channel to create a binary mask
    _, binary_mask = cv2.threshold(alpha_channel, 1, 255, cv2.THRESH_BINARY)

    # Step 5: Dilate the mask to create the "ring" around the subject
    kernel = np.ones((ring_width, ring_width), np.uint8)
    dilated_mask = cv2.dilate(binary_mask, kernel, iterations=1)

    # Step 6: Create a 3-channel version of the dilated mask
    dilated_mask_3_channel = cv2.merge([dilated_mask, dilated_mask, dilated_mask])

    # Step 7: Read the original image to blend the ring back onto it
    original_image = cv2.imread(input_image_path)

    # Step 8: Blend the dilated mask onto the original image
    subject_with_ring = np.where(dilated_mask_3_channel == 255, original_image, img_no_bg[:, :, :3])

    # Step 9: Save the output image
    cv2.imwrite(output_image_path, subject_with_ring)

    #step 10: log the cleaned image
    print(f"Just cleaned {output_image_path}")

# Function to remove surplus images in an even manner
def remove_surplus_images(folder_path, max_images=300):
    # List all the image files in the folder (assuming images are .jpg)
    images = [f for f in os.listdir(folder_path) if f.endswith('.jpg')]
    
    # Sort the images by their numeric value
    images.sort(key=lambda x: int(x.split('.')[0]))  # Assuming filenames like '0.jpg', '1.jpg'

    # Check how many images are in the folder
    total_images = len(images)

    # If the number of images is greater than max_images, remove the surplus
    if total_images > max_images:
        surplus = total_images - max_images
        print(f"Found {total_images} images, removing {surplus} images.")

        # Calculate which images to remove
        indices_to_remove = []
        step = total_images / surplus  # Calculate the interval for even removal

        # Select evenly spaced indices for removal
        for i in range(surplus):
            index = int(i * step)  # Evenly distributed index
            if index < total_images:
                indices_to_remove.append(images[index])

        # Remove the images based on calculated indices
        for image_to_remove in indices_to_remove:
            image_path = os.path.join(folder_path, image_to_remove)
            try:
                os.remove(image_path)
                print(f"Removed {image_to_remove}")
            except OSError as error:
                print(f"Error: {error}")

        print(f"Successfully removed {surplus} images. Total images now: {max_images}")
    else:
        print(f"No surplus images found. Total images: {total_images}")

#capture the clear frames from the video
cap = cv2.VideoCapture("videos/grey_stump.mp4")# change the video file name
frame_no = 0
while cap.isOpened():
    ret,frame = cap.read()
    if not ret:
        print("reached the end of the video")
        break
    #if the frame we get is a clean frame we will store it in the clean_images folder
    gray_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)#get the frame in gray scale
    laplacian_var = cv2.Laplacian(gray_frame,cv2.CV_64F).var()#get the laplacian value of the frame
    if laplacian_var > 30:
         target = f"clean_images/{frame_no}.jpg"
         cv2.imwrite(target,frame)
         print(f"created {frame_no}.jpg")
         frame_no +=1

    if cv2.waitKey(1) == ord('q'):
        print("Video stopped by user.")
        break
    
cap.release()
cv2.destroyAllWindows()

#reduce the number of image files to 300
folder = "clean_images"
remove_surplus_images(folder)

clean_files = glob.glob("clean_images/*.jpg")
for clean_file in clean_files:
    clean_input_path = clean_file
    clean_output_path = clean_input_path.replace("clean_images","subject_images")
    add_proximity_ring(clean_input_path,clean_output_path,ring_width = 50)

print("done")