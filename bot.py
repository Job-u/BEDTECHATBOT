import os
from unidecode import unidecode
import configparser
import re
from difflib import get_close_matches

class Bot:
    # List of commands that will end the conversation
    exit_commands = ("bye", "exit", "ty", "thanks", "done", "quit", "stop")
    
    # Dictionary of translations for supported phrases
    # Each key is an English phrase, with translations in Filipino and Casiguran Agta
    translations = {
        # Greetings and Common Phrases
        "What is your name": {"filipino": "Ano ang pangalan mo?", "casiguran_agta": "Anya i ngahen moa"},
        "Goodbye": {"filipino": "Paalam.", "casiguran_agta": "Naydén kako dén"},
        "Thank you": {"filipino": "Maraming salamat.", "casiguran_agta": "Me ado a salamat"},
        "I am sorry": {"filipino": "Patawarin mo ako.", "casiguran_agta": "Patawadén nék mo"},
        "Yes": {"filipino": "Opo", "casiguran_agta": "On"},
        "No": {"filipino": "Hindi po", "casiguran_agta": "Ewan be"},
        "My name is": {"filipino": "Ako si", "casiguran_agta": "Saken ti"},
        "Good to see you": {"filipino": "Buti na lang nakita kita", "casiguran_agta": "Meta"},
        "How are you": {"filipino": "Kamusta ka na?", "casiguran_agta": "Kumusta kam dén"},
        "I am fine": {"filipino": "Mabuti naman.", "casiguran_agta": "Ma ige be"},
        "Glad to meet you": {"filipino": "Masaya akong makilala ka", "casiguran_agta": "Mesahat ék a matenggi taka"},
        "Good afternoon": {"filipino": "Magandang hapon", "casiguran_agta": "Memahal a apon"},
        "Good noon": {"filipino": "Magandang tanghali", "casiguran_agta": "Memahal a tanghali"},
        "Good evening": {"filipino": "Magandang gabi", "casiguran_agta": "Memahal a kélép"},
        "Good morning": {"filipino": "Magandang umaga", "casiguran_agta": "Memahal a gagabi"},
        "How about you": {"filipino": "Kayo po? / Ikaw?", "casiguran_agta": "Sikam"},

        # Words
        "Family": {"filipino": "Pamilya", "casiguran_agta": "Metétena"},
        "Happy": {"filipino": "Masaya", "casiguran_agta": "Mesahat"},
        "Near": {"filipino": "Malapit", "casiguran_agta": "Asadek"},
        "Cold": {"filipino": "Malamig", "casiguran_agta": "Medignen"},

        # Weather
        "Rainy": {"filipino": "Maulan", "casiguran_agta": "Me uden"},
        "Cloudy": {"filipino": "Maulap", "casiguran_agta": "Me habuhab"},
        "Summer": {"filipino": "Tag-init", "casiguran_agta": "Tag init"},
        "Rainy season": {"filipino": "Tag-ulan", "casiguran_agta": "Tag udén"},
        "Warm": {"filipino": "Mainit", "casiguran_agta": "Me pasi"},
        "Windy": {"filipino": "Maulap", "casiguran_agta": "Me pahés"},

        # Animals
        "Dog": {"filipino": "Aso", "casiguran_agta": "Aso"},
        
        # Daily Use Expressions
        "Excuse me": {"filipino": "Makikiraan po", "casiguran_agta": "Mékidiman kame"},
        "I'm leaving": {"filipino": "Aalis na po ako", "casiguran_agta": "Még dema kamedén"},
        "Can you help me": {"filipino": "Maaari mo ba akong tulungan?", "casiguran_agta": "Pwede ék moy tulungan"},
        "What can I do for you": {"filipino": "Ano po ang magagawa ko para sa inyo?", "casiguran_agta": "Anyá i magimet koa para dekam"},
        "I understand": {"filipino": "Naiintindihan ko", "casiguran_agta": "Meentendian ko"},
        
        # Question Words
        "What": {"filipino": "Ano?", "casiguran_agta": "Anya"},
        "When": {"filipino": "Kailan?", "casiguran_agta": "Ni kesya"},
        "Where": {"filipino": "Saan?", "casiguran_agta": "tahe"},
        "Which": {"filipino": "Alin?", "casiguran_agta": "nahe"},
        "Who": {"filipino": "Sino?", "casiguran_agta": "te esya"},
        "Why": {"filipino": "Bakit?", "casiguran_agta": "ata ay"},
        "How much": {"filipino": "Magkano?", "casiguran_agta": "sanganya?"},

        # Colors
        "Blue": {"filipino": "Asul", "casiguran_agta": "Asul"},
        "Red": {"filipino": "Pula", "casiguran_agta": "Medingat"},
        "White": {"filipino": "Puti", "casiguran_agta": "Melatak"},
        "Black": {"filipino": "Itim", "casiguran_agta": "mengitet"},
        "Green": {"filipino": "Berde", "casiguran_agta": "Kumanidon"},
        "Yellow": {"filipino": "Dilaw", "casiguran_agta": "Medilaw"},
        "Brown": {"filipino": "Kulay tsokolate", "casiguran_agta": "Tsokolate"},
        "Gray": {"filipino": "Kulay abo", "casiguran_agta": "Kulay abo"},
        "Pink": {"filipino": "Rosas", "casiguran_agta": "Rosas"},
        "Orange": {"filipino": "Dalandan", "casiguran_agta": "Kuman a don"},
        "Violet": {"filipino": "Lila", "casiguran_agta": "Kuman a pensél"},

        # Family Members
        "Grandfather": {"filipino": "Lolo", "casiguran_agta": "Boboy lakay"},
        "Grandmother": {"filipino": "Lola", "casiguran_agta": "Boboy bakés"},
        "Father": {"filipino": "Tatay", "casiguran_agta": "Améng"},
        "Mother": {"filipino": "Nanay", "casiguran_agta": "Inéng"},
        "Older brother": {"filipino": "Kuya", "casiguran_agta": "Kakéng"},
        "Older sister": {"filipino": "Ate", "casiguran_agta": "Kakéng"},
        "Youngest sibling": {"filipino": "Bunso", "casiguran_agta": "Depos"},
        "Husband": {"filipino": "Asawang lalaki", "casiguran_agta": "Asawa a lalaki"},
        "Wife": {"filipino": "Asawang babae", "casiguran_agta": "Asawa a babe"},
        "Son": {"filipino": "Anak na lalaki", "casiguran_agta": "Anak a lalake"},
        "Daughter": {"filipino": "Anak na babae", "casiguran_agta": "Anak a babe"},
        "Aunt": {"filipino": "Tiya", "casiguran_agta": "Dada"},
        "Cousin": {"filipino": "Pinsan", "casiguran_agta": "Pensan"},
        "Uncle": {"filipino": "Tiyo", "casiguran_agta": "Lele"},
        "Niece": {"filipino": "Pamangkin", "casiguran_agta": "Anéng"},
        "Nephew": {"filipino": "Pamangkin", "casiguran_agta": "Anéng"},
        
        # Buying and Selling
        "How much? How many?": {"filipino": "Magkano? Ilan?", "casiguran_agta": "Sanganya?"},
        "How much for two": {"filipino": "Magkano ang dalawa?", "casiguran_agta": "Sangan éduwa"},
        "I will get two": {"filipino": "Kukuha ako ng dalawa", "casiguran_agta": "Mangalap pékta éduwa"},
        "Okay, you can get them": {"filipino": "Sige kunin mo na", "casiguran_agta": "Nay alapén mo dén"},
        "It is fifty pesos": {"filipino": "Limampung piso ito", "casiguran_agta": "Lima apulo ye"},
        "The two are 100 pesos": {"filipino": "Isang daang piso ang dalawa", "casiguran_agta": "Esa a daan éduwa"},

        # Giving Directions
        "Where are you going": {"filipino": "Saan ka pupunta?", "casiguran_agta": "Ahe ka umange"},
        "Im going to the garden": {"filipino": "Pupunta ako sa halamanan", "casiguran_agta": "Ange ékta sikaw"},
        "The garden is by the river": {"filipino": "Malapit sa ilog ang halamanan", "casiguran_agta": "Adene ta dinom ya tu sikaw"},
        "Whose garden is it": {"filipino": "Kaninong halamanan iyon?", "casiguran_agta": "Kini esya a sikaw ya"},
        "It is my garden": {"filipino": "Sa akin ang halamanan", "casiguran_agta": "Ko o ko a sikaw"}
    }

    def __init__(self):
        config = configparser.ConfigParser()
        config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
        config.read(config_path)
        self.audio_dataset = config.get('Paths', 'audio_dataset')

    def _normalize(self, text):
        """Lowercase, remove accents, punctuation, and common fillers in English/Tagalog."""
        if not text:
            return ""
        text = unidecode(text.lower())
        # Remove punctuation
        text = re.sub(r"[\.,!?;:\-_/\\'\"]+", " ", text)
        # Remove common fillers / prefixes
        fillers = [
            r"\bwhat is\b", r"\bwhat's\b", r"\bcan you translate\b", r"\bplease translate\b",
            r"\bano ang\b", r"\bano yung\b", r"\bano ito\b", r"\bpaki translate\b", r"\bpaki\b",
            r"\banong\b", r"\bmeaning ng\b", r"\bkahulugan ng\b", r"\btranslate\b"
        ]
        for f in fillers:
            text = re.sub(f, " ", text)
        # Collapse spaces
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def _format_translation(self, english):
        translations = self.translations[english]
        return (
            f"English: {english}\n"
            f"Filipino: {translations['filipino']}\n"
            f"Casiguran Agta: {translations['casiguran_agta']}"
        )

    def translate(self, userinput):
        """Translates user input with fuzzy matching and filler removal.
        Returns: (text_response, matched_english_phrase or None, suggestions_list)
        """
        if not userinput:
            return "Please provide a phrase to translate.", None, []

        userinput_norm = self._normalize(userinput)
        if not userinput_norm:
            return "Please provide a phrase to translate.", None, []

        # Build search corpus of phrases (map normalized phrase -> english key)
        phrase_to_english = {}
        corpus = []
        for english, translations in self.translations.items():
            entries = [english, translations['filipino'], translations['casiguran_agta']]
            for e in entries:
                norm = self._normalize(e)
                if not norm:
                    continue
                phrase_to_english[norm] = english
                corpus.append(norm)

        # 1) Exact normalized match across any language
        if userinput_norm in phrase_to_english:
            eng = phrase_to_english[userinput_norm]
            return self._format_translation(eng), eng, []

        # 2) Substring/includes match (e.g., input contains the word)
        includes = [p for p in corpus if p in userinput_norm or userinput_norm in p]
        if includes:
            # Prefer the shortest include as likely precise term
            includes.sort(key=len)
            eng = phrase_to_english[includes[0]]
            # Suggestions: other close includes mapped back to English, unique
            suggestions = []
            seen = set([eng])
            for p in includes[1:6]:
                e = phrase_to_english[p]
                if e not in seen:
                    seen.add(e)
                    suggestions.append(e)
            return self._format_translation(eng), eng, suggestions

        # 3) Fuzzy match against the corpus
        close = get_close_matches(userinput_norm, corpus, n=5, cutoff=0.6)
        if close:
            eng_top = phrase_to_english[close[0]]
            # Build unique English suggestions (skip the top match)
            suggestions = []
            seen = set([eng_top])
            for c in close[1:]:
                e = phrase_to_english[c]
                if e not in seen:
                    seen.add(e)
                    suggestions.append(e)
            return self._format_translation(eng_top), eng_top, suggestions

        # 4) If nothing found, provide detailed category guidance
        categories = {
            "Greetings": ["Good morning", "Good afternoon", "Good evening", "How are you", "I am fine", "Goodbye", "Thank you", "Glad to meet you", "Good to see you", "How about you"],
            "Family Members": ["Father", "Mother", "Grandfather", "Grandmother", "Older Brother", "Older Sister", "Youngest Sibling", "Husband", "Wife", "Son", "Daughter", "Aunt", "Cousin", "Uncle", "Nephew", "Niece"],
            "Colors": ["Blue", "Red", "White", "Black", "Green", "Yellow", "Brown", "Gray", "Pink", "Orange", "Violet"],
            "Animals": ["Dog"],
            "Question Words": ["What", "When", "Where", "Which", "Who", "Why", "How much"],
            "Daily Expressions": ["Excuse me", "I'm leaving", "Can you help me", "What can I do for you", "I understand"],
            "Words": ["Family", "Happy", "Near", "Rainy", "Cold"],
            "Buying and Selling": ["How much for two", "I will get two", "Okay, you can get them", "It is fifty pesos", "The two are 100 pesos"],
            "Giving Directions": ["Where are you going", "I'm going to the garden", "The garden is by the river", "Whose garden is it", "It is my garden"]
        }
        
        guide_parts = ["I couldn't find a close match. Here are categories you can try:"]
        for category, items in categories.items():
            guide_parts.append(f"{category}: {', '.join(items)}")
        
        guide = "\n".join(guide_parts)
        return guide, None, []