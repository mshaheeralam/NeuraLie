# NeuraLie
An AI based tri-modal approach for deception detection

## Abstract
NeuraLie is an AI-based lie detection solution that utilizes the subject's brain waves (EEG signals) along with other elusive physical cues, namely facial expressions and eye-blinking patterns, to detect deception. This particular approach not only aims to address the limitations and inaccuracies of the conventional polygraph but has also aimed to revolutionize the efficacy of lie detection systems in general. The conventional polygraph test uses only physiological responses making them less effective and unreliable, as has been proved over the years. NeuraLie will make use of an EEG headset and a camera, which will send inputs to the NeuraLie web application running on the computer they are connected to. The procedure will be the same as in current lie detection techniques, involving an examiner/interviewer and a subject being monitored by the hardware. The interviewers can get themselves registered, allowing multiple interviewers to make use of the same machine and have their own logs stored locally for future reference. The data collected from the two hardware interfaces, EEG headset, and camera, are sent for processing on the backend, after which they are given as input to the three Deep Learning models that NeuraLie utilizes. The results are ensembled to reach a conclusive result, which is a binary classification between truth and lies.

https://github.com/mshaheeralam/NeuraLie/assets/56303960/d908560f-8338-4fe0-83ad-de529bed9c68

## Demo
https://github.com/mshaheeralam/NeuraLie/assets/56303960/b0428961-68dc-45e2-805b-517ce32a2dda

## How to run
Install dependencies 
```
pip install django
```
Change directory to folder containing these files then
```
python manage.py runserver
```
