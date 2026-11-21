import urllib.parse
import webbrowser


def search_google(text):
    query = text.lower().strip()
    for prefix in ("search google for", "google search", "search for", "search", "google"):
        if query.startswith(prefix):
            query = query[len(prefix):].strip()
            break

    if not query:
        print("[Skill -> Web Search]: No search term provided.")
        return

    params = urllib.parse.urlencode({"q": query})
    url = "https://www.google.com" + chr(47) + "search?" + params
    print("[DEBUG URL]:", url)
    webbrowser.open(url)


def search_youtube(text):
    query = text.lower().strip()
    for prefix in ("search youtube for", "youtube", "play"):
        if query.startswith(prefix):
            query = query[len(prefix):].strip()
            break

    if query:
        params = urllib.parse.urlencode({"search_query": query})
        url = "https://www.youtube.com" + chr(47) + "results?" + params
        webbrowser.open(url)
        print(f"[Skill -> YouTube]: Searching YouTube for '{query}'")

def open_website(text):
    """Opens bookmarked websites directly."""
    lower = text.lower()
    websites = {
        "youtube": "https://www.youtube.com/",
        "steamrip": "https://steamrip.com/",
        "fmhy": "https://fmhy.net/",
    }

    for site_name, url in websites.items():
        if site_name in lower:
            webbrowser.open(url)
            print(f"[Skill -> Web]: Opening {site_name.upper()}")
            return True
    return False
