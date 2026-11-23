"""
Machine Learning Classifier for CareerScan using Scikit-Learn TF-IDF & Logistic Regression.
Trains on verified dataset of fraudulent vs legitimate recruitment text.
"""

import os
import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sample_data.dataset import TRAINING_DATA

MODEL_CACHE_FILE = os.path.join(os.path.dirname(__file__), "scam_classifier_model.joblib")

_pipeline = None


def train_or_load_model():
    """
    Loads cached ML model or trains a new one using the curated corpus.
    """
    global _pipeline
    if _pipeline is not None:
        return _pipeline

    if os.path.exists(MODEL_CACHE_FILE):
        try:
            _pipeline = joblib.load(MODEL_CACHE_FILE)
            return _pipeline
        except Exception:
            pass

    # Train model
    texts = [item[0] for item in TRAINING_DATA]
    labels = [item[1] for item in TRAINING_DATA]

    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(
            ngram_range=(1, 2),
            stop_words="english",
            max_df=0.95,
            min_df=1,
            sublinear_tf=True
        )),
        ("classifier", LogisticRegression(
            C=2.5,
            class_weight="balanced",
            random_state=42,
            max_iter=300
        ))
    ])

    pipeline.fit(texts, labels)

    try:
        joblib.dump(pipeline, MODEL_CACHE_FILE)
    except Exception:
        pass

    _pipeline = pipeline
    return _pipeline


def predict_scam_probability(text):
    """
    Predicts probability of text being a recruitment scam (0.0 - 100.0%).
    Also extracts influential n-gram keywords present in text.
    """
    model = train_or_load_model()
    if not text or not text.strip():
        return {
            "probability": 0.0,
            "prediction": 0,
            "top_scam_keywords": []
        }

    proba = model.predict_proba([text])[0]
    scam_prob = float(proba[1]) * 100.0  # Class 1 is Scam

    # Extract top influential keywords/features found in the input text
    top_keywords = []
    try:
        tfidf = model.named_steps["tfidf"]
        clf = model.named_steps["classifier"]
        feature_names = np.array(tfidf.get_feature_names_out())
        coefs = clf.coef_[0]

        # Transform single document
        tfidf_vec = tfidf.transform([text]).toarray()[0]
        nonzero_indices = np.where(tfidf_vec > 0)[0]

        if len(nonzero_indices) > 0:
            # Score each active feature by (tfidf_weight * coefficient)
            feature_scores = []
            for idx in nonzero_indices:
                score = tfidf_vec[idx] * coefs[idx]
                if score > 0:  # Positive weights contribute to scam classification
                    feature_scores.append((feature_names[idx], float(score)))

            feature_scores.sort(key=lambda x: x[1], reverse=True)
            top_keywords = [item[0] for item in feature_scores[:6]]
    except Exception:
        top_keywords = []

    return {
        "probability": round(scam_prob, 1),
        "prediction": int(scam_prob >= 50.0),
        "top_scam_keywords": top_keywords
    }
