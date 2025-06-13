import pandas as pd
import re
import emoji
import unicodedata
from typing import Dict, List

def normalize_unicode(text: str) -> str:
    """Normalize unicode characters to ASCII."""
    return unicodedata.normalize('NFKD', str(text)).encode('ascii', 'ignore').decode('utf-8')

def clean_text(text: str) -> str:
    """Clean text by removing unwanted characters and normalizing format."""
    text = text.lower()
    text = emoji.demojize(text)
    transformations = [
        (r':[a-zA-Z_]+:', ' '),      # Remove emoji names
        (r'http\S+', ''),             # Remove URLs
        (r'@\w+|#\w+', ''),          # Remove mentions and hashtags
        (r'[^\w\s]', ' '),           # Remove symbols, keep alphanumeric
        (r'\b\d+\b', ' '),           # Remove standalone numbers
        (r'\s+', ' '),               # Remove extra spaces
        (r'(\w)\1{2,}', r'\1'),      # Normalize repeated characters (aaa -> a)
        (r'(\w+)(\1{1,})$', r'\1')   # Normalize repeated words (gasss -> gas)
    ]

    for pattern, replacement in transformations:
        text = re.sub(pattern, replacement, text)
    return text.strip()

def join_spaced_letters(text: str) -> str:
    """Join spaced letters (e.g., p r o m o -> promo)."""
    pattern = r'\b(?:[a-zA-Z]\s){2,}[a-zA-Z]\b'
    for match in re.findall(pattern, text):
        text = text.replace(match, match.replace(' ', ''))
    return text

def load_slang_dictionary() -> Dict[str, str]:
    slang_dict_manual = {
        "gk": "tidak", "gak": "tidak", "g": "tidak", "tdk": "tidak", "ga": "tidak",
        "nggak": "tidak", "enggak": "tidak", "gpp": "tidak apa-apa",
        "gakpapa": "tidak apa-apa", "tp": "tapi", "tapi": "tetapi",
        "kl": "kalau", "klw": "kalau", "kalo": "kalau", "klo": "kalau",
        "krn": "karena", "karena": "sebab", "jd": "jadi", "sdh": "sudah",
        "udh": "sudah", "udah": "sudah", "dl": "dulu",
        "sm": "sama", "sama": "dengan", "dg": "dengan", "dr": "dari",
        "utk": "untuk", "yg": "yang", "jg": "juga", "d": "di",
        "dll": "dan lain-lain", "dst": "dan seterusnya", "ttp": "tetap",
        "tsb": "tersebut", "dlm": "dalam", "pdhl": "padahal",
        "mrk": "mereka", "sy": "saya", "gw": "saya", "gue": "saya",
        "gua": "saya", "w": "saya", "gwe": "saya", "km": "kamu",
        "lu": "kamu", "lo": "kamu", "q": "aku", "ak": "aku",
        "aq": "aku", "elo": "kamu", "elu": "kamu", "loe": "kamu",
        "mnrt": "menurut", "spt": "seperti", "bener": "benar", "kok": "mengapa",
        "lg": "lagi", "bgt": "banget", "banget": "sekali", "cm": "cuma",
        "cuman": "cuma", "emg": "memang", "emng": "memang",
        "bs": "bisa", "bsa": "bisa", "sabi": "bisa",
        "bikin": "membuat", "ksih": "kasih", "ksh": "kasih",
        "jgn": "jangan", "jngn": "jangan",
        "biar": "agar", "supaya": "agar",
        "anjay": "astaga", "anjir": "astaga", "anjrit": "astaga",
        "wkwk": "haha", "wkwkwk": "haha", "wk": "haha", "lol": "haha",
        "ngakak": "tertawa", "santuy": "santai", "woles": "santai", "mager": "malas",
        "gabut": "tidak ada kerjaan", "baper": "terbawa perasaan",
        "kepo": "penasaran", "julid": "iri", "gibah": "bergosip",
        "panik": "takut", "cape": "capek", "capekkk": "capek",
        "pusinggg": "pusing", "skuy": "ayo", "gas": "ayo", "gaskeun": "ayo",
        "mantul": "bagus", "uhuy": "mantap", "mantab": "mantap",
        "kocak": "lucu", "ngeri": "hebat", "goks": "hebat",
        "pecah": "seru", "smg": "semoga",
        "receh": "tidak penting", "lebay": "berlebihan", "php": "pemberi harapan palsu",
        "auto": "langsung", "halu": "berkhayal",
        "ngab": "teman", "cuy": "teman", "ngabers": "remaja pria",
        "bro": "saudara", "sis": "kakak", "tmn": "teman",
        "tmn2": "teman-teman", "bocil": "anak kecil", "org": "orang",
        "bang": "kakak", "bg": "kakak", "bng": "kakak", "kak": "kakak",
        "min": "minimal", "jp": "jackpot", "jepe": "jackpot", "jepey": "jackpot",
        "bonus": "hadiah", "depo": "deposit", "wd": "withdraw",
        "bet": "banget", "gmpng": "mudah", "gampang": "mudah",
        "win": "menang", "betting": "taruhan",
        "slot": "permainan judi", "event": "acara", "promo": "promosi",
        "gacr": "gacor", "gcr": "gacor",
        "mekswin": "maxwin", "gacir": "gacor", "y": "ya", "kn": "kan", "cs" : "dan kawan kawan",
        "dri": "dari", "msk": "masuk", "thn": "tahun", "th": "tahun", "korup": "korupsi",
        "ortu": "orang tua", "jekpot": "jackpot", "ny": "nya", "mmg": "memang", "klihatan": "terlihat",
        "keliatan": "terlihat", "demen": "suka", "kayak": "seperti", "dah": "sudah", "knp": "kenapa",
        "wtf": "astaga", "sosmed": "sosial media", "gaspol": "ayo", "maen": "main",
        "judol": "judi online", "smpe": "sampai", "sampe": "sampai", "nyampe": "sampai",
        "pinjol": "pinjaman online", "ntar": "nanti", "nnti": "nanti", "nti": "nanti",
        "gini": "seperti ini", "gni": "seperti ini", "begini": "seperti ini", "bpk": "bapak",
        "bp": "bapak", "tilep": "mengambil", "mirip": "seperti", "mrp": "seperti", "drpd": "daripada",
        "thdp": "terhadap", "jga": "juga", "mngkin": "mungkin", "ap": "apa", "bkl": "akan",
        "bakal": "akan", "mna": "dimana", "mn": "dimana", "mana": "dimana", "cilik": "kecil",
        "pny": "punya", "wong": "orang", "msh": "masih", "sj": "saja", "pk": "bapak", "dn": "dan",
        "plis": "tolong", "hati2": "hati hati", "tlpn": "telepon", "tlp": "telepon",
        "ngakak": "tertawa", "jir": "astaga"
    }
    try:
        slang_df = pd.read_csv("hf://datasets/theonlydo/indonesia-slang/slang-indo.csv")
        slang_dict_hf = slang_df.set_index('slang')['formal'].to_dict()
        return {**slang_dict_hf, **slang_dict_manual}
    except Exception as e:
        print(f"Error loading slang dictionary: {e}")
        return slang_dict_manual

def replace_slang(text: str, slang_dict: Dict[str, str]) -> str:
    return " ".join(slang_dict.get(word, word) for word in text.split())
