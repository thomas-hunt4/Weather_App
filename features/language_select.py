# Enhanced Language Selection and Translation System
# Supports English, Spanish, and Hindi with f-string variable support

TRANSLATION = {
    "en": {
        # Original keys
        "greeting": "hello",
        "theme button": "Dark Mode",
        
        # App and Navigation
        "app_title": "Weather Wonderland",
        "language_label": "Language:",
        "light_mode": "Light Mode",
        "dark_mode": "Dark Mode",
        
        # Weather Display Labels
        "temperature_label": "Temperature:",
        "description_label": "Description:",
        "wind_label": "Wind Speed:",
        "humidity_label": "Humidity:",
        "precipitation_label": "Chance of Precipitation:",
        "sunrise_label": "Sunrise:",
        "sunset_label": "Sunset:",
        
        # Weather Display Values (with variables)
        "city_display": "{city}, {country}",
        "temperature_display": "{temp}°C",
        "humidity_display": "{humidity}%",
        "wind_display": "{speed} m/s",
        "sunrise_display": "{time}",
        "sunset_display": "{time}",
        
        # Navigation Buttons
        "forecast_button": "Forecast",
        "trend_button": "Trending Temperature",
        "historical_button": "Historical Data",
        "weather_alerts_button": "Weather Alerts",
        "emergency_button": "Emergency Info",
        
        # Input and Search
        "select_city_prompt": "Enter a city to see weather",
        "select_city_placeholder": "Select City",
        "select_favorite": "Select Favorite",
        "loading_weather": "Loading weather for {city}...",
        "weather_loaded_success": "Weather data loaded for {city}",
        
        # Menu Items
        "menu_button": "Menu",
        "manage_favorites": "Manage Favorites",
        "settings": "Settings",
        "help": "Help",
        
        # Favorites Management
        "manage_favorites_title": "Manage Favorites",
        "add_city_label": "Add City:",
        "add_button": "Add",
        "remove_button": "Remove",
        "current_favorites_label": "Current Favorites:",
        
        # Quiz Section
        "weather_quiz_title": "Weather Quiz",
        "new_question_button": "New Question",
        "reset_quiz_button": "Reset Quiz",
        "quiz_score": "Score: {score}/{total} ({percent}%)",
        "quiz_loading": "Loading quiz question...",
        "quiz_no_questions": "No quiz questions available",
        "quiz_error": "Error loading quiz question",
        
        # Status Messages
        "current_location": "Current Location",
        "map_unavailable": "Map not available",
        
        # Error Titles
        "error_title": "Error",
        "invalid_input_title": "Invalid Input",
        "network_error_title": "Network Error",
        "city_not_found_title": "City Not Found",
        "api_key_error_title": "API Error",
        "timeout_error_title": "Connection Timeout",
        "general_api_error_title": "Weather Service Error",
        
        # Error Messages
        "empty_city_name": "Please enter a city name",
        "city_name_too_short": "City name must be at least 2 characters long",
        "city_name_too_long": "City name is too long (maximum 50 characters)",
        "invalid_city_characters": "City name contains invalid characters. Use only letters, spaces, and basic punctuation",
        "city_name_no_letters": "City name must contain at least one letter",
        "no_weather_data": "No weather data available to display",
        "display_weather_error": "Error displaying weather information",
        
        # API Error Messages
        "network_error_message": "Unable to connect to weather service. Please check your internet connection and try again.",
        "city_not_found_message": "The city '{city}' was not found. Please check the spelling and try again.",
        "api_key_error_message": "Weather service authentication failed. Please contact support.",
        "timeout_error_message": "The weather service is taking too long to respond. Please try again in a moment.",
        "general_api_error_message": "Unable to retrieve weather data for '{city}'. Error: {error}",
        
        # Success Messages
        "success_title": "Success",
        "favorite_added": "'{city}' has been added to your favorites",
        "favorite_removed": "'{city}' has been removed from your favorites",
        
        # Info Messages
        "info_title": "Information",
        "settings_coming_soon": "Settings feature coming soon!",
        "help_title": "Help",
        "help_information": "Welcome to Weather Wonderland! Enter a city name to get current weather information. Use favorites to quickly access your preferred locations.",
        
        # Warning Messages
        "weather_alert_title": "Weather Alert",
        "weather_alert_message": "Weather Alert: {alert}",
        
        # Emergency
        "emergency_title": "Emergency Information",
        "emergency_info": "In case of weather emergency, contact your local emergency services immediately. Stay indoors and follow official weather warnings.",
        
        # Feature Errors
        "favorite_selection_error": "Error selecting favorite city",
        "alerts_window_error": "Error opening weather alerts window",
        "menu_selection_error": "Error processing menu selection",
        "favorites_dialog_error": "Error opening favorites management",
        "favorite_add_failed": "Failed to add favorite: {error}",
        "favorite_add_error": "Error adding city to favorites",
        "favorite_remove_failed": "Failed to remove favorite: {error}",
        "favorite_remove_error": "Error removing city from favorites",
        
        # Quiz Messages
        "correct_answer_title": "Correct!",
        "correct_answer_message": "Great job! That's correct.",
        "incorrect_answer_title": "Incorrect",
        "incorrect_answer_message": "Sorry, that's not right. The correct answer is: {correct}",
        
        # Additional Quiz Keys
        "start_set": "Start Set {set_num}",
        "quiz_complete": "Quiz Complete!",
        "all_sets_complete": "All Sets Complete!",
        "quiz_display_error": "Error displaying quiz question",
        "search_error": "Error searching for weather data",
        
        # UI Elements
        "ok_button": "OK"
    },
    
    "es": {
        # Original keys
        "greeting": "buenas",
        "theme button": "Modo Oscuro",
        
        # App and Navigation
        "app_title": "Mundo del Clima",
        "language_label": "Idioma:",
        "light_mode": "Modo Claro",
        "dark_mode": "Modo Oscuro",
        
        # Weather Display Labels
        "temperature_label": "Temperatura:",
        "description_label": "Descripción:",
        "wind_label": "Velocidad del Viento:",
        "humidity_label": "Humedad:",
        "precipitation_label": "Posibilidad de Precipitación:",
        "sunrise_label": "Amanecer:",
        "sunset_label": "Atardecer:",
        
        # Weather Display Values (with variables)
        "city_display": "{city}, {country}",
        "temperature_display": "{temp}°C",
        "humidity_display": "{humidity}%",
        "wind_display": "{speed} m/s",
        "sunrise_display": "{time}",
        "sunset_display": "{time}",
        
        # Navigation Buttons
        "forecast_button": "Pronóstico",
        "trend_button": "Tendencia de Temperatura",
        "historical_button": "Datos Históricos",
        "weather_alerts_button": "Alertas Meteorológicas",
        "emergency_button": "Información de Emergencia",
        
        # Input and Search
        "select_city_prompt": "Ingrese una ciudad para ver el clima",
        "select_city_placeholder": "Seleccionar Ciudad",
        "select_favorite": "Seleccionar Favorito",
        "loading_weather": "Cargando clima para {city}...",
        "weather_loaded_success": "Datos del clima cargados para {city}",
        
        # Menu Items
        "menu_button": "Menú",
        "manage_favorites": "Gestionar Favoritos",
        "settings": "Configuración",
        "help": "Ayuda",
        
        # Favorites Management
        "manage_favorites_title": "Gestionar Favoritos",
        "add_city_label": "Agregar Ciudad:",
        "add_button": "Agregar",
        "remove_button": "Eliminar",
        "current_favorites_label": "Favoritos Actuales:",
        
        # Quiz Section
        "weather_quiz_title": "Quiz del Clima",
        "new_question_button": "Nueva Pregunta",
        "reset_quiz_button": "Reiniciar Quiz",
        "quiz_score": "Puntuación: {score}/{total} ({percent}%)",
        "quiz_loading": "Cargando pregunta del quiz...",
        "quiz_no_questions": "No hay preguntas de quiz disponibles",
        "quiz_error": "Error cargando pregunta del quiz",
        
        # Status Messages
        "current_location": "Ubicación Actual",
        "map_unavailable": "Mapa no disponible",
        
        # Error Titles
        "error_title": "Error",
        "invalid_input_title": "Entrada Inválida",
        "network_error_title": "Error de Red",
        "city_not_found_title": "Ciudad No Encontrada",
        "api_key_error_title": "Error de API",
        "timeout_error_title": "Tiempo de Conexión Agotado",
        "general_api_error_title": "Error del Servicio Meteorológico",
        
        # Error Messages
        "empty_city_name": "Por favor ingrese un nombre de ciudad",
        "city_name_too_short": "El nombre de la ciudad debe tener al menos 2 caracteres",
        "city_name_too_long": "El nombre de la ciudad es muy largo (máximo 50 caracteres)",
        "invalid_city_characters": "El nombre de la ciudad contiene caracteres inválidos. Use solo letras, espacios y puntuación básica",
        "city_name_no_letters": "El nombre de la ciudad debe contener al menos una letra",
        "no_weather_data": "No hay datos meteorológicos disponibles para mostrar",
        "display_weather_error": "Error mostrando información meteorológica",
        
        # API Error Messages
        "network_error_message": "No se puede conectar al servicio meteorológico. Verifique su conexión a internet e intente nuevamente.",
        "city_not_found_message": "La ciudad '{city}' no fue encontrada. Verifique la ortografía e intente nuevamente.",
        "api_key_error_message": "Falló la autenticación del servicio meteorológico. Contacte soporte técnico.",
        "timeout_error_message": "El servicio meteorológico está tardando mucho en responder. Intente nuevamente en un momento.",
        "general_api_error_message": "No se pueden obtener datos meteorológicos para '{city}'. Error: {error}",
        
        # Success Messages
        "success_title": "Éxito",
        "favorite_added": "'{city}' ha sido agregado a sus favoritos",
        "favorite_removed": "'{city}' ha sido eliminado de sus favoritos",
        
        # Info Messages
        "info_title": "Información",
        "settings_coming_soon": "¡Función de configuración próximamente!",
        "help_title": "Ayuda",
        "help_information": "¡Bienvenido a Mundo del Clima! Ingrese un nombre de ciudad para obtener información meteorológica actual. Use favoritos para acceder rápidamente a sus ubicaciones preferidas.",
        
        # Warning Messages
        "weather_alert_title": "Alerta Meteorológica",
        "weather_alert_message": "Alerta Meteorológica: {alert}",
        
        # Emergency
        "emergency_title": "Información de Emergencia",
        "emergency_info": "En caso de emergencia meteorológica, contacte inmediatamente a sus servicios de emergencia locales. Permanezca en interior y siga las advertencias meteorológicas oficiales.",
        
        # Feature Errors
        "favorite_selection_error": "Error seleccionando ciudad favorita",
        "alerts_window_error": "Error abriendo ventana de alertas meteorológicas",
        "menu_selection_error": "Error procesando selección de menú",
        "favorites_dialog_error": "Error abriendo gestión de favoritos",
        "favorite_add_failed": "Error al agregar favorito: {error}",
        "favorite_add_error": "Error agregando ciudad a favoritos",
        "favorite_remove_failed": "Error al eliminar favorito: {error}",
        "favorite_remove_error": "Error eliminando ciudad de favoritos",
        
        # Quiz Messages
        "correct_answer_title": "¡Correcto!",
        "correct_answer_message": "¡Buen trabajo! Eso es correcto.",
        "incorrect_answer_title": "Incorrecto",
        "incorrect_answer_message": "Lo siento, eso no es correcto. La respuesta correcta es: {correct}",
        
        # Additional Quiz Keys  
        "start_set": "Iniciar Set {set_num}",
        "quiz_complete": "¡Quiz Completado!",
        "all_sets_complete": "¡Todos los Sets Completados!",
        "quiz_display_error": "Error mostrando pregunta del quiz",
        "search_error": "Error buscando datos meteorológicos",
        
        # UI Elements
        "ok_button": "OK"
    },
    
    "hi": {
        # Original keys
        "greeting": "नमस्ते",
        "theme button": "डार्क मोड",
        
        # App and Navigation
        "app_title": "मौसम वंडरलैंड",
        "language_label": "भाषा:",
        "light_mode": "लाइट मोड",
        "dark_mode": "डार्क मोड",
        
        # Weather Display Labels
        "temperature_label": "तापमान:",
        "description_label": "विवरण:",
        "wind_label": "हवा की गति:",
        "humidity_label": "नमी:",
        "precipitation_label": "बारिश की संभावना:",
        "sunrise_label": "सूर्योदय:",
        "sunset_label": "सूर्यास्त:",
        
        # Weather Display Values (with variables)
        "city_display": "{city}, {country}",
        "temperature_display": "{temp}°C",
        "humidity_display": "{humidity}%",
        "wind_display": "{speed} मी/से",
        "sunrise_display": "{time}",
        "sunset_display": "{time}",
        
        # Navigation Buttons
        "forecast_button": "पूर्वानुमान",
        "trend_button": "तापमान प्रवृत्ति",
        "historical_button": "ऐतिहासिक डेटा",
        "weather_alerts_button": "मौसम अलर्ट",
        "emergency_button": "आपातकालीन जानकारी",
        
        # Input and Search
        "select_city_prompt": "मौसम देखने के लिए शहर का नाम दर्ज करें",
        "select_city_placeholder": "शहर चुनें",
        "select_favorite": "पसंदीदा चुनें",
        "loading_weather": "{city} के लिए मौसम लोड हो रहा है...",
        "weather_loaded_success": "{city} के लिए मौसम डेटा लोड हो गया",
        
        # Menu Items
        "menu_button": "मेनू",
        "manage_favorites": "पसंदीदा प्रबंधित करें",
        "settings": "सेटिंग्स",
        "help": "सहायता",
        
        # Favorites Management
        "manage_favorites_title": "पसंदीदा प्रबंधित करें",
        "add_city_label": "शहर जोड़ें:",
        "add_button": "जोड़ें",
        "remove_button": "हटाएं",
        "current_favorites_label": "वर्तमान पसंदीदा:",
        
        # Quiz Section
        "weather_quiz_title": "मौसम प्रश्नोत्तरी",
        "new_question_button": "नया प्रश्न",
        "reset_quiz_button": "प्रश्नोत्तरी रीसेट करें",
        "quiz_score": "स्कोर: {score}/{total} ({percent}%)",
        "quiz_loading": "प्रश्नोत्तरी प्रश्न लोड हो रहा है...",
        "quiz_no_questions": "कोई प्रश्नोत्तरी प्रश्न उपलब्ध नहीं",
        "quiz_error": "प्रश्नोत्तरी प्रश्न लोड करने में त्रुटि",
        
        # Status Messages
        "current_location": "वर्तमान स्थान",
        "map_unavailable": "मानचित्र उपलब्ध नहीं",
        
        # Error Titles
        "error_title": "त्रुटि",
        "invalid_input_title": "अमान्य इनपुट",
        "network_error_title": "नेटवर्क त्रुटि",
        "city_not_found_title": "शहर नहीं मिला",
        "api_key_error_title": "API त्रुटि",
        "timeout_error_title": "कनेक्शन टाइमआउट",
        "general_api_error_title": "मौसम सेवा त्रुटि",
        
        # Error Messages
        "empty_city_name": "कृपया शहर का नाम दर्ज करें",
        "city_name_too_short": "शहर का नाम कम से कम 2 अक्षरों का होना चाहिए",
        "city_name_too_long": "शहर का नाम बहुत लंबा है (अधिकतम 50 अक्षर)",
        "invalid_city_characters": "शहर के नाम में अमान्य अक्षर हैं। केवल अक्षर, स्थान और बुनियादी विराम चिह्न का उपयोग करें",
        "city_name_no_letters": "शहर के नाम में कम से कम एक अक्षर होना चाहिए",
        "no_weather_data": "प्रदर्शित करने के लिए कोई मौसम डेटा उपलब्ध नहीं",
        "display_weather_error": "मौसम जानकारी प्रदर्शित करने में त्रुटि",
        
        # API Error Messages
        "network_error_message": "मौसम सेवा से कनेक्ट नहीं हो सका। कृपया अपना इंटरनेट कनेक्शन जांचें और पुनः प्रयास करें।",
        "city_not_found_message": "शहर '{city}' नहीं मिला। कृपया स्पेलिंग जांचें और पुनः प्रयास करें।",
        "api_key_error_message": "मौसम सेवा प्रमाणीकरण विफल। कृपया सहायता से संपर्क करें।",
        "timeout_error_message": "मौसम सेवा का जवाब आने में बहुत समय लग रहा है। कृपया एक क्षण में पुनः प्रयास करें।",
        "general_api_error_message": "'{city}' के लिए मौसम डेटा प्राप्त नहीं कर सका। त्रुटि: {error}",
        
        # Success Messages
        "success_title": "सफलता",
        "favorite_added": "'{city}' आपके पसंदीदा में जोड़ दिया गया है",
        "favorite_removed": "'{city}' आपके पसंदीदा से हटा दिया गया है",
        
        # Info Messages
        "info_title": "जानकारी",
        "settings_coming_soon": "सेटिंग्स सुविधा जल्द आ रही है!",
        "help_title": "सहायता",
        "help_information": "मौसम वंडरलैंड में आपका स्वागत है! वर्तमान मौसम जानकारी पाने के लिए शहर का नाम दर्ज करें। अपने पसंदीदा स्थानों तक तुरंत पहुंचने के लिए पसंदीदा का उपयोग करें।",
        
        # Warning Messages
        "weather_alert_title": "मौसम अलर्ट",
        "weather_alert_message": "मौसम अलर्ट: {alert}",
        
        # Emergency
        "emergency_title": "आपातकालीन जानकारी",
        "emergency_info": "मौसम आपातकाल की स्थिति में, तुरंत अपनी स्थानीय आपातकालीन सेवाओं से संपर्क करें। घर के अंदर रहें और आधिकारिक मौसम चेतावनियों का पालन करें।",
        
        # Feature Errors
        "favorite_selection_error": "पसंदीदा शहर चुनने में त्रुटि",
        "alerts_window_error": "मौसम अलर्ट विंडो खोलने में त्रुटि",
        "menu_selection_error": "मेनू चयन प्रसंस्करण में त्रुटि",
        "favorites_dialog_error": "पसंदीदा प्रबंधन खोलने में त्रुटि",
        "favorite_add_failed": "पसंदीदा जोड़ने में विफल: {error}",
        "favorite_add_error": "शहर को पसंदीदा में जोड़ने में त्रुटि",
        "favorite_remove_failed": "पसंदीदा हटाने में विफल: {error}",
        "favorite_remove_error": "शहर को पसंदीदा से हटाने में त्रुटि",
        
        # Quiz Messages
        "correct_answer_title": "सही!",
        "correct_answer_message": "बहुत बढ़िया! यह सही है।",
        "incorrect_answer_title": "गलत",
        "incorrect_answer_message": "खुशी है कि यह सही नहीं है। सही उत्तर है: {correct}",
        
        # Additional Quiz Keys
        "start_set": "सेट {set_num} शुरू करें",
        "quiz_complete": "प्रश्नोत्तरी पूर्ण!",
        "all_sets_complete": "सभी सेट पूर्ण!",
        "quiz_display_error": "प्रश्नोत्तरी प्रश्न प्रदर्शित करने में त्रुटि",
        "search_error": "मौसम डेटा खोजने में त्रुटि",
        
        # UI Elements
        "ok_button": "ठीक"
    }
}

selected_language = "en"

def set_language(lang_code):
    """Set the current language"""
    global selected_language
    if lang_code in TRANSLATION:
        selected_language = lang_code
    else:
        selected_language = "en"

def get_language():
    """Get the current language code"""
    return selected_language

def language_selector(key, **kwargs):
    """
    Get translated text for a key with optional formatting variables
    
    Args:
        key (str): Translation key
        **kwargs: Variables for f-string formatting
    
    Returns:
        str: Translated and formatted text
    """
    # Get the translation for the current language, fallback to English
    translation = TRANSLATION.get(selected_language, TRANSLATION["en"]).get(key, key)
    
    # If no kwargs provided, return the translation as-is
    if not kwargs:
        return translation
    
    # Apply f-string formatting with provided variables
    try:
        return translation.format(**kwargs)
    except (KeyError, ValueError) as e:
        print(f"Translation formatting error for key '{key}': {e}")
        # Return the unformatted translation as fallback
        return translation

# Alias for convenience - this is what the home_page.py uses
def t(key, **kwargs):
    """Convenience alias for language_selector"""
    return language_selector(key, **kwargs)

# Additional utility functions for language management

def get_available_languages():
    """Get list of available language codes"""
    return list(TRANSLATION.keys())

def get_language_name(lang_code):
    """Get human-readable language name"""
    language_names = {
        "en": "English",
        "es": "Español", 
        "hi": "हिन्दी"
    }
    return language_names.get(lang_code, lang_code)

def is_language_available(lang_code):
    """Check if a language is available"""
    return lang_code in TRANSLATION

def add_translation_key(key, translations):
    """
    Add a new translation key with translations for all languages
    
    Args:
        key (str): Translation key
        translations (dict): Dictionary with language codes as keys and translations as values
    """
    for lang_code, translation in translations.items():
        if lang_code in TRANSLATION:
            TRANSLATION[lang_code][key] = translation

def get_missing_translations(lang_code):
    """
    Get list of translation keys missing from a language
    
    Args:
        lang_code (str): Language code to check
        
    Returns:
        list: List of missing keys
    """
    if lang_code not in TRANSLATION:
        return []
    
    english_keys = set(TRANSLATION["en"].keys())
    lang_keys = set(TRANSLATION[lang_code].keys())
    
    return list(english_keys - lang_keys)

def validate_translations():
    """
    Validate all translations and report any issues
    
    Returns:
        dict: Dictionary with validation results
    """
    results = {
        "missing_keys": {},
        "formatting_errors": {},
        "total_keys": len(TRANSLATION["en"])
    }
    
    english_keys = set(TRANSLATION["en"].keys())
    
    for lang_code in TRANSLATION:
        if lang_code == "en":
            continue
            
        lang_keys = set(TRANSLATION[lang_code].keys())
        missing = english_keys - lang_keys
        
        if missing:
            results["missing_keys"][lang_code] = list(missing)
    
    return results

# Export commonly used functions
__all__ = [
    'set_language', 
    'get_language', 
    'language_selector', 
    't',
    'get_available_languages',
    'get_language_name',
    'is_language_available',
    'validate_translations'
]