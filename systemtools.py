import os
import subprocess
from datetime import datetime


def tell_time(text=None):
    now = datetime.now().strftime("%I:%M %p")
    print(f"[Skill -> System]: Current time is {now}")


def tell_date(text=None):
    today = datetime.now().strftime("%A, %B %d, %Y")
    print(f"[Skill -> System]: Today is {today}")


def open_app(text):
    lower = text.lower()

    # Map voice/typed keywords to your exact shortcut paths
    apps = {
        "autocad": r"C:\Users\Public\Desktop\AutoCAD 2027 - English.lnk",
        "cloudflare": r"C:\Users\Ritesh\Desktop\Cloudflare One Client.lnk",
        "steam": r"C:\Users\Public\Desktop\Steam.lnk",
        "nvidia": r"C:\Users\Public\Desktop\NVIDIA App.lnk",
        "epic": r"C:\Users\Public\Desktop\Epic Games Launcher.lnk",
        "blender": r"C:\Users\Ritesh\Desktop\Blender 5.1.lnk",
        "unreal": r"C:\Users\Ritesh\Desktop\Unreal Engine.lnk",
        "lm studio": r"C:\Users\Ritesh\Desktop\LM Studio.lnk",
        "vs code": r"C:\Users\Ritesh\Desktop\Visual Studio Code.lnk",
        "visual studio": r"C:\Users\Ritesh\Desktop\Visual Studio Code.lnk",
        "secret neighbor": r"E:\games\Secret-Neighbor-SteamRIP.com\Secret Neighbor\Secret Neighbor.exe",
        "spider-man": r"E:\games\Marvels-Spider-Man-2-SteamRIP.com\Marvels Spider-Man 2\Spider-Man2.exe",
        "spiderman": r"E:\games\Marvels-Spider-Man-2-SteamRIP.com\Marvels Spider-Man 2\Spider-Man2.exe",
        "fall guys": r"C:\Users\Ritesh\Desktop\Fall Guys.url",

    }

    # Check your desktop shortcuts first
    for keyword, path in apps.items():
        if keyword in lower:
            if os.path.exists(path):
                os.startfile(path)
                print(f"[Skill -> System]: Opening {keyword.title()}")
            else:
                print(f"[Skill -> System]: Shortcut not found at {path}")
            return

    # Built-in Windows Apps, Settings, & Lenovo Vantage
    
    if "settings" in lower or "setting" in lower:
        os.system("start ms-settings:")
        print("[Skill -> System]: Opening Windows Settings")
    elif "notepad" in lower:
        os.system("start notepad")
        print("[Skill -> System]: Opening Notepad")
    elif "calculator" in lower or "calc" in lower:
        os.system("start calc")
        print("[Skill -> System]: Opening Calculator")
    
    elif "vantage" in lower or "wantage" in lower:
        os.startfile(r"shell:AppsFolder\E046963F.LenovoCompanion_k1h2ywk1493x8!App")
        print("[Skill -> System]: Opening Lenovo Vantage")
        return


        
    elif "settings" in lower or "setting" in lower:
        os.system("start ms-settings:")
        print("[Skill -> System]: Opening Windows Settings")

    else:
        print("[Skill -> System]: App not recognized.")
