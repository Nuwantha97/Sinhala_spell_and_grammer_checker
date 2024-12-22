import Levenshtein
from app.utils import sinhala_to_ipa

def spell_check(word, ipa_list, top_n=3):
    # List to store IPA matches and their distances
    word_distances = [
        (ipa, Levenshtein.distance(word, ipa)) for ipa in ipa_list
    ]

    # Sort by Levenshtein distance and return the top N results
    word_distances.sort(key=lambda x: x[1])
    return word_distances[:top_n]


def check_sentence(sentence, sinhala_dictionary):
    ipa_list = sinhala_dictionary["IPA"]  # List of IPA representations
    ipa_to_word = sinhala_dictionary["word"]  # Map IPA to actual words

    words = sentence.split()  # Split the sentence into words
    corrected_words = []  # Store corrected words
    suggestions = {}  # Store suggestions for each word

    for word in words:
        # Get top suggestions based on IPA
        top_words = spell_check(sinhala_to_ipa(word), ipa_list, top_n=3)
        if top_words:
            # Get the actual word for the top IPA suggestion
            corrected_word = ipa_to_word.get(top_words[0][0], word)
            corrected_words.append(corrected_word)

            # Add all suggestions (converted from IPA to actual words)
            suggestions[word] = [
                (ipa_to_word.get(ipa, ipa), distance) for ipa, distance in top_words
            ]
        else:
            corrected_words.append(word)  # Use original word if no suggestion
            suggestions[word] = [("No suggestion", None)]  # No suggestions available

    # Combine corrected words into a sentence
    corrected_sentence = " ".join(corrected_words)

    # Return original sentence, corrected sentence, and suggestions
    return sentence, corrected_sentence, suggestions

