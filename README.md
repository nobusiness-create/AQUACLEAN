# AQUA-CLEAN

## Autonomous Aquatic Waste Collection & Intelligent Segregation System

AQUA-CLEAN is a floating robotic system developed to detect, collect, and manage floating waste from water bodies.

The project combines computer vision, autonomous navigation, proximity-based safety, motor control, conveyor-based waste collection, and web-based monitoring into a single modular robotic platform.

The current system is an engineering prototype under active development and validation.

---

## Overview

AQUA-CLEAN is designed around the following operating pipeline:

```text
Water Body
    ↓
Waste Detection
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
Waste Identification
    ↓
Segregation
    ↓
Storage & Monitoring
```


The robot uses a floating catamaran-style platform with distributed propulsion and a conveyor-based collection mechanism.

A Raspberry Pi 5 acts as the primary computing and control platform.

Core Concept

The software architecture separates perception, decision-making, safety, and actuation:
