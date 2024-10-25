# Frame Extraction
This introduction will take you through how to use these frame extration scripts.

## Python version
Let's begin with the video_to_subjectv2.2.py. To be able to successfuly use and run this script you will need to have the libraries in the requirements.txt file. **This script has been tested with python versions 3.11.9 and 3.12.2 and .mp4 video files**.
### Functionality
The function of this script is to take a video input and from the video, extract at most 300 frames from the entire video and then from each image get the subject in that image. The program follows the following flow:
1. Create two folders, one called clean_images and another called subject_images.
2. We then extract all clean frames from the video and save them to the clean images folder, to know whether a frame is blurry or clear we use a Laplacian variable
3. We then delete all the surplus frames such that we remain with 300 (This will only happen if the extracted frames are more than 300). This is done in an even version such that we have an even distribution of frames throughout the video
4. From that we get every image from the clean_images folder and extract the subject from each image such that we get the image without most of the background.
### Proper Use
To ensure the script works as intended, you will need to create an empty folder and save the scripts in that folder, in the same folder you will need a folder named "videos" and in that folder you will have you video file (Prefarably less than 2 minutes runtime). In the script on line 93 rename the videos name with the video name you will find in the script or vice versa.

_this script was intended to take a video file and extract images to use as colmap(https://colmap.github.io/tutorial.html) inputs_

**Have fun with the script**