

TRANSLATION = {
    "en":{
        "greeting": "hello",
        "theme button": "Dark Mode",
    },
    "es":{
        "greeting": "buenas"
    },
    "hi":{
        "greeting": "नमस्ते"
    }
}


selected_language = "en"

def set_language(lang_code):
    global selected_language
    if lang_code in TRANSLATION:
        selected_language = lang_code
    else:
        selected_language = "en"

def get_language():
    return selected_language

def language_selector(key):
        return TRANSLATION.get(selected_language, TRANSLATION["en"]).get(key, key)
    



