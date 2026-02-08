import pandas as pd

def load_dictionary(file_path):
    # Load the Sinhala dictionary CSV file
    df = pd.read_csv(file_path)
    return {
        "IPA": df["IPA"].tolist(),
        "word": df.set_index("IPA")["word"].to_dict(),
    }

def sinhala_to_ipa(text):
    consonant_map = {
        "ක": "k", "ඛ": "kʰ", "ග": "ɡ", "ඝ": "ɡʱ",
        "ඞ": "ŋ", "ඟ": "ŋɡ", "ච": "ʧ", "ඡ": "ʧʰ",
        "ජ": "ʤ", "ඣ": "ʤʱ", "ඤ": "ɲ", "ඥ": "ɡn",
        "ට": "ʈ", "ඨ": "ʈʰ", "ඩ": "ɖ", "ඪ": "ɖʱ",
        "ණ": "ɳ", "ත": "t̪", "ථ": "t̪ʰ", "ද": "d̪",
        "ධ": "d̪ʱ", "න": "n̪", "ප": "p", "ඵ": "pʰ",
        "බ": "b", "භ": "bʱ", "ම": "m", "ය": "j",
        "ර": "r", "ල": "l", "ව": "ʋ", "ශ": "ʃ",
        "ෂ": "ʂ", "ස": "s", "හ": "h", "ළ": "ɭ",
        "ෆ": "f"
    }

    vowel_map = {
        "අ": "ʌ", "ආ": "aː", "ඇ": "æ", "ඈ": "æː",
        "ඉ": "i", "ඊ": "iː", "උ": "u", "ඌ": "uː",
        "එ": "e", "ඒ": "eː", "ඔ": "o", "ඕ": "oː",
        "ා": "aː", "ැ": "æ", "ෑ": "æː", "ි": "i",
        "ී": "iː", "ු": "u", "ූ": "uː", "ෙ": "e",
        "ේ": "eː", "ො": "o", "ෝ": "oː", "ෞ": "au"
    }

    def get_next_chars(pos, text, count=3):
        result = []
        for i in range(count):
            if pos + i < len(text):
                result.append(text[pos + i])
            else:
                result.append(None)
        return result

    def process_syllable(pos, text):
        char = text[pos]
        next_chars = get_next_chars(pos + 1, text)

        if char == " ":
            return "| ", 1

        if char == "අ" and next_chars[0] == "ං":
            return "ʌŋ ", 2

        if char == "ං":
            return "", 1

        if char in consonant_map:
            if char == "න" and pos + 2 < len(text) and text[pos:pos+3] == "නවා":
                return "n̪ ə ", 1

            if char == "ව" and pos + 1 < len(text) and text[pos:pos+2] == "වා":
                return "ʋ a ", 2

            base = consonant_map[char] + " "

            if next_chars[0] in vowel_map:
                return base, 1
            elif next_chars[0] == "්":
                return base, 2
            elif pos == len(text) - 1:
                return base + "ə ", 1
            else:
                if char == "ක" and pos == 1:
                    return base + "ʌ ", 1
                else:
                    return base + "ʌ ", 1

        elif char in vowel_map:
            if char == "ා" and pos == len(text) - 1:
                return "", 1
            return vowel_map[char] + " ", 1

        elif char == "්":
            return "", 1

        return char + " ", 1

    result = ""
    i = 0
    while i < len(text):
        segment, skip = process_syllable(i, text)
        result += segment
        i += skip

    result = result.strip()
    while "  " in result:
        result = result.replace("  ", " ")

    return result