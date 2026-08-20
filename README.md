# ParamediCure: Fast triage. Clear stages. Faster care
An integrated AI Project Cycle prototype built for the Class 12 AI Curriculum. This project decouples a high-performance Python frontend interface from an ensemble Machine Learning analytics pipeline.
# <img width="512" height="683" alt="sfkaxasvap3g1" src="https://github.com/user-attachments/assets/cc1b8ec9-92e5-408f-a362-3ce1f8c55730" />

# System Architecture
- **Frontend UI Engine (`ParamediCureApp.py`):** Built natively in Python using `Tkinter` and `tkintermapview`. Handles multi-threaded geolocated routing, custom trigonometry-based Haversine distance tracking, and localized edge-data logging.
- **Machine Learning Backend (`orange_workflow.ows`):** An analytical framework built in Orange Data Mining. Uses an unsupervised Preprocessing pipeline paired with a Supervised **Random Forest Classifier** to evaluate clinical features and predict patient outcomes.

# AI Domains & Features Tracked
- **Domain:** Data Science & Machine Learning (Supervised Predictive Classification)
- **Key Features:** Patient Age, Gender, Income Level, Kiosks per 10k population, Distance to Kiosk, Diagnosis Delay, and Treatment Adherence.
- **Target Variable:** `Outcome` (Categorized as Improved, Stable, or Worsened)


Installation & Setup
1. Clone the repository.
2. Install required dependencies: `pip install tkintermapview`
3. Launch the operational kiosk: `python ParamediCureApp.py`
4. Open `orange_workflow.ows` inside Orange Data Mining to view the ML validation matrices.
