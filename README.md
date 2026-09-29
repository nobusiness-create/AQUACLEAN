# AQUA-CLEAN

AQUA-CLEAN is an autonomous aquatic waste collection and intelligent segregation prototype designed for operation in water bodies. The system combines computer vision, autonomous navigation, proximity safety, waste collection, and a web-based monitoring interface.

## System Overview

```text
Camera
  ↓
YOLO Waste Detection
  ↓
Target Selection
  ↓
Navigation
  ↓
Motor Control
  ↓
Waste Collection
  ↓
Return / Dock
```

The Raspberry Pi 5 acts as the main controller. A forward-facing Rapoo USB camera provides the vision input, while ultrasonic sensors and a capacity sensor support safety and collection monitoring.

## Key Features

- YOLO-based waste detection
- Multi-target detection and sequential target selection
- Live camera streaming
- Three-motor propulsion control
- Conveyor-based waste collection
- Dual ultrasonic proximity safety
- IR-based collection-bin capacity monitoring
- Raspberry Pi 5 integration
- Read-only live monitoring dashboard

## Hardware

- Raspberry Pi 5
- Rapoo USB webcam
- 3 propulsion DC motors
- 1 conveyor motor
- 2 × L298N motor drivers
- 2 ultrasonic sensors
- IR capacity sensor
- MPU6050
- 12 V battery
- Floating catamaran-style chassis

## Software

- Python
- OpenCV
- Ultralytics YOLO
- Flask / Flask-SocketIO
- gpiozero
- NumPy
- PyTorch

## Repository Structure

```text
aquaclean/
├── main.py
├── config.py
├── camera.py
├── detector.py
├── navigation.py
├── motors.py
├── conveyor.py
├── ultrasonic.py
├── capacity.py
├── safety.py
├── mission.py
├── dashboard.py
├── remote.py
├── templates/
├── static/
├── tests/
├── models/
└── dataset/
```

## Running on Raspberry Pi

Create and activate the virtual environment:

```bash
python3 -m venv ~/aquaclean-venv
source ~/aquaclean-venv/bin/activate
cd ~/aquaclean
```

Run in commissioning/manual-only mode:

```bash
python main.py --no-autonomous
```

The monitoring interface is served by the Raspberry Pi.

## YOLO Model

The project currently uses a single detection class:

```text
0 = waste
```

The model is trained using a custom dataset and can be retrained as additional real-pool images are collected.

Keep new datasets versioned separately and evaluate a new model before replacing the deployed model.

## Development Status

The project is a functional prototype undergoing hardware commissioning, real-pool validation, and iterative YOLO dataset expansion.

## Safety

Motor power and Raspberry Pi power should be separated appropriately, sensor logic levels must be verified before connection, and autonomous operation should only be enabled after individual hardware and safety tests have passed.
