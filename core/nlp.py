import spacy


def extract_entities(text):
    # Load the English language model
    nlp = spacy.load("en_core_web_sm")
    # Process the text with the model
    doc = nlp(text)
    # Extract the named entities
    entities = [(entity.text, entity.label_) for entity in doc.ents]
    # Return the entities
    return entities
