# FortiShield
FortiShield is an AI-powered cybersecurity application designed to provide intelligent and real-time malware detection. It combines deep learning with automated system monitoring to protect users from malicious files.

# Features

- Real-time monitoring of Downloads folder using Watchdog
- AI-based malware detection using CNN (Deep Learning)
- Binary-to-image conversion for pattern analysis
- Automatic quarantine of malicious files
- Instant alerts and notifications
- Manual scan for files from any location
- Threat logging system for tracking activity

# Working

1. Monitors Downloads folder continuously
2. Detects new file
3. Converts file → binary image
4. CNN model analyzes patterns
5. Classifies file as Safe / Malicious
6. If malicious → quarantine + alert + log

# Tech Stack

- **Programming Language:** Python
- **Libraries:** TensorFlow, Keras, OpenCV, NumPy, Watchdog
- **GUI:** Tkinter
- **Database:** SQLite
- **Concepts:** Machine Learning, Deep Learning, Cybersecurity

# Project Structure

- `gui/` → User Interface
- `modules/` → Core functionality (scanner, monitor, notifier, etc.)
- `ai_model/` → Trained deep learning model
- `database/` → Logs and threat data
- `main.py` → Entry point

# Note
Dataset is not included due to size constraints.

# Future Scope

- Improve model accuracy with larger dataset
- Add cloud-based threat intelligence
- Real-time system-wide monitoring
- Deploy as a full-scale security application

# Author
Ayana Xavier

