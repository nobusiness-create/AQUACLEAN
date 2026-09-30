# AQUA-CLEAN

### Autonomous Aquatic Waste Collection & Intelligent Segregation System

AQUA-CLEAN is a floating robotic system designed to detect and collect floating waste from water bodies using computer vision, autonomous navigation, and a conveyor-based collection mechanism.

The system is built around a **Raspberry Pi 5** and a floating catamaran-style platform.

---

## System Workflow

```text
Camera
   ↓
YOLO Waste Detection
   ↓
Target Selection
   ↓
Navigation
   ↓
Waste Collection
   ↓
Return / Docking
   ↓
Unloading
   ↓
Segregation & Monitoring
```

---

## Key Features

- YOLO-based floating waste detection
- Sequential multi-target selection
- Autonomous navigation
- Three-motor propulsion
- Conveyor-based waste collection
- Dual ultrasonic proximity safety
- IR-based collection-bin monitoring
- Raspberry Pi 5 integration
- Live camera monitoring
- Modular control architecture

---

## Hardware

- Raspberry Pi 5
- Rapoo C200 USB Camera
- 3 × DC propulsion motors
- 1 × conveyor motor
- 2 × L298N motor drivers
- 2 × ultrasonic sensors
- IR capacity sensor
- MPU6050 IMU
- 12 V battery
- Floating catamaran-style chassis

---

## Software

- Python
- OpenCV
- Ultralytics YOLO
- PyTorch
- NumPy
- Flask / Flask-SocketIO
- gpiozero
- smbus2
- pytest

Python dependencies are listed in [`requirements.txt`](requirements.txt).

---

## AI-Based Waste Detection

A custom YOLO model is used to detect floating waste.

### Detection Classes

| Class ID | Class |
|---:|---|
| 0 | waste |

The currently deployed model is:

```text
models/best.pt
```

### Baseline Model Results

| Metric | Validation | Held-out Test |
|---|---:|---:|
| Precision | 0.802 | 0.708 |
| Recall | 0.758 | 0.576 |
| mAP@50 | 0.816 | 0.723 |
| mAP@50-95 | 0.484 | 0.297 |

The model will be updated as the AQUA-CLEAN dataset is expanded with more real-water images.

---

## Architecture

```text
Camera
  ↓
Vision / YOLO
  ↓
Target Selection
  ↓
Navigation
  ↓
Safety Layer
  ↓
Motor Control
  ↓
L298N
  ↓
Propulsion / Conveyor
```

Sensors provide additional safety and system-state information to the control layer.

---

## Repository Structure

```text
AQUACLEAN/
├── README.md
├── requirements.txt
├── .gitignore
├── models/
│   └── best.pt
├── dataset/
│   └── data.yaml
├── navigation/
├── vision/
├── docs/
│   └── images/
└── media/
    ├── images/
    └── videos/
```

Large datasets, training runs, backups, and temporary files are kept outside the public repository.

---

## Installation

```bash
git clone https://github.com/nobusiness-create/AQUACLEAN.git
cd AQUACLEAN

python3 -m venv ~/aquaclean-venv
source ~/aquaclean-venv/bin/activate

pip install -r requirements.txt
```

Raspberry Pi deployments may require platform-specific installation of PyTorch and GPIO-related packages.

---

## Running

```bash
cd ~/aquaclean
source ~/aquaclean-venv/bin/activate
python main.py --no-autonomous
```

Autonomous operation should only be enabled after the required hardware and safety checks have been completed.

---

## Media

Project photographs and demonstration videos are organized in:

```text
media/
├── images/
└── videos/
```

More photographs and water-testing demonstrations will be added as the prototype develops.

---

## Development Status

**Current stage:** Active Prototype Development

Current development focuses on:

- Real-water validation
- Propulsion and conveyor integration
- Improved YOLO dataset
- Model refinement
- Navigation refinement
- Docking and unloading
- Intelligent waste segregation

---

## Future Direction

AQUA-CLEAN is being developed toward a more robust autonomous platform capable of:

```text
DETECT
  ↓
LOCALIZE
  ↓
APPROACH
  ↓
COLLECT
  ↓
RETURN
  ↓
UNLOAD
  ↓
SEGREGATE
  ↓
MONITOR
```

---

## Project

**AQUA-CLEAN**  
Autonomous Aquatic Waste Collection & Intelligent Segregation System

**Platform:** Raspberry Pi 5  
**Vision:** Custom YOLO Waste Detection  
**Collection:** Conveyor-Based  
**Propulsion:** Three-Motor System  
**Status:** Active Prototype Development
