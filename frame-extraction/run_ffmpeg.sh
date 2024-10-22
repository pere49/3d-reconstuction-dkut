# -----------------------------------------------------------------------------
# Copyright (c) 2023, NVIDIA CORPORATION. All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto. Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.
# -----------------------------------------------------------------------------

# usage: run_ffmpeg.sh <sequence_name> <full_video_path> <downsample_rate>

data_path=/path/to/working/directory
output_path=${data_path}/images_raw
video_path=/path/to/video
frame_rate= 2
mkdir -p ${image_path}
ffmpeg -i ${video_path} -vf "select=not(mod(n\, ${frame_rate} ))" -vsync vfr -q:v 2 ${output_path}/%06d.jpg
