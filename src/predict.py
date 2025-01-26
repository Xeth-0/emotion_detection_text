import nltk
import cloudpickle

nltk.download("punkt_tab")

# load model
with open("./model/emotion_model.pkl", "rb") as f:
    artifact = cloudpickle.load(f)


def predict_text_emotion(text: str) -> tuple:
    model = artifact["model"]

    EmotionFeatureExtractor = artifact["EmotionFeatureExtractor"]
    nrc_emotion_map = artifact["nrc_emotion_map"]
    nrc_emotion_categories = artifact["nrc_emotion_categories"]

    # Split the text into sentences
    sentences = nltk.tokenize.sent_tokenize(text)

    # Predict the probabilities of each emotion for each sentence
    probabilities = [model.predict_proba([sentence]) for sentence in sentences]

    # Predict the most likely emotion for each sentence
    emotions = [model.predict([sentence]) for sentence in sentences]

    # Return the probabilities of the emotions over the entire text(average of the probabilities of each sentence) and the most likely emotion
    # Return it in json format: {"probabilities": {emotion: probability}, "top_emotion": emotion}
    # Calculate the average probabilities for each emotion
    avg_probabilities = {}
    for prob in probabilities:
        for emotion, value in zip(model.classes_, prob[0]):
            if emotion not in avg_probabilities:
                avg_probabilities[emotion] = 0
            avg_probabilities[emotion] += value / len(probabilities)

    # Determine the most likely emotion for the entire text
    top_emotion = max(avg_probabilities, key=avg_probabilities.get)

    # Return the result in the specified format
    return {"probabilities": avg_probabilities, "top_emotion": top_emotion}

def load_model():
    global pipeline
    
    # Load with patched pathlib
    with open("emotion_model.pkl", "rb") as f:
        artifact = cloudpickle.load(f)
    
    # Post-process spaCy components
    if "nlp" in artifact:  # If you have spaCy in your pipeline
        import spacy
        artifact["nlp"] = spacy.load("en_core_web_sm")
    
    return artifact
