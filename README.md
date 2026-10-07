# NeuraLie

Deception detection from video: a Django web app that records an interview and classifies each answer as truth or lie from the subject's **facial expressions** and **eye-blink patterns**.

🏆 **Jury's Choice Award, Microsoft Imagine Cup 2023 (Pakistan)**

NeuraLie was our final-year project in BS Computer Science at the Ghulam Ishaq Khan Institute (GIKI), built by a team of four:
Muhammad Maaz Tariq, Shaheer Alam, Mohammad Arslan and Muhammad Afzal, supervised by Dr. Zahid Halim. The full report is in [`Thesis.pdf`](Thesis.pdf).

---

## How it works

Deception shows up as *changes* over time, not in a single frame. So the system looks at the whole recorded answer, not one image.

```text
Recorded answer (video)
   │
   ├─> Face per frame ─> pretrained emotion CNN (fer.h5) ─> 2,048 features per frame
   │                                                          └─> GRU model ─> P(truth)
   │
   └─> Facial landmarks (dlib) ─> blink count and rate ─> blink classifier ─> P(lie)
                                                                  │
                                         simple threshold rule ─> final verdict
```

- **Facial expressions** (`BACKEND/Modality2_FacialExpressions`): up to 600 frames per answer. Each face goes through a pretrained 7-emotion CNN, used as a feature extractor. A Keras model (Conv1D + two GRU layers) reads the 600 × 2,048 sequence and outputs truth or lie.
- **Eye blinks** (`BACKEND/Modality1_EyeBlink`): dlib facial landmarks detect blinks across the video. A trained classifier (`my_blink_model.pkl`) predicts truth or lie from the blink statistics.
- **Final verdict**: a threshold rule combines the two probabilities (see `demo` in `FRONTEND/views.py`).
- **Web app** (`FRONTEND`, `Neuralie`): Django. Interviewers register and log in, record answers, and see results and logs stored locally.

### What about EEG?
The original design was **tri-modal** and added EEG brainwave signals (see the thesis). Our EEG headset failed during the project and a replacement could not be sourced in time, so with our supervisor's approval the final system uses two modalities. `BACKEND/Modality3_EEG` is an empty placeholder from that plan.

## Dataset

We built our own dataset by filming students on campus answering questions truthfully and deceptively. **The videos are not included in this repository** to protect the participants' privacy.

The demo page reads videos from a local `Data/` folder (ignored by Git). To try it, add your own recordings there, named `trial_lie_<n>.mp4` or `trial_truth_<n>.mp4`.

## Running it locally

Built in 2023 with Python 3.9. Install dependencies and start the Django server:

```bash
pip install -r requirements.txt
```

```bash
python manage.py migrate
```

```bash
python manage.py runserver
```

The trained models are included in `BACKEND/`. Settings read `DJANGO_SECRET_KEY` and `DJANGO_DEBUG` from the environment; the defaults are for local development only.

## Tech stack

Python · Django · TensorFlow / Keras (CNN, GRU) · OpenCV · dlib · NumPy · SciPy

## License

See [LICENSE](LICENSE).
