# NeuraLie  
Tri-modal deception detection using EEG, facial expressions, and eye-blink patterns.  

🏆 **Winner – Jury’s Choice Award, Microsoft Imagine Cup 2023 (Pakistan)**  

---

## 🚀 Overview  
NeuraLie is a multimodal lie detection system that integrates **EEG signals**, **facial expression analysis**, and **eye-blink patterns** to classify truth vs. deception.  
The system fuses multiple models through ensembling to achieve higher robustness and accuracy compared to unimodal approaches.  

It was developed as part of the **Microsoft Imagine Cup 2023**, where it won the Jury’s Choice Award in Pakistan.  

---

## 🎥 Demo  

- **[Project Overview (Slides)](https://github.com/mshaheeralam/NeuraLie/assets/56303960/d908560f-8338-4fe0-83ad-de529bed9c68)** – High-level presentation explaining NeuraLie’s approach, modalities, and motivation.  
- **[Live System Demo](https://github.com/mshaheeralam/NeuraLie/assets/56303960/b0428961-68dc-45e2-805b-517ce32a2dda)** – Full walkthrough of NeuraLie in action, showing facial + eye-blink detection working together.  

---

## ✨ Features  
- **Tri-modal fusion** – EEG brainwave analysis + eye-blink patterns + facial expressions.  
- **Model ensembling** – Combines outputs from multiple models for reliable classification.  
- **Research-oriented design** – Built to test real-time multimodal biometrics.  
- **Web application** – Django-powered interface for interviewer login, data capture, and result storage.  

---

## 🧩 Architecture  

```text
EEG Headset  ─┐
               ├─> Signal Processing ─┐
Camera       ──┘                      ├─> Deep Models (EEG / Face / Blink) ──> Ensemble ──> Truth/Lie
Django Web App (UI + control + local logging)
```

---

## 🛠️ Tech Stack  
- **Languages**: Python  
- **Frameworks**: Django, OpenCV, scikit-learn, TensorFlow/PyTorch  
- **Modalities**: EEG signals, blink detection, facial expression recognition  
- **Deployment**: Local machine (single-user web app)  

---

## ⚡ Quickstart  

1. Clone the repository:  
```bash
git clone https://github.com/mshaheeralam/neuralie.git
cd neuralie
```

2. Install dependencies:  
```bash
pip install -r requirements.txt
```

3. Run the Django app:  
```bash
python manage.py runserver
```

> Note: Pretrained models and EEG data are not included due to size and privacy. Instructions are provided in the repo to plug in your own data/models.  

---

## 📂 Suggested Repository Structure  
```
neuralie/
  ├─ app/                 # Django app (views, urls, templates)
  ├─ models/              # Trained models / weights (gitignored if large)
  ├─ processing/          # EEG/vision preprocessing + feature extraction
  ├─ data/                # Sample inputs (gitignored)
  ├─ README.md
  └─ manage.py
```

---

## 🔮 Roadmap / Future Work  
- Expand dataset with additional subjects.  
- Containerize for reproducible deployments (Docker/Kubernetes).  
- Add inference API for external integrations.  
