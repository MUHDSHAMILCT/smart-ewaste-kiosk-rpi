<div align="center">

# 🌿 Encycle Bank — Smart E-Waste Recycling Kiosk
### Autonomous Raspberry Pi Hardware-Integrated Recycling & Verification System

[![Python](https://img.shields.io/badge/Python-3.9%20%7C%203.10%20%7C%203.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-Raspberry%20Pi%203B+%20%7C%204%20%7C%205-C51A4A?style=for-the-badge&logo=raspberry-pi&logoColor=white)](https://www.raspberrypi.com)
[![Framework](https://img.shields.io/badge/Flask-Web%20%26%20REST%20API-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![Hardware PWM](https://img.shields.io/badge/Actuation-pigpio%20PWM-00599C?style=for-the-badge&logo=raspberrypi&logoColor=white)](https://abyz.me.uk/rpi/pigpio/)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)

<br/>

**Encycle Bank** is a complete, production-ready E-Waste collection and verification kiosk application engineered for **Raspberry Pi OS**. It bridges a modern touch-screen web interface with low-level GPIO hardware control—automating motorized trapdoors, camera inspection, digital verification (Email OTP / WhatsApp), and an EcoCredit reward loyalty engine.

</div>

---

## 📌 Table of Contents
- [✨ Key Features](#-key-features)
- [🏗️ System Architecture](#️-system-architecture)
- [🔌 Hardware & Pinout Wiring](#-hardware--pinout-wiring)
- [📂 Project Directory Structure](#-project-directory-structure)
- [⚡ Quick Start Guide (Automated)](#-quick-start-guide-automated)
- [🛠️ Manual Installation Guide](#️-manual-installation-guide)
- [⚙️ Environment Configuration](#️-environment-configuration)
- [🧪 Hardware Diagnostics & Testing](#-hardware-diagnostics--testing)
- [🚀 24/7 Production Kiosk Service (Systemd)](#-247-production-kiosk-service-systemd)
- [❓ Frequently Asked Questions & Troubleshooting](#-frequently-asked-questions--troubleshooting)
- [🤝 Contributing & License](#-contributing--license)

---

## ✨ Key Features

- **Autonomous Single-Board Design**: Runs entirely on a single Raspberry Pi (4B / 5 / 3B+) without requiring external PCs or microcontrollers.
- **Hardware PWM Trapdoor Actuation**: Zero-jitter servo motor control via the `pigpio` daemon with automatic idle signal cutoff to prevent servo buzzing.
- **Dual Camera Support (HAL)**: Seamlessly operates with the **Official Raspberry Pi Camera (CSI / libcamera)** or plug-and-play **USB Webcams (V4L2 / OpenCV)**.
- **Hardware Abstraction Layer (HAL)**: Includes built-in software simulation (`MOCK_HARDWARE=true`), enabling full UI/backend development and testing on Windows, macOS, or Linux PCs without physical GPIO.
- **Touch Kiosk Touch UI**: Built for 7" to 15" touch displays with an on-screen touchscreen numpad, responsive layouts, and auto-hiding cursor.
- **Verification & Security**: Email OTP delivery (via Gmail SMTP) and WhatsApp receipt integration.
- **EcoCredit Loyalty System**: Automatic credit calculator based on device category, grading, and weight, complete with milestone bonus tiers.
- **24/7 Resilience**: Pre-configured `systemd` service and Chromium autostart script for automated power-on boot into fullscreen kiosk mode.

---

## 🏗️ System Architecture

```
                       ┌───────────────────────────────┐
                       │     TOUCHSCREEN DISPLAY       │
                       │  (Chromium Fullscreen Kiosk)  │
                       └───────────────▲───────────────┘
                                       │ HTTP / WebSockets
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                            RASPBERRY PI (OS)                                │
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                          Flask Backend                              │   │
│   │     • Auth Routes (OTP)           • Devices & Classification        │   │
│   │     • EcoCredits Engine           • SQLite Local Database           │   │
│   └──────────────────┬───────────────────────────────┬──────────────────┘   │
│                      │                               │                      │
│                      ▼                               ▼                      │
│   ┌─────────────────────────────────────┐   ┌───────────────────────────┐   │
│   │    Hardware Abstraction (HAL)       │   │    External Integrations  │   │
│   │  • pigpio / GPIO Servo Driver       │   │  • SMTP Email Gateway     │   │
│   │  • Picamera2 / OpenCV Webcam Driver │   │  • WhatsApp API Provider  │   │
│   └──────────────────┬──────────────────┘   └───────────────────────────┘   │
└──────────────────────┼──────────────────────────────────────────────────────┘
                       │ Low-Level GPIO & CSI / USB
        ┌──────────────┴──────────────┐
        ▼                             ▼
┌──────────────────┐        ┌──────────────────┐
│   MG996R Servo   │        │ Camera (CSI/USB) │
│ (Motorized Door) │        │ (Inspection Box) │
└──────────────────┘        └──────────────────┘
```

---

## 🔌 Hardware & Pinout Wiring

| Component | Wire / Interface | Raspberry Pi Physical Pin | BCM GPIO Number | Recommended Specifications |
| :--- | :--- | :--- | :--- | :--- |
| **Servo PWM Signal** | Orange / Yellow | **Pin 12** | **GPIO 18** | Hardware PWM (PWM0) |
| **Servo Ground** | Brown / Black | **Pin 6 or Pin 14** | **GND** | Must share Common Ground with Pi |
| **Servo 5V Power** | Red | External 5V PSU | — | **5V 2A-3A dedicated supply** (MG996R / MG995) |
| **Official Pi Camera** | Ribbon Cable | CSI Camera Connector | — | `libcamera` / `Picamera2` enabled |
| **USB Webcam** | USB Type-A | Any USB 2.0 / 3.0 Port | `/dev/video0` | Plug-and-play V4L2 device |
| **Touch Display** | Micro-HDMI + USB | Micro-HDMI 0 & USB Port | — | 1024×600 or 1920×1080 Touch Monitor |

> ⚠️ **Important Wiring Note**: Do not power high-torque servos (like the MG996R) directly from the Pi's 5V rail during door actuation, as sudden current spikes can trigger undervoltage resets on the Pi. Use an external 5V 2A power source with common ground.

---

## 📂 Project Directory Structure

```plaintext
├── .env.example              # Template for environment configuration
├── .gitignore                # Rules to keep credentials & database out of git
├── app.py                    # Flask application factory and route coordinator
├── arduino/                  # Optional auxiliary firmware (if used)
├── backend/
│   ├── hardware/             # Camera & Servo Hardware Abstraction Layer (HAL)
│   ├── database/             # SQLite schema and model initialization
│   ├── routes/               # API endpoints (Auth, Device deposit, Rewards)
│   └── services/             # Email OTP, WhatsApp notification dispatchers
├── frontend/
│   ├── static/               # CSS stylesheets, UI assets, and client JS
│   └── templates/            # Single Page Application (SPA) HTML templates
├── scripts/
│   ├── setup_pi.sh           # 1-Click automated system installer
│   ├── run_pi_kiosk.sh       # Script to launch kiosk and Chromium browser
│   ├── test_pi_camera.py     # Diagnostic script for camera sensor
│   └── test_pi_servo.py      # Diagnostic script for trapdoor servo
├── storage/                  # Local runtime profile & image directory
├── ewaste-kiosk.service      # Systemd daemon config for auto-start on boot
└── requirements.txt          # Python library dependencies
```

---

## ⚡ Quick Start Guide (Automated)

On your Raspberry Pi terminal inside this cloned repository:

```bash
# 1. Grant execution permissions
chmod +x scripts/*.sh

# 2. Run the all-in-one setup script
sudo bash scripts/setup_pi.sh
```

The script will automatically install system dependencies, configure permissions, start `pigpiod`, install Python packages, and set up the background system service.

---

## 🛠️ Manual Installation Guide

### Step 1: Update & Install System Packages
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y \
  python3-pip python3-venv python3-full python3-dev \
  python3-picamera2 libcamera-apps \
  python3-gpiozero python3-rpi-lgpio \
  python3-pigpio pigpio \
  chromium-browser unclutter xdotool sqlite3
```

### Step 2: Configure System Permissions & Hardware Daemons
```bash
# Enable camera interface
sudo raspi-config nonint do_camera 0

# Add user to required hardware groups
sudo usermod -a -G gpio,spi,i2c,dialout,video $USER

# Start hardware PWM daemon
sudo systemctl enable pigpiod
sudo systemctl start pigpiod
```

### Step 3: Set Up Python Environment
```bash
python3 -m venv --system-site-packages venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

---

## ⚙️ Environment Configuration

Copy the example environment configuration file:
```bash
cp .env.example .env
nano .env
```

Adjust the parameters for your hardware:
```env
# Set to 'false' on the physical Raspberry Pi, 'true' on developer PC
MOCK_HARDWARE=false

# Camera Mode: 'auto', 'picamera', or 'webcam'
CAMERA_MODE=auto

# Servo Configuration (Hardware Pin 12 = BCM 18)
SERVO_GPIO_PIN=18
SERVO_OPEN_PW=2000     # Open pulse width in microseconds
SERVO_CLOSE_PW=500     # Closed pulse width in microseconds
SERVO_OPEN_SECS=15.0   # Door hold duration (seconds)

# Web Server
HOST=0.0.0.0
PORT=5000
SECRET_KEY=your-secure-random-secret-key

# Email OTP Gateway
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USE_TLS=true
SMTP_EMAIL=your-kiosk-email@gmail.com
SMTP_PASSWORD=your-google-app-password
```

---

## 🧪 Hardware Diagnostics & Testing

Verify that your physical components are functioning properly before launching the full kiosk:

### 1. Test Camera
```bash
python3 scripts/test_pi_camera.py
```
*Captures a test frame and saves it to `storage/test_picamera_capture.jpg`.*

### 2. Test Trapdoor Servo Motor
```bash
python3 scripts/test_pi_servo.py
```
*Rotates the servo to the open position for 5 seconds, closes it, and cuts the PWM signal.*

---

## 🚀 24/7 Production Kiosk Service (Systemd)

To ensure the kiosk runs automatically on startup without manual intervention:

```bash
# Register and start the background service
sudo cp ewaste-kiosk.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable ewaste-kiosk
sudo systemctl start ewaste-kiosk

# Check live service status
sudo systemctl status ewaste-kiosk
```

### Auto-Launch Fullscreen Chromium on Desktop Boot
```bash
mkdir -p ~/.config/autostart
cat << 'EOF' > ~/.config/autostart/kiosk.desktop
[Desktop Entry]
Type=Application
Name=Encycle Bank
Exec=bash -c "sleep 5 && chromium-browser --kiosk --noerrdialogs --disable-infobars --no-first-run --incognito http://localhost:5000"
X-GNOME-Autostart-enabled=true
EOF
```

---

## ❓ Frequently Asked Questions & Troubleshooting

<details>
<summary><b>1. "pigpio daemon not running" error</b></summary>
Run <code>sudo systemctl restart pigpiod</code> and verify it is active with <code>sudo systemctl status pigpiod</code>. The pigpio daemon is required for hardware PWM.
</details>

<details>
<summary><b>2. USB Webcam vs CSI Ribbon Camera</b></summary>
If you are using a standard USB webcam, set <code>CAMERA_MODE=webcam</code> in your <code>.env</code>. Note that <code>rpicam-hello</code> and <code>Picamera2</code> are strictly for CSI ribbon cables and will ignore USB cameras.
</details>

<details>
<summary><b>3. Servo motor jitters or the Pi reboots</b></summary>
High-power servos (e.g. MG996R) draw high current when initiating movement. Power the servo from an external 5V 2A+ power supply rather than directly from the Pi's 5V pins, and ensure the negative terminal is connected to the Pi's GND.
</details>

---

## 🤝 Contributing & License

Contributions, bug reports, and hardware improvements are welcome! Feel free to open an issue or pull request.

Distributed under the **MIT License**. See `LICENSE` for more information.
