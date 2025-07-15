

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

def select_language_update():
    global selected_language
    x = input("Select Language (en/es/hi): ")
    if x in TRANSLATION:
        selected_language = x
    else:
        selected_language = "en"


def language_selector(key):
        return TRANSLATION.get(selected_language, TRANSLATION["en"]).get(key, key)
    


select_language_update()


sl = selected_language
# print(T)
