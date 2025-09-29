import os
import pygame
import speech_recognition as sr
from unidecode import unidecode
import configparser

class Bot:
    # List of commands that will end the conversation
    exit_commands = ("bye", "exit", "ty", "thanks", "done", "quit", "stop")
    
    # Dictionary of translations for supported phrases
    # Each key is an English phrase, with translations in Filipino and Casiguran Agta
    translations = {
        # Greetings and Common Phrases
        "What is your name?": {"filipino": "Ano ang pangalan mo?", "casiguran_agta": "anya i ngahen moa"},
        "Goodbye": {"filipino": "Paalam.", "casiguran_agta": "naydén kako dén"},
        "Thank you.": {"filipino": "Maraming salamat.", "casiguran_agta": "me ado a salamat"},
        "I am sorry.": {"filipino": "Patawarin mo ako.", "casiguran_agta": "Patawadén nék mo"},
        "Yes.": {"filipino": "Opo.", "casiguran_agta": "on"},
        "No.": {"filipino": "Hindi po.", "casiguran_agta": "ewan be"},
        "My name is": {"filipino": "Ako si", "casiguran_agta": "saken ti"},
        "Good to see you": {"filipino": "Buti na lang nakita kita", "casiguran_agta": "meta"},
        "How are you?": {"filipino": "Kamusta ka na?", "casiguran_agta": "kumusta kam dén"},
        "I am fine": {"filipino": "Mabuti naman.", "casiguran_agta": "ma ige be"},
        "Glad to meet you": {"filipino": "Masaya akong makilala ka.", "casiguran_agta": "mesahat ék a matenggi taka"},
        "Good afternoon": {"filipino": "Magandang hapon", "casiguran_agta": "memahal a apon"},
        "Good evening": {"filipino": "Magandang gabi", "casiguran_agta": "memahal a kélép"},
        "Good morning": {"filipino": "Magandang umaga", "casiguran_agta": "memahal a gagabi"},
        "How about you?": {"filipino": "Kayo po? / Ikaw?", "casiguran_agta": "sikam"},

        # Words
        "Family": {"filipino": "Pamilya", "casiguran_agta": "Mététena"},
        "Happy": {"filipino": "Masaya", "casiguran_agta": "Mesahat"},
        "Near": {"filipino": "Malapit", "casiguran_agta": "Asadek"},
        "Rainy": {"filipino": "Maulan", "casiguran_agta": "Me uden"},

        # Animals
        "Dog": {"filipino": "Aso", "casiguran_agta": "Aso"},
        
        # Daily Use Expressions
        "Excuse me": {"filipino": "Makikiraan po.", "casiguran_agta": "mékidiman kame"},
        "I'm leaving": {"filipino": "Aalis na po ako.", "casiguran_agta": "még dema kamedén"},
        "Can you help me": {"filipino": "Maaari mo ba akong tulungan?", "casiguran_agta": "pwede ék moy tulungan"},
        "What can I do for you": {"filipino": "Ano po ang magagawa ko para sa inyo?", "casiguran_agta": "anya i magimet koa para dekam"},
        "I understand": {"filipino": "Naiintindihan ko.", "casiguran_agta": "meentendian ko"},
        
        # Question Words
        "What": {"filipino": "Ano?", "casiguran_agta": "anya"},
        "When": {"filipino": "Kailan?", "casiguran_agta": "ni kesya"},
        "Where": {"filipino": "Saan?", "casiguran_agta": "tahe"},
        "Which": {"filipino": "Alin?", "casiguran_agta": "nahe"},
        "Who": {"filipino": "Sino?", "casiguran_agta": "te esya"},
        "Why": {"filipino": "Bakit?", "casiguran_agta": "ata ay"},
        "How much": {"filipino": "Magkano?", "casiguran_agta": "sanganya?"},

        # Colors
        "Blue": {"filipino": "Asul", "casiguran_agta": "asul"},
        "Red": {"filipino": "Pula", "casiguran_agta": "medingat"},
        "White": {"filipino": "Puti", "casiguran_agta": "melatak"},
        "Black": {"filipino": "Itim", "casiguran_agta": "mengitet"},
        "Green": {"filipino": "Berde", "casiguran_agta": "kumanidon"},
        "Yellow": {"filipino": "Dilaw", "casiguran_agta": "medilaw"},
        "Brown": {"filipino": "Kulay tsokolate", "casiguran_agta": "tsokolate"},
        "Gray": {"filipino": "Kulay abo", "casiguran_agta": "kulay abo"},
        "Pink": {"filipino": "Rosas", "casiguran_agta": "rosas"},
        "Orange": {"filipino": "Dalandan", "casiguran_agta": "Kuman a don"},
        "Violet": {"filipino": "Lila", "casiguran_agta": "Kuman a pensél"},

        # Family Members
        "Grandfather": {"filipino": "Lolo", "casiguran_agta": "boboy lakay"},
        "Grandmother": {"filipino": "Lola", "casiguran_agta": "boboy bakés"},
        "Father": {"filipino": "Tatay", "casiguran_agta": "améng"},
        "Mother": {"filipino": "Nanay", "casiguran_agta": "inéng"},
        "Older Brother": {"filipino": "Kuya", "casiguran_agta": "kakéng"},
        "Older Sister": {"filipino": "Ate", "casiguran_agta": "kakéng"},
        "Youngest Sibling": {"filipino": "Bunso", "casiguran_agta": "depos"},
        "Husband": {"filipino": "Asawang lalaki", "casiguran_agta": "asawa a lalaki"},
        "Wife": {"filipino": "Asawang babae", "casiguran_agta": "asawa a babe"},
        "Son": {"filipino": "Anak na lalaki", "casiguran_agta": "anak a lalake"},
        "Daughter": {"filipino": "Anak na babae", "casiguran_agta": "anak a babe"},
        "Aunt": {"filipino": "Tiya", "casiguran_agta": "Dada"},
        "Cousin": {"filipino": "Pinsan", "casiguran_agta": "Pensan"},
        
        # Buying and Selling
        "How much for two": {"filipino": "Magkano ang dalawa?", "casiguran_agta": "sangan éduwa"},
        "I will get two": {"filipino": "Kukuha ako ng dalawa.", "casiguran_agta": "mangalap pékta éduwa"},
        "Okay, you can get them": {"filipino": "Sige kunin mo na.", "casiguran_agta": "nay alapén mo dén"},
        "It is fifty pesos": {"filipino": "Limampung piso ito.", "casiguran_agta": "lima apulo ye"},
        "The two are 100 pesos": {"filipino": "Isang daang piso ang dalawa.", "casiguran_agta": "esa a daan éduwa"},

        # Giving Directions
        "Where are you going": {"filipino": "Saan ka pupunta?", "casiguran_agta": "ahe ka umange"},
        "I'm going to the garden": {"filipino": "Pupunta ako sa halamanan.", "casiguran_agta": "ange ékta sikaw"},
        "Where is the garden": {"filipino": "Nasaan ang halamanan?", "casiguran_agta": "ahe to sikaw"},
        "The garden is by the river": {"filipino": "Malapit sa ilog ang halamanan.", "casiguran_agta": "adene ta dinom ya tu sikaw"},
        "Whose garden is it": {"filipino": "Kaninong halamanan iyon?", "casiguran_agta": "kini esya a sikaw ya"},
        "It is my garden": {"filipino": "Sa akin ang halamanan.", "casiguran_agta": "ko o ko a sikaw"}
    }

    def __init__(self):
        # Loads configuration for audio dataset path from config.ini
        config = configparser.ConfigParser()
        config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
        config.read(config_path)
        self.audio_dataset = config.get('Paths', 'audio_dataset')
        
        # Initialize the speech recognizer and pygame mixer for audio playback
        self.recognizer = sr.Recognizer()
        pygame.mixer.init()

    def translate(self, userinput):
        """
        Tries to match the user's input to a known phrase.
        Returns the translation and the matched English phrase (for audio lookup).
        """
        userinput_clean = unidecode(userinput.lower().strip())

        # 1) Prefer exact match on any language
        for english, translations in self.translations.items():
            english_clean = unidecode(english.lower())
            filipino_clean = unidecode(translations['filipino'].lower())
            agta_clean = unidecode(translations['casiguran_agta'].lower())

            if userinput_clean in (english_clean, filipino_clean, agta_clean):
                translation_text = (
                    f"English: {english}\n"
                    f"Filipino: {translations['filipino']}\n"
                    f"Casiguran Agta: {translations['casiguran_agta']}"
                )
                return translation_text, english

        # 2) Then try word-boundary contains (avoid "mother" matching "grandmother")
        import re
        def contains_word(haystack: str, needle: str) -> bool:
            if not needle:
                return False
            pattern = r"(^|\W)" + re.escape(needle) + r"(\W|$)"
            return re.search(pattern, haystack) is not None

        for english, translations in self.translations.items():
            english_clean = unidecode(english.lower())
            filipino_clean = unidecode(translations['filipino'].lower())
            agta_clean = unidecode(translations['casiguran_agta'].lower())

            if (contains_word(english_clean, userinput_clean) or contains_word(userinput_clean, english_clean) or
                contains_word(filipino_clean, userinput_clean) or contains_word(userinput_clean, filipino_clean) or
                contains_word(agta_clean, userinput_clean) or contains_word(userinput_clean, agta_clean)):
                translation_text = (
                    f"English: {english}\n"
                    f"Filipino: {translations['filipino']}\n"
                    f"Casiguran Agta: {translations['casiguran_agta']}"
                )
                return translation_text, english

        # If no match is found, return a default message
        return "Oops! We don’t have a translation for that yet.", None

    def voice_input(self):
        """
        Uses the microphone to capture user's speech and convert it to text.
        Returns the recognized text or an error message if recognition fails.
        """
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = self.recognizer.listen(source)
            text = self.recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand.")
            return ""
        except sr.RequestError as e:
            print(f"Speech service is not available right now. Error: {e}")
            return ""
        except Exception as e:
            print(f"Unexpected error: {e}")
            return ""