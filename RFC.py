import os
import random
import cv2
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

def select_random_frame(video_path, output_folder, base_frame_name, frame_index):
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    random_frame_number = random.randint(0, total_frames - 1)
    cap.set(cv2.CAP_PROP_POS_FRAMES, random_frame_number)
    ret, frame = cap.read()

    if ret:
        frame_name = os.path.join(output_folder, f"{base_frame_name}_{frame_index}.jpg")
        cv2.imwrite(frame_name, frame)
    else:
        print(f"Failed to read the frame from {video_path}")

    cap.release()

def process_videos(video_files, output_folder, num_frames, base_frame_name):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for idx, video_file in enumerate(video_files):
        for frame_idx in range(num_frames):
            select_random_frame(video_file, output_folder, base_frame_name, idx * num_frames + frame_idx)

def select_files():
    file_paths = filedialog.askopenfilenames(title="Select video files", filetypes=[("Video files", "*.mp4 *.avi *.mov")])

    if file_paths:
        num_frames = simpledialog.askinteger("Number of Frames", "Enter the number of frames to extract from each video:", minvalue=1, initialvalue=1)
        base_frame_name = simpledialog.askstring("Frame Name", "Enter the base name for the frames:", initialvalue="frame")

        if num_frames and base_frame_name:
            default_output_folder = os.path.join(os.path.expanduser("frames"))
            process_videos(file_paths, default_output_folder, num_frames, base_frame_name)
            messagebox.showinfo("Success", f"Frames have been saved successfully to {default_output_folder}!")
        else:
            messagebox.showwarning("Warning", "Invalid number of frames or frame name.")
    else:
        messagebox.showwarning("Warning", "No video files were selected.")

root = tk.Tk()
root.title("Random Frame Selector")

label = tk.Label(root, text="Select video files to extract random frames:")
label.pack(pady=10)

button = tk.Button(root, text="Select Video Files", command=select_files)
button.pack(pady=10)

root.mainloop()
