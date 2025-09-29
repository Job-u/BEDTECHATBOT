import os
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
        config = configparser.ConfigParser()
        config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
        config.read(config_path)
        self.audio_dataset = config.get('Paths', 'audio_dataset')

    def translate(self, userinput):
        """Translates user input using the translations dictionary"""
        if not userinput:
            return "Please provide a phrase to translate.", None

        userinput_clean = unidecode(userinput.lower().strip())

        # Try exact match
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

        return "Sorry, I don't have a translation for that phrase.", None