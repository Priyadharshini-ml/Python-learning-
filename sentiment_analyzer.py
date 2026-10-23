
"""Sentiment Analyzer: a beginner NLP ML project."""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report


REVIEWS = [
    "I love this product",
    "Excellent quality and amazing service",
    "Very happy with my purchase",
    "The experience was wonderful",
    "This works perfectly",
    "I highly recommend this service",
    "The product is fantastic",
    "Great value for money",
    "I am very satisfied",
    "Amazing experience overall",
    "I hate this product",
    "Terrible quality and poor service",
    "Very disappointed with my purchase",
    "The experience was awful",
    "This does not work properly",
    "I would not recommend this",
    "The product is horrible",
    "A complete waste of money",
    "I am very dissatisfied",
    "Extremely bad experience",
]

LABELS = [
    "positive", "positive", "positive", "positive",
    "positive", "positive", "positive", "positive",
    "positive", "positive",
    "negative", "negative", "negative", "negative",
    "negative", "negative", "negative", "negative",
    "negative", "negative",
]


def build_model():
    return Pipeline([
        ("tfidf", TfidfVectorizer()),
        ("classifier", LogisticRegression(max_iter=1000)),
    ])


def main():
    X_train, X_test, y_train, y_test = train_test_split(
        REVIEWS,
        LABELS,
        test_size=0.25,
        random_state=42,
        stratify=LABELS,
    )

    model = build_model()
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    print("Model Evaluation")
    print(classification_report(
        y_test, predictions, zero_division=0
    ))

    print("\nSentiment Analyzer")
    text = input("Enter a review: ").strip()

    if not text:
        print("Please enter a review.")
        return

    sentiment = model.predict([text])[0]
    print(f"Predicted sentiment: {sentiment.title()}")

    print(
        "Note: This is a learning demo trained on a tiny "
        "sample dataset, not a reliable production model."
    )


if __name__ == "__main__":
    main()
