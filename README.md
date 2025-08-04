#🎥 Screen & Audio Recorder with Hotkeys and GUI
This Python application allows you to record your screen and audio simultaneously, take screenshots, and combine the recordings into a single video file using FFmpeg. It features a Tkinter-based GUI and global hotkeys for easy control.

#🚀 Features
📹 Screen recording at 10 FPS
🎙️ Audio recording using your system's microphone
🎞️ Merges audio and video using FFmpeg
🖼️ Screenshot capture with timestamped filenames
🧵 Multi-threaded recording for performance
🧩 Global hotkeys for:
Win + Shift + R → Start recording
Win + Shift + S → Stop recording
Print Screen → Take screenshot
🪟 Minimal GUI with instructions and quit button
🛠️ Requirements
Install the required Python libraries:


Also, ensure FFmpeg is installed and added to your system's PATH. You can download it from: https://ffmpeg.org/download.html

#📁 File Structure
C:\Temp\screen_rec\
├── screen_record.avi       # Raw screen recording
├── audio_record.wav        # Raw audio recording
├── final_output.mp4        # Final merged output
├── screenshot_*.png        # Timestamped screenshots
🧪 How It Works
Start Recording: Press Win + Shift + R
Stop Recording: Press Win + Shift + S
Screenshot: Press Print Screen
Quit App: Use the GUI "Quit" button
The app minimizes on launch and runs in the background, listening for hotkeys.

#⚠️ Notes
The default recording duration is set to 1 hour.
All files are saved in C:\Temp\screen_rec. You can change this path in the script.
Ensure you run the script with administrator privileges to allow global hotkey detection.

#📸 GUI Preview
The GUI is minimal and only displays hotkey instructions and a quit button. It minimizes automatically on launch.

#📄 License
This project is open-source and free to use under the MIT License.
