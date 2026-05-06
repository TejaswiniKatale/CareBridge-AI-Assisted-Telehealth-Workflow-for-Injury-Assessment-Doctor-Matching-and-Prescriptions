# CareBridge: AI-Assisted Telehealth Workflow for Injury Assessment, Doctor Matching, and Medication-Safe Prescriptions

CareBridge is an AI-assisted telehealth framework designed to support patients from initial injury reporting to doctor consultation, prescription generation, and pharmacy selection. The system combines patient-provided information, image/video-based injury understanding, large language model (LLM) reasoning, and doctor/pharmacy filtering to create a safer and more structured telehealth workflow.

> This project is intended as a research prototype and decision-support system. It does not replace licensed medical professionals or emergency medical care.

---

## 1. Project Overview

In many telehealth platforms, patients may struggle to describe injuries clearly, select the right specialist, or safely understand medication instructions. CareBridge addresses this by creating an end-to-end AI-assisted workflow where:

1. The patient submits symptoms, injury details, images, or a short video.
2. A vision model analyzes visible injury-related cues.
3. An LLM summarizes the case and identifies the likely specialist category.
4. The system recommends doctors based on specialty, rating, price, and availability.
5. The selected doctor reviews the case and generates a prescription.
6. The prescription is forwarded to pharmacy options where the patient can compare prices.

---

## 2. Key Features

### Patient Intake

The system collects structured patient information such as:

- Injury location
- Injury description
- Pain level
- Duration of symptoms
- Cause of injury
- Bleeding, swelling, bruising, or wound presence
- Movement limitation
- Uploaded image or short video

### Image and Video-Based Injury Understanding

The vision module can help identify visible signs such as:

- Wound presence
- Bleeding
- Swelling
- Bruising
- Redness
- Limited movement from short video
- Limping or abnormal motion patterns for leg/knee injuries

Example output:

```json
{
  "injury_group": "knee",
  "wound_detected": true,
  "bleeding_detected": true,
  "limping_detected": true,
  "knee_bending": "limited",
  "confidence": {
    "wound": 0.89,
    "bleeding": 0.84,
    "limping": 0.81
  }
}
```

### LLM-Based Case Summarization

The LLM converts patient input and visual findings into a structured case summary.

Example:

```json
{
  "case_summary": "Patient reports a knee injury after running on the ground. Video suggests visible bleeding around the knee, reduced bending ability, and limping while walking.",
  "possible_severity": "moderate",
  "recommended_specialist": "orthopedic doctor",
  "urgent_flags": [
    "visible bleeding",
    "limited movement",
    "difficulty walking"
  ]
}
```

### Doctor Matching

Doctors can be filtered based on:

- Specialty
- Consultation price
- Ratings
- Availability
- Distance or online availability
- Experience

Example doctor categories:

- Orthopedic doctor
- Dermatologist
- ENT specialist
- Ophthalmologist
- General physician
- Emergency care provider

### Medication-Safe Prescription Workflow

After the consultation, the doctor generates a prescription. The system can support:

- Prescription digitization
- Medication instruction explanation
- Allergy and interaction warnings
- Pharmacy comparison
- Price filtering
- Prescription forwarding to selected pharmacy

---

## 3. System Architecture

The proposed CareBridge workflow is:

```text
Patient Input
    |
    |-- Text symptoms
    |-- Injury image
    |-- Short injury video
    |
    v
Data Preprocessing
    |
    |-- Image frame extraction
    |-- Video frame sampling
    |-- Patient information cleaning
    |
    v
Vision Module
    |
    |-- Injury region detection
    |-- Wound/bleeding/swelling cues
    |-- Movement limitation cues
    |
    v
LLM Reasoning Module
    |
    |-- Case summarization
    |-- Specialist recommendation
    |-- Risk flag extraction
    |
    v
Doctor Recommendation Module
    |
    |-- Specialty filter
    |-- Price filter
    |-- Rating filter
    |-- Availability filter
    |
    v
Doctor Consultation
    |
    v
Prescription Generation
    |
    v
Pharmacy Matching
    |
    |-- Price comparison
    |-- Availability check
    |-- Prescription forwarding
    |
    v
Patient Decision
```

---

## 4. Proposed Technology Stack

### Frontend

- React.js or Next.js
- Tailwind CSS
- Patient upload form
- Doctor and pharmacy filter interface

### Backend

- Python Flask or FastAPI
- REST APIs for patient intake, AI processing, doctor matching, and prescription workflow

### AI/ML Components

- Vision-Language Model for image/video interpretation
- YOLO-based object detection for visible injury cues, if trained data is available
- LLM for case summarization and specialist recommendation
- Rule-based safety layer for urgent flags and medication checks

### Database

- PostgreSQL or MongoDB
- Patient cases
- Doctor profiles
- Pharmacy profiles
- Prescription records

---

## 5. Example Use Case

A patient falls while running and injures their knee.

1. The patient enters:  
   “I was running on the ground and fell. My knee is bleeding and hurts when I bend it.”

2. The patient uploads a 10-second video showing the knee and walking movement.

3. The vision model detects:
   - Visible bleeding
   - Wound around the knee
   - Limping
   - Limited knee bending

4. The LLM generates:
   - A structured summary
   - Recommended specialist: Orthopedic doctor
   - Severity: Moderate
   - Urgent flags: bleeding and movement limitation

5. The patient sees a list of orthopedic doctors with price and rating filters.

6. After consultation, the doctor sends a prescription.

7. The patient compares pharmacies and chooses where to send the prescription.

---


## 6. Research Contribution

The main research goal of this project is to propose a structured AI-assisted telehealth workflow that connects:

- Multimodal patient intake
- Vision-based injury understanding
- LLM-based clinical case summarization
- Specialist recommendation
- Doctor consultation
- Medication-safe prescription handling
- Pharmacy price comparison

This framework aims to improve accessibility, reduce patient confusion, and support safer telehealth decision-making.

---

## 7. Limitations

- The system is not a replacement for doctors or emergency care.
- Injury detection accuracy depends on image/video quality.
- YOLO-based detection requires task-specific training data.
- LLM outputs must be verified by medical professionals.
- Prescription generation should only be performed by licensed doctors.
- The prototype may not handle all injury categories or emergency conditions.

---

## 8. Future Work

- Train a custom injury detection model using verified medical image/video datasets.
- Add real-time video-based motion analysis.
- Improve specialist recommendation using doctor availability and patient location.
- Add medication allergy and drug interaction checking.
- Integrate pharmacy APIs for real-time price comparison.
- Conduct user studies with patients and healthcare professionals.
- Evaluate model performance using accuracy, precision, recall, F1-score, and clinical safety metrics.

---

## 9. Disclaimer

CareBridge is a research prototype for AI-assisted telehealth workflow support. It should not be used as a standalone medical diagnosis or treatment system. All medical decisions must be reviewed and approved by licensed healthcare professionals.



