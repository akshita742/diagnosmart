# disease_info.py

import wikipedia

def get_disease_info(disease_name: str) -> str:
    """
    Fetches a short summary for the disease from Wikipedia.
    """
    try:
        summary = wikipedia.summary(disease_name, sentences=2, auto_suggest=False)
        return summary
    except wikipedia.exceptions.DisambiguationError as e:
        return f"⚠️ Too many matches for '{disease_name}'. Try being more specific."
    except wikipedia.exceptions.PageError:
        return f"❌ No information found for '{disease_name}'."
    except Exception as e:
        return f"❌ Could not fetch info: {e}"
