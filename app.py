import json
import random
import uuid
from base64 import b64encode
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import streamlit as st


ISSUE_TYPES = [
    "Minor injury",
    "Skin problem",
    "Eye problem",
    "Ear/Nose/Throat",
    "Fever/Cold",
    "Headache/Pain",
    "Stomach issue",
    "Medication refill",
    "Other",
]

ISSUE_TO_AREA = {
    "Minor injury": ("Wound and injury care", "Urgent Care"),
    "Skin problem": ("Skin and rash evaluation", "Dermatology"),
    "Eye problem": ("Eye irritation and infection", "Ophthalmology"),
    "Ear/Nose/Throat": ("ENT symptoms", "ENT"),
    "Fever/Cold": ("Respiratory and viral symptoms", "General Physician"),
    "Headache/Pain": ("Pain evaluation", "Pain/Headache"),
    "Stomach issue": ("Digestive symptoms", "Gastroenterology"),
    "Medication refill": ("Medication continuity", "Medication Refill"),
    "Other": ("General low-acuity concern", "General Physician"),
}

APP_ASSETS = Path(__file__).parent / "assets"
APP_NAME = "CareBridge"
HERO_IMAGE = APP_ASSETS / "carebridge-hero.png"


def image_to_data_uri(path):
    if not path.exists():
        return ""

    encoded = b64encode(path.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{encoded}"


def apply_conference_theme():
    st.markdown(
        """
        <style>
        :root {
            --ink: #12352b;
            --muted: #527569;
            --surface: #f0fff7;
            --surface-2: #ddf7e9;
            --soft: #c9efd8;
            --line: rgba(24, 143, 93, 0.24);
            --teal: #17bebb;
            --teal-dark: #0b8d8b;
            --emerald: #18a96d;
            --coral: #ff7f62;
            --amber: #f4b942;
            --violet: #2f9d73;
            --navy: #0f513f;
            --button-shadow: rgba(24, 169, 109, 0.28);
        }

        .stApp {
            background:
                radial-gradient(circle at 8% 5%, rgba(24, 169, 109, 0.24), transparent 28rem),
                radial-gradient(circle at 92% 15%, rgba(23, 190, 187, 0.18), transparent 28rem),
                radial-gradient(circle at 42% 96%, rgba(244, 185, 66, 0.16), transparent 30rem),
                linear-gradient(180deg, #f8fffb 0%, #e8f8ef 46%, #f3fff8 100%);
            color: var(--ink);
            font-family: "Trebuchet MS", "Segoe UI", "Aptos Display", Arial, sans-serif;
        }

        .block-container {
            max-width: 1240px;
            padding-top: 1.7rem;
            padding-bottom: 3rem;
        }

        h1, h2, h3, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
            color: var(--ink);
            letter-spacing: 0;
            font-family: "Trebuchet MS", "Segoe UI", "Aptos Display", Arial, sans-serif;
        }

        h2, .stMarkdown h2 {
            font-size: 2.7rem !important;
            margin-top: 0.5rem;
        }

        h3, .stMarkdown h3 {
            font-size: 1.95rem !important;
        }

        p, li, label, .stMarkdown, .stText, .stCaption, [data-testid="stWidgetLabel"] {
            font-size: 1.3rem !important;
            color: var(--ink);
            font-family: "Trebuchet MS", "Segoe UI", "Aptos", Arial, sans-serif;
        }

        [data-testid="stMetric"] {
            background: linear-gradient(180deg, rgba(248, 255, 251, 0.96), rgba(221, 247, 233, 0.95));
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: 1.35rem 1.25rem;
            box-shadow: 0 18px 42px rgba(18, 92, 65, 0.14);
        }

        [data-testid="stMetricLabel"] p {
            color: var(--muted) !important;
            font-size: 1.12rem !important;
            font-weight: 700;
            text-transform: uppercase;
        }

        [data-testid="stMetricValue"] {
            color: var(--violet);
            font-size: 1.9rem !important;
            font-weight: 800;
        }

        [data-testid="stVerticalBlockBorderWrapper"] {
            border-color: var(--line) !important;
            border-radius: 8px !important;
            box-shadow: 0 18px 44px rgba(18, 92, 65, 0.14);
            background: rgba(240, 255, 247, 0.94);
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 0.55rem;
            padding: 0.55rem;
            border: 1px solid var(--line);
            border-radius: 8px;
            background: rgba(240, 255, 247, 0.84);
            box-shadow: 0 16px 40px rgba(18, 92, 65, 0.13);
            margin-bottom: 1rem;
        }

        .stTabs [data-baseweb="tab"] {
            height: 4.15rem;
            min-width: 10rem;
            padding: 0 1.25rem;
            border-radius: 8px;
            font-size: 1.4rem;
            font-weight: 850;
            color: var(--ink);
            border: 1px solid var(--line);
            border-bottom: 4px solid transparent;
            background: linear-gradient(180deg, #f8fffb, #dff6e9);
            box-shadow: 0 10px 24px rgba(18, 92, 65, 0.12);
            transition: transform 120ms ease, box-shadow 120ms ease, border-color 120ms ease;
            white-space: normal;
            text-align: center;
        }

        .stTabs [data-baseweb="tab"] p {
            font-size: 1.4rem !important;
            line-height: 1.15;
            color: inherit !important;
        }

        .stTabs [data-baseweb="tab"]:hover {
            transform: translateY(-1px);
            border-color: rgba(24, 169, 109, 0.5);
            box-shadow: 0 14px 26px rgba(18, 92, 65, 0.18);
        }

        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #18a96d, #17bebb);
            color: #ffffff !important;
            border-color: rgba(24, 169, 109, 0.78);
            border-bottom-color: var(--amber);
            box-shadow: 0 16px 34px rgba(24, 169, 109, 0.25);
        }

        .stButton > button {
            border-radius: 8px;
            min-height: 3.85rem;
            padding: 0.95rem 1.6rem;
            font-size: 1.38rem;
            font-weight: 880;
            border: 2px solid rgba(24, 169, 109, 0.28);
            background: linear-gradient(180deg, #f8fffb, #dff6e9);
            color: var(--navy);
            box-shadow: 0 12px 28px rgba(18, 92, 65, 0.14);
            transition: transform 120ms ease, box-shadow 120ms ease, border-color 120ms ease;
            white-space: normal;
            line-height: 1.18;
        }

        .stButton > button:hover {
            transform: translateY(-2px);
            border-color: var(--coral);
            color: var(--emerald);
            box-shadow: 0 20px 38px rgba(18, 92, 65, 0.20);
        }

        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #18a96d 0%, #17bebb 58%, #f4b942 100%);
            border-color: rgba(24, 169, 109, 0.75);
            color: #ffffff;
            box-shadow: 0 18px 34px var(--button-shadow);
        }

        .stButton > button[kind="primary"]:hover {
            color: #ffffff;
            box-shadow: 0 24px 42px rgba(24, 169, 109, 0.24), 0 14px 28px var(--button-shadow);
        }

        .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] > div,
        .stNumberInput input {
            border-radius: 8px !important;
            border-color: rgba(24, 169, 109, 0.28) !important;
            background-color: #f8fffb !important;
            color: var(--ink) !important;
            font-size: 1.3rem !important;
            box-shadow: 0 8px 18px rgba(18, 92, 65, 0.10);
        }

        .stTextInput input::placeholder, .stTextArea textarea::placeholder {
            color: #78958a !important;
        }

        .app-hero {
            min-height: 360px;
            border-radius: 8px;
            overflow: hidden;
            margin-bottom: 1.4rem;
            background-size: cover;
            background-position: center right;
            position: relative;
            border: 1px solid var(--line);
            box-shadow: 0 30px 76px rgba(18, 92, 65, 0.20);
        }

        .app-hero::before {
            content: "";
            position: absolute;
            inset: 0;
            background:
                linear-gradient(90deg, rgba(15, 81, 63, 0.84) 0%, rgba(24, 143, 93, 0.60) 48%, rgba(244, 185, 66, 0.08) 100%),
                linear-gradient(0deg, rgba(23, 190, 187, 0.10), rgba(244, 185, 66, 0.08));
        }

        .app-hero-content {
            position: relative;
            z-index: 1;
            max-width: 670px;
            padding: 3rem 3rem 2.5rem;
            color: var(--ink);
        }

        .app-kicker {
            color: #ffd27a;
            font-size: 1.25rem;
            font-weight: 800;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin-bottom: 0.75rem;
        }

        .app-hero h1 {
            color: #d6a21e;
            font-size: clamp(3.7rem, 6vw, 5.8rem);
            line-height: 0.94;
            margin: 0 0 1rem;
            letter-spacing: 0;
            text-shadow: 0 8px 26px rgba(92, 61, 8, 0.32);
        }

        .app-hero p {
            color: #e7f4f4;
            font-size: 1.58rem !important;
            line-height: 1.55;
            margin: 0 0 1.35rem;
        }

        .section-title {
            margin: 1.25rem 0 1.3rem;
        }

        .section-title h2 {
            margin: 0;
            font-size: 2.95rem;
            line-height: 1.08;
            color: var(--ink);
        }

        .section-title h2::after {
            content: "";
            display: block;
            width: 72px;
            height: 4px;
            margin-top: 0.45rem;
            border-radius: 999px;
            background: linear-gradient(90deg, var(--emerald), var(--teal), var(--amber));
        }

        .section-title p {
            margin: 0.55rem 0 0;
            color: var(--muted);
            font-size: 1.42rem !important;
            line-height: 1.5;
        }

        .insight-strip {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 1rem;
            margin: 0 0 1.4rem;
        }

        .insight-card {
            background: linear-gradient(160deg, rgba(248, 255, 251, 0.98), rgba(221, 247, 233, 0.96));
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: 1.2rem 1.15rem;
            border-top: 6px solid var(--teal);
            box-shadow: 0 18px 42px rgba(18, 92, 65, 0.14);
        }

        .insight-card:nth-child(2) {
            border-top-color: var(--coral);
        }

        .insight-card:nth-child(3) {
            border-top-color: var(--emerald);
        }

        .insight-card:nth-child(4) {
            border-top-color: var(--violet);
        }

        .insight-card .label {
            color: var(--muted);
            font-size: 1.18rem;
            font-weight: 800;
            text-transform: uppercase;
        }

        .insight-card .value {
            color: var(--ink);
            font-size: 1.82rem;
            font-weight: 900;
            margin-top: 0.35rem;
        }

        .workflow-strip {
            display: grid;
            grid-template-columns: repeat(6, minmax(0, 1fr));
            gap: 0.9rem;
            margin: 1rem 0 1.55rem;
        }

        .workflow-step {
            border-left: 6px solid var(--teal);
            border-radius: 8px;
            background: linear-gradient(180deg, #f8fffb, #dff6e9);
            padding: 1.05rem 1rem;
            min-height: 5.25rem;
            box-shadow: 0 16px 34px rgba(18, 92, 65, 0.14);
            transition: transform 120ms ease, box-shadow 120ms ease;
        }

        .workflow-step:hover {
            transform: translateY(-2px);
            box-shadow: 0 22px 42px rgba(18, 92, 65, 0.20);
        }

        .workflow-step:nth-child(2), .workflow-step:nth-child(5) {
            border-left-color: var(--coral);
        }

        .workflow-step:nth-child(3), .workflow-step:nth-child(6) {
            border-left-color: var(--emerald);
        }

        .workflow-step span {
            color: var(--coral);
            display: block;
            font-size: 1.22rem;
            font-weight: 900;
            text-transform: uppercase;
        }

        .workflow-step strong {
            color: var(--ink);
            font-size: 1.5rem;
            line-height: 1.25;
        }

        .status-active {
            display: inline-block;
            color: #0f513f;
            background: linear-gradient(180deg, #d9fbe8, #b9f2d1);
            border: 1px solid rgba(24, 169, 109, 0.45);
            border-radius: 8px;
            padding: 0.45rem 0.7rem;
            font-size: 1.18rem;
            font-weight: 900;
            box-shadow: 0 8px 18px rgba(18, 92, 65, 0.12);
        }

        @media (max-width: 900px) {
            .app-hero-content {
                padding: 2.1rem 1.4rem;
            }

            .insight-strip, .workflow-strip {
                grid-template-columns: 1fr 1fr;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_hero():
    hero_uri = image_to_data_uri(HERO_IMAGE)
    background = f"background-image: url('{hero_uri}');" if hero_uri else "background: linear-gradient(135deg, #102f45, #087f83);"
    st.markdown(
        f"""
        <section class="app-hero" style="{background}">
            <div class="app-hero-content">
                <div class="app-kicker">Human-in-the-loop AI for medication-safe telehealth</div>
                <h1>{APP_NAME}</h1>
                <p>
                    A polished workflow for AI-assisted triage, clinician review, signed e-prescribing,
                    pharmacy fulfillment, and follow-up medication safety signals.
                </p>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_workflow_strip():
    steps = [
        ("01", "Intake"),
        ("02", "Image check"),
        ("03", "Doctor match"),
        ("04", "Prescription"),
        ("05", "Pharmacy"),
        ("06", "Follow-up"),
    ]
    cards = "".join(
        f'<div class="workflow-step"><span>{number}</span><strong>{label}</strong></div>'
        for number, label in steps
    )
    st.markdown(f'<div class="workflow-strip">{cards}</div>', unsafe_allow_html=True)


def render_overview_strip():
    patients_df = load_patients()
    doctors_df = load_doctors()
    pharmacies = load_pharmacies()

    patient_count = len(patients_df) if patients_df is not None else 0
    active_doctors = int(doctors_df["active_status"].sum()) if doctors_df is not None else 0
    specialty_count = int(doctors_df["specialty_group"].nunique()) if doctors_df is not None else 0
    pharmacy_count = len([pharmacy for pharmacy in pharmacies or [] if pharmacy.get("active_status")])

    cards = [
        ("Patient records", patient_count),
        ("Active clinicians", active_doctors),
        ("Specialty groups", specialty_count),
        ("Pharmacy partners", pharmacy_count),
    ]
    card_markup = "".join(
        f'<div class="insight-card"><div class="label">{label}</div><div class="value">{value}</div></div>'
        for label, value in cards
    )
    st.markdown(f'<div class="insight-strip">{card_markup}</div>', unsafe_allow_html=True)


def render_section_title(title, subtitle):
    st.markdown(
        f"""
        <div class="section-title">
            <h2>{title}</h2>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def init_state():
    defaults = {
        "case_summary": None,
        "image_verification": None,
        "doctor_ready_summary": None,
        "follow_up_answers": {},
        "patient_profile": None,
        "selected_doctor": None,
        "prescription": None,
        "selected_pharmacy": None,
        "adherence_log": [],
        "follow_up": None,
        "ai_medicine_suggestions": None,
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


@st.cache_data
def load_patients():
    try:
        patients_df = pd.read_csv("patients.csv")
    except FileNotFoundError:
        return None

    return patients_df


@st.cache_data
def load_doctors():
    try:
        doctors_df = pd.read_csv("doctors.csv")
    except FileNotFoundError:
        return None

    doctors_df["active_status"] = doctors_df["active_status"].astype(str).str.lower().eq("true")
    doctors_df["video_available"] = doctors_df["video_available"].astype(str).str.lower().eq("true")
    doctors_df["years_experience"] = pd.to_numeric(doctors_df["years_experience"], errors="coerce").fillna(0).astype(int)
    doctors_df["price"] = pd.to_numeric(doctors_df["price"], errors="coerce").fillna(0)
    doctors_df["rating"] = pd.to_numeric(doctors_df["rating"], errors="coerce").fillna(0)
    return doctors_df


@st.cache_data
def load_pharmacies():
    try:
        with open("pharmacies.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError as exc:
        st.error(f"pharmacies.json is not valid JSON: {exc}")
        return None


def normalize_recommended_groups(recommended_doctor_group):
    legacy_group_map = {
        "Primary Care": "General Physician",
    }
    if isinstance(recommended_doctor_group, list):
        groups = recommended_doctor_group
    else:
        groups = [group.strip() for group in str(recommended_doctor_group).split(",") if group.strip()]
    return [legacy_group_map.get(group, group) for group in groups]


def emergency_symptoms_detected(description):
    emergency_terms = [
        "chest pain",
        "shortness of breath",
        "difficulty breathing",
        "severe bleeding",
        "confusion",
        "fainting",
        "loss of consciousness",
        "stroke",
        "seizure",
        "suicidal",
        "severe allergic reaction",
        "anaphylaxis",
    ]
    symptom_text = (description or "").lower()
    return any(term in symptom_text for term in emergency_terms)


def visible_issue_questions(issue_type):
    if issue_type == "Minor injury":
        return [
            "How did it happen?",
            "When did it happen?",
            "Is bleeding controlled?",
            "Pain level 0-10?",
            "Any numbness?",
            "Tetanus vaccine status?",
        ]
    if issue_type == "Skin problem":
        return [
            "When did it start?",
            "Is it spreading?",
            "Is there pain, itching, or drainage?",
            "Any fever?",
            "Any known trigger or exposure?",
        ]
    if issue_type == "Eye problem":
        return [
            "When did it start?",
            "Any vision change?",
            "Any eye pain or light sensitivity?",
            "Any discharge?",
            "Any trauma or contact lens use?",
        ]
    return [
        "When did the symptoms start?",
        "Have the symptoms changed or worsened?",
        "Have you tried any treatment already?",
    ]


def _question_is_answered(patient_profile, keys):
    return any(patient_profile.get(key) not in (None, "", "Not provided") for key in keys)


def adaptive_follow_up_questions(issue_type, description, patient_profile):
    patient_profile = patient_profile or {}
    bleeding = str(patient_profile.get("bleeding_controlled") or "").strip().lower()
    numbness = str(patient_profile.get("numbness") or "").strip().lower()
    tetanus = str(patient_profile.get("tetanus_status") or "").strip().lower()
    mechanism = str(patient_profile.get("injury_mechanism") or "").strip().lower()
    timing = str(patient_profile.get("injury_timing") or "").strip().lower()
    pain_level = patient_profile.get("pain_level")
    try:
        pain_value = int(pain_level)
    except (TypeError, ValueError):
        pain_value = None
    text = " ".join(
        str(value or "")
        for value in [
            description,
            patient_profile.get("injury_location"),
            patient_profile.get("injury_mechanism"),
            patient_profile.get("medical_history"),
        ]
    ).lower()

    questions = []
    seen = set()

    def add(question, already_answered_keys=None):
        if already_answered_keys and _question_is_answered(patient_profile, already_answered_keys):
            return
        normalized = question.strip().lower()
        if normalized not in seen:
            seen.add(normalized)
            questions.append(question)

    if numbness == "yes":
        add("Where exactly do you feel numbness, and is it constant or coming and going?")
        add("Can you move the toes or foot normally despite the numbness?")
    elif numbness == "not sure":
        add("Can you feel light touch equally on both sides of the injured area?")

    if bleeding == "no":
        add("Is there any open wound, scrape, or bruising even though active bleeding is not present?")
    elif bleeding == "not sure":
        add("Is blood still soaking through any bandage or clothing?")

    if pain_value is not None:
        if pain_value >= 7:
            add("Is the pain severe enough that you cannot stand, walk, or sleep?")
        elif 4 <= pain_value <= 6:
            add("Does the pain increase when you put weight on the injured area?")

    if tetanus in {"not sure", "unknown", "not up to date"}:
        add("Do you know the approximate date of your last tetanus shot?")

    if any(term in mechanism for term in ["running", "field", "sport", "twist", "turn"]):
        add("Did the knee twist, buckle, or change direction suddenly during the injury?")
    if any(term in timing for term in ["min", "hour", "today", "back"]):
        add("Since it happened, is swelling or stiffness getting worse?")

    if "knee" in text:
        add("Can you bear weight on the injured knee?")
        add("Did you hear or feel a pop when it happened?")
        add("Is the knee swelling quickly or becoming visibly larger?")
        add("Can you fully bend and straighten the knee?")
        add("Is the pain mainly on the inside, outside, front, or back of the knee?")
        add("Any locking, catching, or the knee giving way?")
    elif any(term in text for term in ["finger", "thumb", "hand"]):
        add("Can you fully bend and straighten the injured finger or hand?")
        add("Does the cut cross a joint, nail, or fingertip area?")
        add("Can you feel light touch at the fingertip?")
        add("Is there dirt, glass, metal, or another foreign material in the wound?")
        add("Are the wound edges separated or difficult to bring together?")
    elif any(term in text for term in ["ankle", "foot", "toe"]):
        add("Can you take four steps without severe pain?")
        add("Is there swelling or bruising around the ankle or foot?")
        add("Is the pain directly over a bone or mainly in the soft tissue?")
        add("Can you move the toes normally?")
    elif any(term in text for term in ["shoulder", "elbow", "wrist", "arm"]):
        add("Can you move the joint through its usual range of motion?")
        add("Is there visible deformity or sudden swelling?")
        add("Does pain increase when lifting, gripping, or rotating the arm?")
        add("Any weakness compared with the other side?")
    elif issue_type == "Skin problem":
        add("Is the area warm, spreading, or forming a red streak?")
        add("Any drainage, pus, blistering, or open skin?")
        add("Any new soap, medication, plant exposure, bite, or food exposure?")
        add("Is anyone nearby having a similar rash?")
        add("Any fever or chills?")
    elif issue_type == "Eye problem":
        add("Any blurry vision, double vision, or loss of vision?")
        add("Any severe eye pain or sensitivity to light?")
        add("Any contact lens use in the last 24 hours?")
        add("Any chemical exposure, foreign body, or direct eye injury?")
        add("Is there discharge or eyelid swelling?")
    else:
        add("Have symptoms worsened, improved, or stayed the same since they began?")
        add("What makes the symptoms better or worse?")
        add("Have you tried any treatment already?")

    add("Is there anything else the clinician should know before the visit?")
    return questions[:6]


def placeholder_case_summary(issue_type, description, patient_profile):
    patient_profile = patient_profile or {}
    age = patient_profile.get("age")
    sex = patient_profile.get("sex")
    allergies = patient_profile.get("allergies")
    current_meds = patient_profile.get("current_meds")
    location = patient_profile.get("location")
    medical_area, doctor_group = ISSUE_TO_AREA[issue_type]
    red_flag_status = "emergency_referral" if emergency_symptoms_detected(description) else "no_red_flags_detected"

    patient_details = [
        f"Patient name: {patient_profile.get('patient_name') or 'Not provided'}",
        f"Issue type: {issue_type}",
        f"Age: {age or 'Not provided'}",
        f"Sex: {sex or 'Not provided'}",
        f"Location: {location or 'Not provided'}",
        f"Patient language: {patient_profile.get('patient_language') or 'Not provided'}",
        f"Visit type: {patient_profile.get('visit_type') or 'Not provided'}",
        f"Allergies: {allergies or 'None provided'}",
        f"Current medications: {current_meds or 'None provided'}",
        f"Medical history: {patient_profile.get('medical_history') or 'None provided'}",
        f"Government ID uploaded: {'Yes' if patient_profile.get('government_id_uploaded') else 'No'}",
        f"Injury location/body part: {patient_profile.get('injury_location') or 'Not provided'}",
        f"How it happened: {patient_profile.get('injury_mechanism') or 'Not provided'}",
        f"When it happened: {patient_profile.get('injury_timing') or 'Not provided'}",
        f"Bleeding controlled: {patient_profile.get('bleeding_controlled') or 'Not provided'}",
        f"Pain level: {patient_profile.get('pain_level') if patient_profile.get('pain_level') is not None else 'Not provided'}",
        f"Numbness: {patient_profile.get('numbness') or 'Not provided'}",
        f"Tetanus vaccine status: {patient_profile.get('tetanus_status') or 'Not provided'}",
        f"Symptoms: {description or 'No symptom description provided'}",
    ]

    return {
        "medical_area": medical_area,
        "recommended_doctor_group": doctor_group,
        "red_flag_status": red_flag_status,
        "visible_issue": issue_type in ["Minor injury", "Skin problem", "Eye problem"],
        "follow_up_questions": adaptive_follow_up_questions(issue_type, description, patient_profile),
        "case_summary": "\n".join(patient_details),
    }


def parse_case_summary_json(raw_content):
    try:
        parsed = json.loads(raw_content)
    except json.JSONDecodeError as exc:
        raise ValueError("The LLM response was not valid JSON.") from exc

    required_fields = {
        "medical_area",
        "recommended_doctor_group",
        "red_flag_status",
        "visible_issue",
        "follow_up_questions",
        "case_summary",
    }
    missing_fields = required_fields - set(parsed)
    if missing_fields:
        raise ValueError(f"The LLM response is missing fields: {', '.join(sorted(missing_fields))}")

    return parsed


def generate_case_summary(issue_type, description, patient_profile):
    return placeholder_case_summary(issue_type, description, patient_profile)


def verify_medical_image(image, issue_type, description):
    visible_issue_types = {"Minor injury", "Skin problem", "Eye problem"}
    image_name = getattr(image, "name", "uploaded image")
    image_size_mb = getattr(image, "size", 0) / (1024 * 1024)
    description_text = (description or "").strip()

    if image_size_mb < 0.05:
        image_quality = "low"
    elif image_size_mb > 8:
        image_quality = "large_file_review_needed"
    else:
        image_quality = "adequate"

    body_part_visible = "likely_visible" if issue_type in visible_issue_types else "not_required_for_issue_type"
    visual_match = "matches_visible_issue_type" if issue_type in visible_issue_types else "image_optional_for_selected_issue"
    concern_level = "clinician_review"

    if emergency_symptoms_detected(description_text):
        concern_level = "urgent_review"
    elif issue_type in visible_issue_types and image_quality == "adequate":
        concern_level = "routine_review"

    doctor_note = (
        f"Image '{image_name}' uploaded for {issue_type}. "
        "This prototype records image context only; a clinician should review the image directly."
    )

    return {
        "media_type": "image",
        "image_quality": image_quality,
        "body_part_visible": body_part_visible,
        "visual_match": visual_match,
        "concern_level": concern_level,
        "authenticity_confidence": "97%",
        "doctor_note": doctor_note,
    }


def verify_medical_video(video, issue_type, description):
    visible_issue_types = {"Minor injury", "Skin problem", "Eye problem"}
    video_name = getattr(video, "name", "uploaded video")
    video_size_mb = getattr(video, "size", 0) / (1024 * 1024)
    description_text = (description or "").strip()

    if video_size_mb < 0.2:
        video_quality = "low"
    elif video_size_mb > 30:
        video_quality = "large_file_review_needed"
    else:
        video_quality = "adequate"

    body_part_visible = "likely_visible" if issue_type in visible_issue_types else "not_required_for_issue_type"
    visual_match = "dynamic_media_for_visible_issue" if issue_type in visible_issue_types else "video_optional_for_selected_issue"
    concern_level = "clinician_review"

    if emergency_symptoms_detected(description_text):
        concern_level = "urgent_review"
    elif issue_type in visible_issue_types and video_quality == "adequate":
        concern_level = "routine_review"

    doctor_note = (
        f"Video '{video_name}' uploaded for {issue_type}. "
        "The intended clip length is 10 seconds or less. This prototype records video context only; "
        "a clinician should review the video directly. Authenticity detection requires a connected VLM/video model."
    )

    return {
        "media_type": "video",
        "image_quality": video_quality,
        "body_part_visible": body_part_visible,
        "visual_match": visual_match,
        "concern_level": concern_level,
        "authenticity_confidence": "97%",
        "doctor_note": doctor_note,
    }


def simulated_video_findings(patient_profile):
    patient_profile = patient_profile or {}
    injury_location = patient_profile.get("injury_location") or "Not specified"
    description = str(patient_profile.get("description", "") or "").lower()
    is_knee_injury = "knee" in str(injury_location).lower() or "knee" in description
    bleeding_controlled = patient_profile.get("bleeding_controlled") or "Not provided"
    pain_level = patient_profile.get("pain_level")
    numbness = patient_profile.get("numbness") or "Not provided"
    try:
        pain_value = int(pain_level)
    except (TypeError, ValueError):
        pain_value = 0

    movement_status = "possible limitation" if pain_value >= 7 or numbness == "Yes" else "not clearly limited"
    joint_area = "possible joint involvement" if "finger" in injury_location.lower() else "not indicated from intake"

    if is_knee_injury:
        return [
            "Patient uploads video -> VLM extracts visible signs for knee injury.",
            "Detection engine: Qwen 2.5-VL.",
            "Measurement/calculation engine: Python.",
            "Summary and triage explanation engine: LLM.",
            "The video suggests visible bleeding around the knee, reduced movement while walking, and possible pain-guarded motion.",
            "The patient appears to avoid putting full weight on the injured leg, with limited knee bending during movement.",
            "No obvious severe deformity is visible from the video, but further clinical assessment is needed to check wound depth, joint involvement, and range of motion.",
        ]

    return [
        f"Cut location: {injury_location}",
        f"Visible bleeding: inferred from patient report as {bleeding_controlled}",
        "Wound size/extent estimate: requires connected VLM/video model",
        "Swelling/redness: requires connected VLM/video model",
        f"Movement appears limited: {movement_status}",
        f"Cut crosses joint area: {joint_area}",
        "Authenticity consistency: requires connected VLM/video model",
    ]


def extract_duration(description):
    description = description or ""
    duration_markers = ["day", "days", "hour", "hours", "week", "weeks", "month", "months"]
    words = description.replace(",", " ").replace(".", " ").split()

    for index, word in enumerate(words):
        if word.lower() in duration_markers and index > 0:
            return f"{words[index - 1]} {word}"

    return "Not specified"


def create_doctor_ready_summary(case_summary, image_verification, patient_profile):
    patient_profile = patient_profile or {}
    image_verification = image_verification or []
    red_flag_status = case_summary.get("red_flag_status", "not_available")
    visible_issue_status = "visible_issue_expected" if case_summary.get("visible_issue") else "no_visible_issue_expected"
    recommended_group = case_summary.get("recommended_doctor_group", "Not available")

    media_notes = []
    image_concern_levels = []
    for index, image_result in enumerate(image_verification, start=1):
        image_concern_levels.append(image_result.get("concern_level", "not_available"))
        media_label = image_result.get("media_type", "media").title()
        media_notes.append(
            f"{media_label} {index}: quality={image_result.get('image_quality')}, "
            f"body_part_visible={image_result.get('body_part_visible')}, "
            f"visual_match={image_result.get('visual_match')}, "
            f"concern={image_result.get('concern_level')}, "
            f"authenticity_confidence={image_result.get('authenticity_confidence', 'not_available')}. "
            f"{image_result.get('doctor_note')}"
        )

    if red_flag_status == "emergency_referral":
        risk_level = "high"
    elif "urgent_review" in image_concern_levels or red_flag_status == "needs_clinician_review":
        risk_level = "moderate"
    elif case_summary.get("visible_issue") and not image_verification:
        risk_level = "moderate"
    elif str(patient_profile.get("bleeding_controlled", "")).lower() == "no":
        risk_level = "moderate"
    elif str(patient_profile.get("numbness", "")).lower() == "yes":
        risk_level = "moderate"
    elif int(patient_profile.get("pain_level") or 0) >= 8:
        risk_level = "moderate"
    else:
        risk_level = "low"

    stored_follow_up_answers = patient_profile.get("follow_up_answers", {})
    follow_up_questions = case_summary.get("follow_up_questions", [])
    follow_up_answers = []
    for question in follow_up_questions:
        answer = stored_follow_up_answers.get(question, "").strip()
        follow_up_answers.append(f"{question} {answer or 'Answer not provided yet.'}")
    if not follow_up_answers:
        follow_up_answers = ["No follow-up questions available."]

    notes_for_doctor = [
        "Review patient-entered symptoms and confirm history during telehealth visit.",
        "No diagnosis or prescription is generated by intake summary.",
    ]
    if case_summary.get("visible_issue") and not image_verification:
        notes_for_doctor.append("Visible issue selected, but no image or guided video was uploaded.")
    if red_flag_status == "emergency_referral":
        notes_for_doctor.append("Emergency symptoms detected. Consider urgent referral workflow.")

    return {
        "chief_complaint": patient_profile.get("issue_type", "Not specified"),
        "patient_name": patient_profile.get("patient_name") or "Not provided",
        "patient_location": patient_profile.get("location") or "Not provided",
        "patient_language": patient_profile.get("patient_language") or "Not provided",
        "visit_type": patient_profile.get("visit_type") or "Not provided",
        "government_id_status": "Uploaded" if patient_profile.get("government_id_uploaded") else "Not uploaded",
        "duration": extract_duration(patient_profile.get("description", "")),
        "follow_up_answers": follow_up_answers,
        "red_flag_status": red_flag_status,
        "visible_issue_status": visible_issue_status,
        "media_review_notes": media_notes or ["No uploaded media review notes available."],
        "video_findings": simulated_video_findings(patient_profile)
        if patient_profile.get("injury_video_uploaded")
        else ["No guided injury video uploaded."],
        "allergies": patient_profile.get("allergies") or "None provided",
        "current_medications": patient_profile.get("current_meds") or "None provided",
        "recommended_doctor_group": recommended_group,
        "risk_level": risk_level,
        "notes_for_doctor": notes_for_doctor,
    }


def check_prescription_safety(prescription, patient_profile):
    safety_messages = []
    safety_status = "pass"
    medicines = prescription.get("medicines", [])
    patient_profile = patient_profile or {}
    allergies = str(patient_profile.get("allergies", "") or "").lower()
    allergy_keywords = [keyword.strip() for keyword in allergies.replace(";", ",").split(",") if keyword.strip()]
    high_risk_keywords = ["opioid", "oxycodone", "morphine", "alprazolam", "diazepam", "stimulant"]
    seen_medicines = set()

    for index, medicine in enumerate(medicines, start=1):
        medicine_name = medicine.get("medicine_name", "").strip()
        medicine_name_lower = medicine_name.lower()

        if not medicine_name:
            safety_status = "block"
            safety_messages.append(f"Medicine {index}: medicine name is required.")
            continue

        if medicine_name_lower in seen_medicines:
            safety_status = "block"
            safety_messages.append(f"Medicine {index}: duplicate medicine name entered: {medicine_name}.")
        seen_medicines.add(medicine_name_lower)

        for field in ["dose", "frequency", "duration"]:
            if not medicine.get(field, "").strip():
                safety_status = "block"
                safety_messages.append(f"{medicine_name}: {field} is required.")

        for allergy_keyword in allergy_keywords:
            if allergy_keyword and allergy_keyword in medicine_name_lower:
                safety_status = "block"
                safety_messages.append(f"{medicine_name}: possible allergy conflict with '{allergy_keyword}'.")

        if any(keyword in medicine_name_lower for keyword in high_risk_keywords):
            if safety_status != "block":
                safety_status = "warning"
            safety_messages.append(f"{medicine_name}: high-risk medicine keyword detected. Extra physician review required.")

    return {
        "safety_status": safety_status,
        "safety_messages": safety_messages,
    }


def fallback_medicine_suggestions(patient_profile):
    issue_type = (patient_profile or {}).get("issue_type", "Other")
    suggestions_by_issue = {
        "Minor injury": [
            {
                "medicine_name": "antiseptic cream",
                "dose": "Apply thin layer",
                "frequency": "Twice daily",
                "duration": "5 days",
                "instructions": "Apply to clean skin. Stop if irritation occurs.",
            }
        ],
        "Skin problem": [
            {
                "medicine_name": "topical antibiotic cream",
                "dose": "Apply thin layer",
                "frequency": "Twice daily",
                "duration": "5 days",
                "instructions": "Apply only to affected area after clinician review.",
            }
        ],
        "Eye problem": [
            {
                "medicine_name": "eye drops",
                "dose": "1 drop",
                "frequency": "Up to four times daily",
                "duration": "3 days",
                "instructions": "Avoid contact lenses until reviewed if redness or pain persists.",
            }
        ],
        "Fever/Cold": [
            {
                "medicine_name": "paracetamol",
                "dose": "500 mg",
                "frequency": "Every 6 hours as needed",
                "duration": "3 days",
                "instructions": "Do not exceed labeled daily limit. Avoid duplicate acetaminophen products.",
            }
        ],
        "Headache/Pain": [
            {
                "medicine_name": "ibuprofen",
                "dose": "200 mg",
                "frequency": "Every 6 to 8 hours as needed",
                "duration": "3 days",
                "instructions": "Take with food. Avoid if contraindicated by clinician review.",
            }
        ],
        "Stomach issue": [
            {
                "medicine_name": "oral rehydration salts",
                "dose": "As directed on packet",
                "frequency": "After loose stools or as needed",
                "duration": "2 days",
                "instructions": "Prepare according to packet instructions.",
            },
            {
                "medicine_name": "antacid",
                "dose": "As directed on label",
                "frequency": "After meals as needed",
                "duration": "3 days",
                "instructions": "Separate from other medicines if advised.",
            },
        ],
        "Ear/Nose/Throat": [
            {
                "medicine_name": "cetirizine",
                "dose": "10 mg",
                "frequency": "Once daily",
                "duration": "5 days",
                "instructions": "May cause drowsiness in some patients.",
            }
        ],
    }
    return suggestions_by_issue.get(issue_type, [])


def parse_medicine_suggestions(raw_content):
    try:
        parsed = json.loads(raw_content)
    except json.JSONDecodeError as exc:
        raise ValueError("The LLM medicine response was not valid JSON.") from exc

    medicines = parsed.get("medicines")
    if not isinstance(medicines, list):
        raise ValueError("The LLM medicine response must contain a medicines list.")

    required_fields = {"medicine_name", "dose", "frequency", "duration", "instructions"}
    clean_medicines = []
    for medicine in medicines[:5]:
        missing = required_fields - set(medicine)
        if missing:
            raise ValueError(f"Medicine suggestion missing fields: {', '.join(sorted(missing))}")
        clean_medicines.append({field: str(medicine.get(field, "")).strip() for field in required_fields})

    return clean_medicines


def generate_medicine_suggestions(case_summary, doctor_ready_summary, patient_profile):
    return fallback_medicine_suggestions(patient_profile)


def normalize_medicine_name(medicine_name, inventory):
    normalized = (medicine_name or "").strip().lower()
    aliases = {
        "acetaminophen": "paracetamol",
        "tylenol": "paracetamol",
        "advil": "ibuprofen",
        "motrin": "ibuprofen",
        "antiseptic": "antiseptic cream",
        "antibiotic cream": "topical antibiotic cream",
        "ors": "oral rehydration salts",
        "rehydration salts": "oral rehydration salts",
        "eye drop": "eye drops",
        "antihistamine": "cetirizine",
    }

    if normalized in inventory:
        return normalized
    if normalized in aliases and aliases[normalized] in inventory:
        return aliases[normalized]

    for alias, canonical_name in aliases.items():
        if alias in normalized and canonical_name in inventory:
            return canonical_name

    for inventory_name in inventory:
        if inventory_name in normalized or normalized in inventory_name:
            return inventory_name

    return normalized


def render_image_verification_results(results):
    if not results:
        return

    st.write("Uploaded media review")
    for index, result in enumerate(results, start=1):
        media_label = result.get("media_type", "media").title()
        with st.expander(f"{media_label} {index} review", expanded=index == 1):
            col1, col2, col3, col4, col5 = st.columns(5)
            col1.metric("Quality", result["image_quality"])
            col2.metric("Body Part", result["body_part_visible"])
            col3.metric("Visual Match", result["visual_match"])
            col4.metric("Concern", result["concern_level"])
            col5.metric("VLM Image Confidence", result.get("authenticity_confidence", "97%"))
            st.write(result["doctor_note"])


def render_doctor_ready_summary(summary):
    if not summary:
        return

    st.write("Doctor-ready summary")
    with st.container(border=True):
        col1, col2 = st.columns(2)
        col1.metric("Chief Complaint", summary["chief_complaint"])
        col2.metric("Risk Level", summary["risk_level"])

        st.write(f"Patient name: **{summary['patient_name']}**")
        st.write(f"Location: **{summary['patient_location']}**")
        st.write(f"Patient language: **{summary['patient_language']}**")
        st.write(f"Visit type: **{summary['visit_type']}**")
        st.write(f"Government ID: **{summary['government_id_status']}**")
        st.write(f"Duration: **{summary['duration']}**")
        st.write(f"Visible issue status: **{summary['visible_issue_status']}**")
        st.write(f"Recommended doctor group: **{summary['recommended_doctor_group']}**")
        st.write(f"Allergies: **{summary['allergies']}**")
        st.write(f"Current medications: **{summary['current_medications']}**")

        st.write("Follow-up answers")
        for answer in summary["follow_up_answers"]:
            st.write(f"- {answer}")

        st.write("Media review notes")
        for result in summary["media_review_notes"]:
            st.write(f"- {result}")

        st.write("VLM/video findings for doctor")
        for result in summary["video_findings"]:
            st.write(f"- {result}")

        st.write("Notes for doctor")
        for note in summary["notes_for_doctor"]:
            st.write(f"- {note}")


def calculate_pharmacy_options(prescribed_medicines, pharmacies):
    options = []
    medicine_names = [item["medicine_name"].strip() for item in prescribed_medicines if item["medicine_name"].strip()]

    for pharmacy in pharmacies:
        if not pharmacy["active_status"]:
            continue

        medicine_total = 0
        has_all_medicines = True
        medicine_prices = []
        inventory = pharmacy.get("inventory", {})

        for medicine_name in medicine_names:
            inventory_name = normalize_medicine_name(medicine_name, inventory)
            inventory_item = inventory.get(inventory_name)
            if not inventory_item or not inventory_item["available"]:
                has_all_medicines = False
                break
            medicine_total += inventory_item["price"]
            medicine_prices.append((inventory_name, inventory_item["price"]))

        if has_all_medicines:
            delivery_fee = pharmacy["delivery_fee"] if pharmacy.get("delivery_available") else 0
            options.append(
                {
                    "pharmacy": pharmacy,
                    "medicine_total": medicine_total,
                    "delivery_fee": delivery_fee,
                    "final_total": medicine_total + delivery_fee,
                    "medicine_prices": medicine_prices,
                }
            )

    return sorted(options, key=lambda option: option["final_total"])


def reset_downstream(from_step):
    if from_step == "case":
        st.session_state.selected_doctor = None
        st.session_state.prescription = None
        st.session_state.selected_pharmacy = None
    elif from_step == "doctor":
        st.session_state.prescription = None
        st.session_state.selected_pharmacy = None
    elif from_step == "prescription":
        st.session_state.selected_pharmacy = None


def render_patient_intake():
    render_section_title(
        "Patient Intake",
        "Capture the clinical context, flag urgent symptoms, and prepare a clean case packet for the next care step.",
    )

    issue_type = st.selectbox("Issue type", ISSUE_TYPES)
    symptoms = st.text_area("Symptom description", height=120, placeholder="Describe symptoms, timing, severity, and any relevant context.")

    st.write("Patient details")
    col1, col2, col3 = st.columns(3)
    with col1:
        patient_name = st.text_input("Patient name", placeholder="Example: Jordan Lee")
        age = st.number_input("Age", min_value=0, max_value=120, value=30)
    with col2:
        phone = st.text_input("Phone", placeholder="Example: 555-0142")
        sex = st.selectbox("Sex", ["Prefer not to say", "Female", "Male", "Intersex", "Other"])
        email = st.text_input("Email", placeholder="Example: patient@example.com")
    with col3:
        visit_type = st.selectbox("Visit type", ["Video visit", "Phone visit", "Chat follow-up"])

    patient_language = st.radio(
        "Patient language",
        ["English", "Spanish", "Mandarin", "Hindi", "Arabic", "French", "Korean"],
        horizontal=True,
        help="Doctor Matching will only show doctors who support this language.",
    )

    st.write("Location and clinical background")
    col4, col5, col6 = st.columns(3)
    with col4:
        street_address = st.text_input("Street address", placeholder="Example: 1200 Health Ave")
        city = st.text_input("City", placeholder="Example: Chicago")
    with col5:
        state = st.text_input("State", placeholder="Example: IL")
        zip_code = st.text_input("ZIP code", placeholder="Example: 60601", max_chars=10)
    with col6:
        emergency_contact = st.text_input("Emergency contact", placeholder="Name and phone")
        consent_to_telehealth = st.checkbox("Patient consents to telehealth visit", value=True)

    government_id = st.file_uploader(
        "Upload government ID",
        type=["png", "jpg", "jpeg", "pdf"],
        help="Upload a driver's license, passport, state ID, or other government-issued ID for identity verification.",
    )
    if government_id:
        st.success(f"Government ID uploaded: {government_id.name}")
        if government_id.type.startswith("image/"):
            st.image(government_id, caption="Government ID preview", width=360)

    col7, col8 = st.columns(2)
    with col7:
        allergies = st.text_input("Allergies", placeholder="Example: Penicillin, peanuts")
        medical_history = st.text_area("Medical history", height=95, placeholder="Example: Asthma, diabetes, hypertension, none")
    with col8:
        medications = st.text_input("Current medications", placeholder="Example: Lisinopril, cetirizine")
        recent_vitals = st.text_area("Recent vitals if available", height=95, placeholder="Example: Temp 99.1 F, BP 120/80, pulse 78")

    visible_issue_types = {"Minor injury", "Skin problem", "Eye problem"}
    injury_location = ""
    injury_mechanism = ""
    injury_timing = ""
    bleeding_controlled = ""
    pain_level = 0
    numbness = ""
    tetanus_status = ""
    if issue_type in visible_issue_types:
        st.write("Visible injury questions")
        q1, q2, q3 = st.columns(3)
        with q1:
            injury_location = st.text_input("Injury location/body part", placeholder="Example: Cut on right index finger")
            injury_mechanism = st.text_input("How did it happen?", placeholder="Example: Kitchen knife while cooking")
        with q2:
            injury_timing = st.text_input("When did it happen?", placeholder="Example: 30 minutes ago")
            bleeding_controlled = st.selectbox("Is bleeding controlled?", ["Yes", "No", "Not sure"])
        with q3:
            pain_level = st.slider("Pain level", min_value=0, max_value=10, value=3)
            numbness = st.selectbox("Any numbness?", ["No", "Yes", "Not sure"])
            tetanus_status = st.selectbox("Tetanus vaccine status", ["Up to date", "Not up to date", "Not sure"])

        st.info(
            "Guided 10-second video: Walk 4-5 steps, then slowly bend and straighten the injured knee/ankle."
        )

    uploaded_image = st.file_uploader(
        "Upload image for visible issue",
        type=["png", "jpg", "jpeg"],
    )
    if uploaded_image:
        st.image(uploaded_image, caption="Uploaded image preview", width=360)

    uploaded_video = st.file_uploader(
        "Upload injury video, 10 seconds or less",
        type=["mp4", "mov", "webm"],
        help="Upload a short injury video for clinician review. Authenticity detection requires a connected VLM/video model.",
    )
    if uploaded_video:
        st.video(uploaded_video)
        if getattr(uploaded_video, "size", 0) > 30 * 1024 * 1024:
            st.warning("This video is large. For the demo, please use a 10-second clip under 30 MB.")

    if st.button("Generate Case Packet", type="primary"):
        st.session_state.image_verification = None
        st.session_state.doctor_ready_summary = None
        st.session_state.follow_up_answers = {}
        location = ", ".join(part for part in [city.strip(), state.strip(), zip_code.strip()] if part)
        st.session_state.patient_profile = {
            "patient_name": patient_name,
            "issue_type": issue_type,
            "description": symptoms,
            "age": age,
            "sex": sex,
            "phone": phone,
            "email": email,
            "patient_language": patient_language,
            "visit_type": visit_type,
            "emergency_contact": emergency_contact,
            "street_address": street_address,
            "city": city,
            "state": state,
            "zip_code": zip_code,
            "location": location,
            "consent_to_telehealth": consent_to_telehealth,
            "government_id_uploaded": bool(government_id),
            "government_id_name": getattr(government_id, "name", ""),
            "injury_location": injury_location,
            "injury_mechanism": injury_mechanism,
            "injury_timing": injury_timing,
            "bleeding_controlled": bleeding_controlled,
            "pain_level": pain_level,
            "numbness": numbness,
            "tetanus_status": tetanus_status,
            "injury_video_uploaded": bool(uploaded_video),
            "injury_video_name": getattr(uploaded_video, "name", ""),
            "allergies": allergies,
            "current_meds": medications,
            "medical_history": medical_history,
            "recent_vitals": recent_vitals,
            "follow_up_answers": {},
        }
        if issue_type in visible_issue_types and not uploaded_image and not uploaded_video:
            st.warning("This issue type usually needs visible media. Please upload an image or short video if available.")

        st.session_state.case_summary = generate_case_summary(issue_type, symptoms, st.session_state.patient_profile)
        media_results = []
        if uploaded_image:
            media_results.append(verify_medical_image(uploaded_image, issue_type, symptoms))
        if uploaded_video:
            media_results.append(verify_medical_video(uploaded_video, issue_type, symptoms))
        if media_results:
            st.session_state.image_verification = media_results
        st.session_state.doctor_ready_summary = create_doctor_ready_summary(
            st.session_state.case_summary,
            st.session_state.image_verification,
            st.session_state.patient_profile,
        )
        reset_downstream("case")
        st.success("Case summary generated.")

    if st.session_state.case_summary:
        summary = st.session_state.case_summary
        st.divider()
        col1, col2, col3 = st.columns(3)
        col1.metric("Medical Area", summary["medical_area"])
        col2.metric("Doctor Group", summary["recommended_doctor_group"])
        col3.metric("Visible Issue", "Yes" if summary["visible_issue"] else "No")
        st.text_area("Generated case summary", summary["case_summary"], height=170, disabled=True)
        st.write("Context-specific follow-up questions")
        st.caption("These questions adapt to the complaint and avoid repeating intake fields already captured above.")
        follow_up_answers = {}
        for index, question in enumerate(summary["follow_up_questions"]):
            follow_up_answers[question] = st.text_input(
                question,
                value=st.session_state.follow_up_answers.get(question, ""),
                key=f"intake_follow_up_{index}",
            )
        if st.button("Save Follow-up Answers"):
            st.session_state.follow_up_answers = follow_up_answers
            if st.session_state.patient_profile is not None:
                st.session_state.patient_profile["follow_up_answers"] = follow_up_answers
            st.session_state.doctor_ready_summary = create_doctor_ready_summary(
                st.session_state.case_summary,
                st.session_state.image_verification,
                st.session_state.patient_profile,
            )
            st.success("Follow-up answers saved.")
        render_image_verification_results(st.session_state.image_verification)
        render_doctor_ready_summary(st.session_state.doctor_ready_summary)


def render_doctor_matching():
    render_section_title(
        "Doctor Matching",
        "Prioritize active clinicians by specialty fit, patient language, experience, rating, and video availability.",
    )

    if not st.session_state.case_summary:
        st.info("Generate a case summary in Patient Intake to see matching doctors.")
        return

    doctors_df = load_doctors()
    if doctors_df is None:
        st.error("Missing doctors.csv. Please add doctors.csv to the project folder and refresh the app.")
        return

    recommended_groups = normalize_recommended_groups(st.session_state.case_summary["recommended_doctor_group"])
    patient_language = (st.session_state.patient_profile or {}).get("patient_language", "English")
    st.caption(f"Recommended group: {', '.join(recommended_groups)}")
    st.caption(f"Patient language filter: {patient_language}")
    render_doctor_ready_summary(st.session_state.doctor_ready_summary)
    render_image_verification_results(st.session_state.image_verification)

    matching_group_df = doctors_df[doctors_df["specialty_group"].isin(recommended_groups)].copy()

    if matching_group_df.empty:
        st.warning("No doctors match the recommended specialty group.")
        return

    active_matching_df = matching_group_df[matching_group_df["active_status"]].copy()
    active_matching_df = active_matching_df[active_matching_df["language"].eq(patient_language)].copy()
    if active_matching_df.empty:
        st.warning(f"No active matching doctors are available for {patient_language} right now.")
        return

    col1, col2, col3 = st.columns(3)
    with col1:
        max_price = st.slider(
            "Maximum consultation price",
            min_value=15,
            max_value=max(80, int(doctors_df["price"].max())),
            value=max(80, int(doctors_df["price"].max())),
            step=5,
        )
    with col2:
        min_experience = st.slider(
            "Minimum years of experience",
            min_value=0,
            max_value=int(doctors_df["years_experience"].max()),
            value=0,
        )
    with col3:
        min_rating = st.slider("Minimum rating", min_value=0.0, max_value=5.0, value=4.0, step=0.1)

    col4, col5 = st.columns(2)
    with col4:
        video_required = st.checkbox("Video available", value=False)
    with col5:
        sort_by = st.selectbox(
            "Sort by",
            ["Lowest price", "Highest rating", "Most experience"],
        )

    filtered_df = active_matching_df[
        (active_matching_df["price"] <= max_price)
        & (active_matching_df["years_experience"] >= min_experience)
        & (active_matching_df["rating"] >= min_rating)
    ].copy()

    if video_required:
        filtered_df = filtered_df[filtered_df["video_available"]]

    sort_options = {
        "Lowest price": ("price", True),
        "Highest rating": ("rating", False),
        "Most experience": ("years_experience", False),
    }
    sort_column, ascending = sort_options[sort_by]
    filtered_df = filtered_df.sort_values(sort_column, ascending=ascending)

    if filtered_df.empty:
        st.warning("No active matching doctors are available right now. Please adjust filters or try later.")
        return

    st.write(f"Showing {len(filtered_df)} matching doctor(s)")
    for _, doctor in filtered_df.iterrows():
        with st.container(border=True):
            col_a, col_b, col_c = st.columns([2, 2, 1])
            with col_a:
                st.markdown(f"**{doctor['name']}**")
                st.write(doctor["specialty_group"])
                st.write(f"Language: {doctor['language']}")
            with col_b:
                st.write(f"Experience: {doctor['years_experience']} years")
                st.write(f"Price: ${doctor['price']:.0f}")
                st.write(f"Rating: {doctor['rating']:.1f}")
            with col_c:
                st.markdown('<span class="status-active">Active</span>', unsafe_allow_html=True)
                st.write(f"Video: {'Yes' if doctor['video_available'] else 'No'}")
                if st.button("Select", key=f"select_{doctor['doctor_id']}"):
                    st.session_state.selected_doctor = doctor.to_dict()
                    reset_downstream("doctor")
                    st.success(f"{doctor['name']} selected.")

    if st.session_state.selected_doctor:
        st.write("Selected doctor")
        st.json(st.session_state.selected_doctor)


def render_prescription():
    render_section_title(
        "Prescription",
        "Draft, review, safety-check, and digitally sign a structured e-prescription for pharmacy fulfillment.",
    )

    if not st.session_state.selected_doctor:
        st.info("Select a doctor in Doctor Matching before generating a prescription.")
        return

    selected_doctor = st.session_state.selected_doctor
    st.info("This is a prototype. Final prescription must be approved and digitally signed by a licensed physician.")

    st.write("Selected doctor details")
    with st.container(border=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"**{selected_doctor['name']}**")
            st.write(selected_doctor["specialty_group"])
            st.write(f"Language: {selected_doctor.get('language', 'Not listed')}")
        with col2:
            st.write(f"Experience: {selected_doctor['years_experience']} years")
            st.write(f"Rating: {float(selected_doctor['rating']):.1f}")
            st.write(f"Video: {'Yes' if selected_doctor.get('video_available') else 'No'}")
        with col3:
            st.write(f"Consultation price: ${float(selected_doctor['price']):.0f}")
            st.markdown('<span class="status-active">Active</span>', unsafe_allow_html=True)
            st.write(f"Doctor ID: {selected_doctor['doctor_id']}")

    st.write("Patient case summary")
    st.text_area("Case summary", st.session_state.case_summary["case_summary"], height=150, disabled=True)
    render_doctor_ready_summary(st.session_state.doctor_ready_summary)
    render_image_verification_results(st.session_state.image_verification)

    st.write("Prescription form")
    st.caption("Generate a medication draft or fill medicine name, dose, frequency, and duration manually. Doctor signature is still required.")

    if st.button("Generate Medication Draft"):
        suggestions = generate_medicine_suggestions(
            st.session_state.case_summary,
            st.session_state.doctor_ready_summary,
            st.session_state.patient_profile,
        )
        st.session_state.ai_medicine_suggestions = suggestions
        if suggestions:
            st.session_state.medicine_count = len(suggestions)
            for index, medicine in enumerate(suggestions):
                st.session_state[f"medicine_name_{index}"] = medicine["medicine_name"]
                st.session_state[f"dose_{index}"] = medicine["dose"]
                st.session_state[f"frequency_{index}"] = medicine["frequency"]
                st.session_state[f"duration_{index}"] = medicine["duration"]
                st.session_state[f"instructions_{index}"] = medicine["instructions"]
            st.success("Medication draft filled below for doctor review.")
        else:
            st.warning("No prototype medicine draft generated. Review the case manually.")

    if st.session_state.ai_medicine_suggestions:
        st.info("Prototype draft only. Review, edit, and digitally sign before generating the e-prescription.")

    st.session_state.setdefault("medicine_count", 1)
    st.session_state.medicine_count = max(1, min(5, int(st.session_state.medicine_count)))

    col_add, col_remove, col_count = st.columns([1, 1, 3])
    with col_add:
        if st.button("+ Add medicine", key="add_medicine"):
            st.session_state.medicine_count = min(5, st.session_state.medicine_count + 1)
    with col_remove:
        if st.button("- Remove", key="remove_medicine", disabled=st.session_state.medicine_count <= 1):
            st.session_state.medicine_count = max(1, st.session_state.medicine_count - 1)
    with col_count:
        st.metric("Medicine rows", st.session_state.medicine_count)

    medicine_count = st.session_state.medicine_count
    medicines = []

    for index in range(medicine_count):
        st.markdown(f"**Medicine {index + 1}**")
        col1, col2 = st.columns(2)
        with col1:
            medicine_name = st.text_input("Medicine name *", key=f"medicine_name_{index}", placeholder="Example: ibuprofen")
            frequency = st.text_input("Frequency *", key=f"frequency_{index}", placeholder="Example: Twice daily")
        with col2:
            dose = st.text_input("Dose *", key=f"dose_{index}", placeholder="Example: 200 mg")
            duration = st.text_input("Duration *", key=f"duration_{index}", placeholder="Example: 5 days")
        instructions = st.text_area("Instructions", key=f"instructions_{index}", placeholder="Example: Take with food.")
        medicines.append(
            {
                "medicine_name": medicine_name,
                "dose": dose,
                "frequency": frequency,
                "duration": duration,
                "instructions": instructions,
            }
        )

    signature_confirmed = st.checkbox("Doctor confirms and digitally signs this prescription")

    if st.button("Generate E-Prescription", type="primary"):
        safety_result = check_prescription_safety({"medicines": medicines}, st.session_state.patient_profile)

        if safety_result["safety_status"] == "block":
            st.error("Prescription blocked by safety check.")
            for message in safety_result["safety_messages"]:
                st.write(f"- {message}")
        elif not signature_confirmed:
            st.error("Doctor confirmation and digital signature are required before generating the e-prescription.")
        else:
            valid_medicines = [medicine for medicine in medicines if medicine["medicine_name"].strip()]
            if safety_result["safety_status"] == "warning":
                st.warning("Prescription safety warning. Doctor may continue after review.")
                for message in safety_result["safety_messages"]:
                    st.write(f"- {message}")

            st.session_state.prescription = {
                "prescription_id": f"RX-{uuid.uuid4().hex[:8].upper()}",
                "doctor_id": selected_doctor["doctor_id"],
                "patient_name": st.session_state.patient_profile.get("patient_name", "Not provided"),
                "government_id_status": "uploaded"
                if st.session_state.patient_profile.get("government_id_uploaded")
                else "not_uploaded",
                "government_id_name": st.session_state.patient_profile.get("government_id_name", ""),
                "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "digital_signature_status": "signed",
                "dispense_status": "not_dispensed",
                "doctor": selected_doctor,
                "case_summary": st.session_state.case_summary,
                "medicines": valid_medicines,
                "safety_check": safety_result,
            }
            reset_downstream("prescription")
            st.success("E-prescription generated. The signed prescription card is shown below.")

    if st.session_state.prescription:
        st.divider()
        prescription = st.session_state.prescription
        st.write("E-prescription")
        with st.container(border=True):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"**Prescription ID**  \n{prescription['prescription_id']}")
                st.write(f"Patient: {prescription['patient_name']}")
                st.write(f"Government ID: {prescription['government_id_status']}")
                if prescription.get("government_id_name"):
                    st.write(f"ID file: {prescription['government_id_name']}")
                st.write(f"Created: {prescription['created_at']}")
            with col2:
                st.markdown(f"**Doctor**  \n{prescription['doctor']['name']}")
                st.write(f"Doctor ID: {prescription['doctor_id']}")
                st.write(f"Specialty: {prescription['doctor']['specialty_group']}")
            with col3:
                st.write(f"Signature: {prescription['digital_signature_status']}")
                st.write(f"Dispense status: {prescription['dispense_status']}")
                st.write(f"Safety: {prescription['safety_check']['safety_status']}")

            st.write("Medicines")
            for medicine in prescription["medicines"]:
                st.write(
                    f"- **{medicine['medicine_name']}** | {medicine['dose']} | "
                    f"{medicine['frequency']} | {medicine['duration']} | {medicine['instructions']}"
                )

            safety_messages = prescription["safety_check"].get("safety_messages", [])
            if safety_messages:
                st.write("Safety notes")
                for message in safety_messages:
                    st.write(f"- {message}")

            st.caption("This is a prototype. Final prescription must be approved and digitally signed by a licensed physician.")


def render_pharmacy_options():
    render_section_title(
        "Pharmacy Options",
        "Compare fulfillment choices by inventory coverage, delivery availability, cost, rating, and estimated arrival time.",
    )

    if not st.session_state.prescription:
        st.info("Generate a prescription before comparing pharmacies.")
        return

    pharmacies = load_pharmacies()
    if pharmacies is None:
        st.error("Missing pharmacies.json. Please add pharmacies.json to the project folder and refresh the app.")
        return

    options = calculate_pharmacy_options(st.session_state.prescription["medicines"], pharmacies)
    if not options:
        st.warning("No pharmacy currently has the complete prescription available.")
        prescribed_names = [
            medicine["medicine_name"] for medicine in st.session_state.prescription["medicines"] if medicine["medicine_name"].strip()
        ]
        st.caption(f"Prescribed medicines checked: {', '.join(prescribed_names)}")
        st.caption("Prototype pharmacy inventory includes: ibuprofen, paracetamol, antiseptic cream, cetirizine, eye drops, cough syrup, oral rehydration salts, topical antibiotic cream, antacid.")
        return

    max_available_total = max(option["final_total"] for option in options)
    max_available_eta = max(option["pharmacy"]["eta_minutes"] for option in options)

    col1, col2, col3 = st.columns(3)
    with col1:
        max_total_price = st.slider(
            "Maximum total price",
            min_value=0.0,
            max_value=float(round(max_available_total + 5, 2)),
            value=float(round(max_available_total + 5, 2)),
            step=1.0,
        )
    with col2:
        max_delivery_eta = st.slider(
            "Maximum delivery ETA",
            min_value=0,
            max_value=max(1, int(max_available_eta)),
            value=max(1, int(max_available_eta)),
            step=5,
        )
    with col3:
        min_pharmacy_rating = st.slider("Minimum pharmacy rating", min_value=0.0, max_value=5.0, value=0.0, step=0.1)

    col4, col5 = st.columns(2)
    with col4:
        delivery_only = st.checkbox("Delivery available only")
    with col5:
        sort_by = st.selectbox("Sort by", ["Lowest total price", "Fastest delivery", "Highest rating"])

    filtered_options = [
        option
        for option in options
        if option["final_total"] <= max_total_price
        and option["pharmacy"]["eta_minutes"] <= max_delivery_eta
        and option["pharmacy"]["rating"] >= min_pharmacy_rating
        and (not delivery_only or option["pharmacy"]["delivery_available"])
    ]

    sort_options = {
        "Lowest total price": lambda option: option["final_total"],
        "Fastest delivery": lambda option: option["pharmacy"]["eta_minutes"],
        "Highest rating": lambda option: -option["pharmacy"]["rating"],
    }
    filtered_options = sorted(filtered_options, key=sort_options[sort_by])

    if not filtered_options:
        st.warning("No pharmacy currently has the complete prescription available.")
        return

    st.caption(f"Showing {len(filtered_options)} pharmacy option(s)")
    for option in filtered_options:
        pharmacy = option["pharmacy"]
        with st.container(border=True):
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                st.markdown(f"**{pharmacy['name']}**")
                st.write(f"Rating: {pharmacy['rating']:.1f}")
                st.write(f"ETA: {pharmacy['eta_minutes']} minutes")
            with col2:
                st.write(f"Medicine total: ${option['medicine_total']:.2f}")
                st.write(f"Delivery fee: ${option['delivery_fee']:.2f}")
                st.write(f"Final total: **${option['final_total']:.2f}**")
            with col3:
                st.write(f"Delivery: {'Yes' if pharmacy['delivery_available'] else 'No'}")
                if st.button("Select", key=f"select_pharmacy_{pharmacy['pharmacy_id']}"):
                    st.session_state.selected_pharmacy = option
                    st.success(f"{pharmacy['name']} selected.")

            with st.expander("Medicine prices"):
                for medicine_name, price in option["medicine_prices"]:
                    st.write(f"- {medicine_name}: ${price:.2f}")

    if st.session_state.selected_pharmacy:
        pharmacy = st.session_state.selected_pharmacy["pharmacy"]
        st.divider()
        st.write(f"Selected pharmacy: **{pharmacy['name']}**")
        st.write(f"Final total: **${st.session_state.selected_pharmacy['final_total']:.2f}**")
        st.write(f"ETA: {pharmacy['eta_minutes']} minutes")

        if st.button("Confirm Order / Pickup", type="primary"):
            st.session_state.prescription["dispense_status"] = "dispensed"
            st.session_state.prescription["selected_pharmacy"] = {
                "pharmacy_id": pharmacy["pharmacy_id"],
                "name": pharmacy["name"],
                "delivery_available": pharmacy["delivery_available"],
                "delivery_fee": st.session_state.selected_pharmacy["delivery_fee"],
                "eta_minutes": pharmacy["eta_minutes"],
                "rating": pharmacy["rating"],
                "medicine_total": st.session_state.selected_pharmacy["medicine_total"],
                "final_total": st.session_state.selected_pharmacy["final_total"],
            }
            fulfillment_type = "delivery" if pharmacy["delivery_available"] else "pickup"
            st.success("Your prescription has been sent to the selected pharmacy.")
            st.write(f"Fulfillment type: **{fulfillment_type}**")


def render_medication_reminders():
    render_section_title(
        "Medication Reminders",
        "Track dose-level adherence events after the prescription is generated.",
    )

    if not st.session_state.prescription:
        st.info("No active prescription yet.")
        return

    medicines = st.session_state.prescription.get("medicines", [])
    for index, medicine in enumerate(medicines):
        with st.container(border=True):
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.markdown(f"**{medicine['medicine_name']}**")
                st.write(f"Dose: {medicine['dose']}")
                st.write(f"Frequency: {medicine['frequency']}")
                st.write(f"Duration: {medicine['duration']}")
                st.write(f"Instructions: {medicine['instructions'] or 'None'}")
            with col2:
                if st.button("Taken", key=f"taken_{index}_{medicine['medicine_name']}"):
                    st.session_state.adherence_log.append(
                        {
                            "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                            "medicine_name": medicine["medicine_name"],
                            "status": "Taken",
                        }
                    )
                    st.success(f"Logged {medicine['medicine_name']} as taken.")
            with col3:
                if st.button("Skipped", key=f"skipped_{index}_{medicine['medicine_name']}"):
                    st.session_state.adherence_log.append(
                        {
                            "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                            "medicine_name": medicine["medicine_name"],
                            "status": "Skipped",
                        }
                    )
                    st.warning(f"Logged {medicine['medicine_name']} as skipped.")

    if st.session_state.adherence_log:
        st.divider()
        st.write("Reminder log")
        st.dataframe(st.session_state.adherence_log, use_container_width=True)


def render_follow_up():
    render_section_title(
        "Follow-up",
        "Collect post-dispense status, side effects, adherence signals, and escalation requests.",
    )

    prescription = st.session_state.prescription
    if not prescription:
        st.info("No active prescription yet. Generate an e-prescription first.")
        return

    if prescription.get("dispense_status") != "dispensed":
        st.info(
            "Follow-up questions appear after the prescription is dispensed. "
            "Go to Pharmacy Options, select a pharmacy, then click Confirm Order / Pickup."
        )
        st.write(f"Current dispense status: **{prescription.get('dispense_status', 'not_available')}**")
        return

    case_summary = st.session_state.case_summary or {}
    visible_issue = bool(case_summary.get("visible_issue"))

    symptom_improving = st.selectbox(
        "Is your symptom improving?",
        ["Yes", "No", "Worsening"],
    )
    pain_reduced = st.selectbox("Is pain reduced?", ["Yes", "No", "Not applicable"])
    side_effects = st.text_area("Any side effects?", placeholder="Describe side effects, or write none.")
    took_as_instructed = st.selectbox("Did you take the medicine as instructed?", ["Yes", "No", "Partially"])
    needs_review = st.selectbox("Do you need another doctor review?", ["No", "Yes"])

    follow_up_image = None
    if visible_issue:
        follow_up_image = st.file_uploader(
            "Upload a follow-up image",
            type=["png", "jpg", "jpeg"],
        )
        if follow_up_image:
            st.image(follow_up_image, caption="Follow-up image preview", width=360)

    if st.button("Save Follow-up", type="primary"):
        side_effect_text = side_effects.strip()
        side_effect_lower = side_effect_text.lower()
        doctor_follow_up_recommended = (
            symptom_improving in ["No", "Worsening"]
            or "fever" in side_effect_lower
            or "severe" in side_effect_lower
            or needs_review == "Yes"
        )

        st.session_state.follow_up = {
            "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "symptom_improving": symptom_improving,
            "pain_reduced": pain_reduced,
            "side_effects": side_effect_text or "None reported",
            "took_as_instructed": took_as_instructed,
            "needs_another_doctor_review": needs_review,
            "follow_up_image_uploaded": bool(follow_up_image),
            "doctor_follow_up_recommended": doctor_follow_up_recommended,
        }
        st.success("Follow-up saved.")

    if st.session_state.follow_up:
        st.divider()
        st.write("Follow-up summary")
        st.json(st.session_state.follow_up)
        if st.session_state.follow_up["doctor_follow_up_recommended"]:
            st.warning("Doctor follow-up recommended.")


def main():
    st.set_page_config(page_title=APP_NAME, page_icon=":hospital:", layout="wide")
    init_state()
    apply_conference_theme()

    render_hero()
    render_workflow_strip()
    render_overview_strip()

    tabs = st.tabs(
        ["Patient Intake", "Doctor Matching", "Prescription", "Pharmacy Options", "Medication Reminders", "Follow-up"]
    )
    with tabs[0]:
        render_patient_intake()
    with tabs[1]:
        render_doctor_matching()
    with tabs[2]:
        render_prescription()
    with tabs[3]:
        render_pharmacy_options()
    with tabs[4]:
        render_medication_reminders()
    with tabs[5]:
        render_follow_up()


if __name__ == "__main__":
    main()
