import cv2  
import numpy as np  
import time

# File paths
input_video_path = '1.mp4'
output_video_path = 'final.mp4'

# Video capture setup
video = cv2.VideoCapture(input_video_path)
if not video.isOpened():
    print(f"Error: Could not open video file {input_video_path}")
    exit()

# Get video properties
width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = video.get(cv2.CAP_PROP_FPS)
total_frames_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
threshold = 20.0
summarized_duration = 15  # Desired duration in seconds

# Calculate the target number of frames for the summarized video
target_frame_count = int(summarized_duration * fps)
frame_interval = total_frames_count // target_frame_count

# Video writer setup
fourcc = cv2.VideoWriter_fourcc(*'DIVX')
writer = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

# Read the first frame
ret, prev_frame = video.read()
if not ret:
    print("Error: Could not read the first frame.")
    video.release()
    exit()

# Initialize frame counters
total_frames = 0
unique_frames = 0
common_frames = 0

# Start processing time
start_time = time.time()

# Process video frames
while video.isOpened():
    ret, frame = video.read()
    if not ret:
        break

    if total_frames % frame_interval == 0:
        # Calculate frame difference
        frame_diff = np.sum(np.absolute(frame - prev_frame)) / np.size(frame)
        if frame_diff > threshold:
            writer.write(frame)
            prev_frame = frame
            unique_frames += 1
        else:
            common_frames += 1

    cv2.imshow('Frame', frame)
    total_frames += 1

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# End processing time
end_time = time.time()
processing_time = end_time - start_time

# Print summary
print("Video Summary")
print(f"Total frames: {total_frames}")
print(f"Unique frames: {unique_frames}")
print(f"Common frames: {common_frames}")
print(f"Processing time (seconds): {processing_time:.2f}")
print(f"Frames per second (FPS): {total_frames / processing_time:.2f}")
print(f"Original video duration (seconds): {total_frames_count / fps:.2f}")
print(f"Summarized video duration (seconds): {unique_frames / fps:.2f}")

# Release resources
video.release()
writer.release()
cv2.destroyAllWindows()
