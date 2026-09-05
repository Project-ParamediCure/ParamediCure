# ParamediCure: Fast Triage. Clear Stages. Faster Care.

An integrated AI Project Cycle prototype built for the Class 12 AI Curriculum at Birla Public School, Doha. This project couples a responsive, dark-mode Python frontend interface with an automated, incremental Machine Learning analytics pipeline.

## 🖼️ Project Visual Identity
The system operates under the official branding asset shown below. Ensure this image is saved locally as `paramedicure_logo.png` in the application directory to allow the user interface to load custom branding assets correctly:

<img src="paramedicure_logo.png" width="400" alt="ParamediCure Logo" />

---

## 🏗️ System Architecture
The application layout decouples real-time geolocated UI components from predictive classification math to guarantee stutter-free multi-threaded map execution:

*   **Frontend UI Engine (`ParamediCureApp.py`):** Built natively in Python using `Tkinter` and `tkintermapview`. It implements a customized mathematical **Haversine formula** to handle live straight-line spherical distance mapping. The UI automatically runs spatial updates across an interactive coordinate display canvas assuming a constant ambulance transit performance speed of **45 km/h**.
*   **Machine Learning Pipeline:** Powered by an online classification engine using the `Orange` framework. It loads structural telemetry matrices (`emergency_kiosk_dataset.tab`), applies a **K-Nearest Neighbors (KNN)** predictive model ($K=3$), and continuously appends verified coordinates back into local storage to achieve data-driven **incremental learning**.

---

## 📑 Multi-Stage Medical Triage Framework
The software dynamically scales severity weights using three explicitly structured clinical stages, accessible via interactive desktop control panels:

*   **Stage 1 (Yellow) | Fractures:** Low-to-moderate systemic risk. Covers specialized structural containment routing for Arm, Leg, or Rib fractures.
*   **Stage 2 (Green) | Fainting & Related:** General non-acute observation tracking. Manages triage sequences for dizziness, low blood pressure variations, and mild breathing adjustments.
*   **Stage 3 (Red) | Critical / Cardiac:** High-risk priority interception. Deploys instantaneous routing matrix loops for Cardiac Arrest, Heart Attacks, and active Stroke symptoms.

---

## 📦 Installation & Setup

### 1. Pre-requisites
Ensure you are using a local computer system configured with a desktop display server environment (Windows, macOS, or Linux). This script cannot render windows on a headless cloud console or online development notebooks.

### 2. Dependency Resolution
Install all mandatory external packages, mathematical compilation engines, and image manipulation modules by running the command below in your terminal:

```bash
pip install Orange3 tkintermapview pillow numpy
```

### 3. Execution Sequence
Ensure that both your primary script file and your visual asset (`paramedicure_logo.png`) are located in the same directory path, then boot up the deployment panel:

```bash
python ParamediCureApp.py
```

*Note: If `emergency_kiosk_dataset.tab` is missing during your first launch sequence, the Python engine will automatically synthesize a balanced synthetic dataset of 60 initial geospatial telemetry vector rows to calibrate the classification matrix.*
