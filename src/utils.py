import requests
import json
from bs4 import BeautifulSoup

def change_words(text, old_word, new_word):
    updated_text = text.replace(old_word, new_word)
    return updated_text

def chg_json_var(file_path: str, key: str, new_value):
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    if key in data:
        data[key] = new_value

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
    else:
        return

def welcome_message(member):
    welcome = (
        f"Hos geldin {member}, sunucuya katilman icin bir kac soruya cevap vermelisin.\n"
        "> Yasin kac? (Yas kisitlamasi yoktur.)\n"
        "> Sunucuya niye katildin? (Herhangi bir sebep olabilir.)\n"
        "Bu sorulari cevaplamak zorundasiniz, <@&1336209216809205822> seninle ozenle ilgilenecektir."
    )
    return welcome

def shorten_url(long_url):
    session = requests.Session()

    main_page = session.get("https://dar.vin/")
    soup = BeautifulSoup(main_page.text, "html.parser")
    
    csrf_meta = soup.find("meta", {"name": "csrf-token"})
    if not csrf_meta:
        return "[warn]: CSRF"

    csrf_token = csrf_meta["content"]

    data = {
        "link-url": long_url,
        "_token": csrf_token,
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://dar.vin/"
    }

    response = session.post("https://dar.vin/shorten", data=data, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        short_url_input = soup.find("input", {"class": "result-box"})
        if short_url_input:
            return short_url_input["value"]
        return "[warn]. url bulamadim galiba bilmiyom"
    return f"[warn]: {response.status_code} - {response.text}"
