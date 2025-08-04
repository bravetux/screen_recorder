# Import necessary libraries
import os  # For file and directory operations
import cv2  # OpenCV for video writing
import numpy as np  # For array manipulation
import pyautogui  # For screen capture and screenshots
import sounddevice as sd  # For audio recording
from scipy.io.wavfile import write  # To save audio as WAV
import threading  # For running tasks concurrently
import time  # For timing operations
import tkinter as tk  # GUI toolkit
from tkinter import messagebox  # For popup messages
import subprocess  # To run external commands (FFmpeg)
from datetime import datetime  # For timestamping screenshots
import keyboard  # For global hotkey detection

# Recording settings
fps = 10  # Frames per second for screen recording
screen_size = pyautogui.size()  # Get screen resolution
recording_event = threading.Event()  # Event to control recording state

# Define paths for saving files
save_dir = r"C:\Temp\screen_rec"
video_path = os.path.join(save_dir, "screen_record.avi")
audio_path = os.path.join(save_dir, "audio_record.wav")
final_path = os.path.join(save_dir, "final_output.mp4")

# Create save directory if it doesn't exist
os.makedirs(save_dir, exist_ok=True)

# Function to record audio
def record_audio(duration, audio_path):
    try:
        fs = 44100  # Sampling rate
        audio = sd.rec(int(duration * fs), samplerate=fs, channels=2)  # Record audio
        sd.wait()  # Wait until recording is finished
        write(audio_path, fs, audio)  # Save audio to file
    except Exception as e:
        print(f"Audio recording error: {e}")

# Function to record screen
def record_screen(duration, video_path):
    try:
        fourcc = cv2.VideoWriter_fourcc(*"XVID")  # Video codec
        out = cv2.VideoWriter(video_path, fourcc, fps, screen_size)  # Video writer object
        start_time = time.time()
        while recording_event.is_set() and (time.time() - start_time < duration):
            img = pyautogui.screenshot()  # Capture screen
            frame = np.array(img)  # Convert to numpy array
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert color format
            out.write(frame)  # Write frame to video
        out.release()  # Release video writer
    except Exception as e:
        print(f"Screen recording error: {e}")

# Function to combine audio and video using FFmpeg
def combine_audio_video(video_path, audio_path, output_path):
    try:
        command = [
            "ffmpeg",
            "-y",  # Overwrite output file if exists
            "-i", video_path,
            "-i", audio_path,
            "-c:v", "copy",  # Copy video codec
            "-c:a", "aac",  # Convert audio to AAC
            "-strict", "experimental",
            output_path
        ]
        subprocess.run(command, check=True)  # Run FFmpeg command
        messagebox.showinfo("Success", f"Combined video saved:\n{output_path}")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("FFmpeg Error", f"Failed to combine audio and video.\n{e}")

# Function to start recording
def start_recording():
    if recording_event.is_set():
        return  # Already recording

    duration = 3600  # Max duration: 1 hour

    recording_event.set()  # Set recording flag
    # Start audio and screen recording in separate threads
    audio_thread = threading.Thread(target=record_audio, args=(duration, audio_path), daemon=True)
    screen_thread = threading.Thread(target=record_screen, args=(duration, video_path), daemon=True)

    audio_thread.start()
    screen_thread.start()

    print("Recording started...")

# Function to stop recording
def stop_recording():
    if not recording_event.is_set():
        return  # Not recording
    recording_event.clear()  # Clear recording flag
    print("Stopping recording...")

    time.sleep(2)  # Wait for threads to finish
    combine_audio_video(video_path, audio_path, final_path)  # Merge audio and video

# Function to take a screenshot
def take_screenshot():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # Generate timestamp
    screenshot_path = os.path.join(save_dir, f"screenshot_{timestamp}.png")
    screenshot = pyautogui.screenshot()
    screenshot.save(screenshot_path)
    print(f"Screenshot saved to: {screenshot_path}")

# Function to set up global hotkeys
def setup_hotkeys():
    keyboard.add_hotkey('windows+shift+r', start_recording)
    keyboard.add_hotkey('windows+shift+s', stop_recording)
    keyboard.add_hotkey('print screen', take_screenshot)

# GUI setup
root = tk.Tk()
root.title("Screen Recorder")
root.geometry("320x200")
root.resizable(False, False)

# GUI labels and buttons
tk.Label(root, text="🎬 Use Hotkeys to Control Recording").pack(pady=10)
tk.Label(root, text="▶ Win + Shift + R: Start Recording").pack()
tk.Label(root, text="⏹ Win + Shift + S: Stop Recording").pack()
tk.Label(root, text="📸 Print Screen: Take Screenshot").pack(pady=10)
tk.Button(root, text="Quit", command=root.quit).pack(pady=5)

# Minimize window on start
root.update_idletasks()
root.iconify()

# Register hotkeys
setup_hotkeys()

# Start GUI event loop
root.mainloop()
