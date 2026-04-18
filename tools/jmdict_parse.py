import xml.etree.ElementTree as ET
import sqlite3
from pathlib import Path
from collections import defaultdict

# configuration
BASE_DIR = Path(__file__).resolve().parent
JM_DICT_PATH = BASE_DIR / "JMdict_e.xml"
OUTPUT_DB = BASE_DIR.parent / "src" / "jmdict.db"

# mappings
POS_MAP = {
    "'ku' adjective (archaic)": ("Adjective", ["い", "archaic"]),
    "'shiku' adjective (archaic)": ("Adjective", ["い", "archaic"]),
    "'taru' adjective": ("Adjective", ["たる"]),
    "Godan verb - -aru special class": ("Verb", ["5-dan", "ある"]),
    "Godan verb - Iku/Yuku special class": ("Verb", ["5-dan", "いく/ゆく"]),
    "Godan verb with 'bu' ending": ("Verb", ["5-dan", "ぶ"]),
    "Godan verb with 'gu' ending": ("Verb", ["5-dan", "ぐ"]),
    "Godan verb with 'ku' ending": ("Verb", ["5-dan", "く"]),
    "Godan verb with 'mu' ending": ("Verb", ["5-dan", "む"]),
    "Godan verb with 'nu' ending": ("Verb", ["5-dan", "ぬ"]),
    "Godan verb with 'ru' ending": ("Verb", ["5-dan", "る"]),
    "Godan verb with 'ru' ending (irregular verb)": ("Verb", ["5-dan", "る", "irregular"]),
    "Godan verb with 'su' ending": ("Verb", ["5-dan", "す"]),
    "Godan verb with 'tsu' ending": ("Verb", ["5-dan", "つ"]),
    "Godan verb with 'u' ending": ("Verb", ["5-dan", "う"]),
    "Godan verb with 'u' ending (special class)": ("Verb", ["5-dan", "う", "special"]),
    "Ichidan verb": ("Verb", ["1-dan"]),
    "Ichidan verb - kureru special class": ("Verb", ["1-dan", "くれる"]),
    "Ichidan verb - zuru verb (alternative form of -jiru verbs)": ("Verb", ["1-dan", "ずる"]),
    "Kuru verb - special class": ("Verb", ["来る"]),
    "Nidan verb (lower class) with 'dzu' ending (archaic)": ("Verb", ["2-dan", "archaic"]),
    "Nidan verb (lower class) with 'gu' ending (archaic)": ("Verb", ["2-dan", "archaic"]),
    "Nidan verb (lower class) with 'hu/fu' ending (archaic)": ("Verb", ["2-dan", "archaic"]),
    "Nidan verb (lower class) with 'ku' ending (archaic)": ("Verb", ["2-dan", "archaic"]),
    "Nidan verb (lower class) with 'mu' ending (archaic)": ("Verb", ["2-dan", "archaic"]),
    "Nidan verb (lower class) with 'nu' ending (archaic)": ("Verb", ["2-dan", "archaic"]),
    "Nidan verb (lower class) with 'ru' ending (archaic)": ("Verb", ["2-dan", "archaic"]),
    "Nidan verb (lower class) with 'su' ending (archaic)": ("Verb", ["2-dan", "archaic"]),
    "Nidan verb (lower class) with 'tsu' ending (archaic)": ("Verb", ["2-dan", "archaic"]),
    "Nidan verb (lower class) with 'u' ending and 'we conjugation (archaic)": ("Verb", ["2-dan", "archaic"]),
    "Nidan verb (lower class) with 'yu' ending (archaic)": ("Verb", ["2-dan", "archaic"]),
    "Nidan verb (lower class) with 'zu' ending (archaic)": ("Verb", ["2-dan", "archaic"]),
    "Nidan verb (upper class) with 'bu' ending (archaic)": ("Verb", ["2-dan", "archaic"]),
    "Nidan verb (upper class) with 'gu' ending (archaic)": ("Verb", ["2-dan", "archaic"]),
    "Nidan verb (upper class) with 'hu/fu' ending (archaic)": ("Verb", ["2-dan", "archaic"]),
    "Nidan verb (upper class) with 'ku' ending (archaic)": ("Verb", ["2-dan", "archaic"]),
    "Nidan verb (upper class) with 'ru' ending (archaic)": ("Verb", ["2-dan", "archaic"]),
    "Nidan verb (upper class) with 'tsu' ending (archaic)": ("Verb", ["2-dan", "archaic"]),
    "Nidan verb (upper class) with 'yu' ending (archaic)": ("Verb", ["2-dan", "archaic"]),
    "Nidan verb with 'u' ending (archaic)": ("Verb", ["2-dan", "archaic"]),
    "Yodan verb with 'bu' ending (archaic)": ("Verb", ["4-dan", "ぶ", "archaic"]),
    "Yodan verb with 'gu' ending (archaic)": ("Verb", ["4-dan", "ぐ", "archaic"]),
    "Yodan verb with 'hu/fu' ending (archaic)": ("Verb", ["4-dan", "ふ", "archaic"]),
    "Yodan verb with 'ku' ending (archaic)": ("Verb", ["4-dan", "く", "archaic"]),
    "Yodan verb with 'mu' ending (archaic)": ("Verb", ["4-dan", "む", "archaic"]),
    "Yodan verb with 'ru' ending (archaic)": ("Verb", ["4-dan", "る", "archaic"]),
    "Yodan verb with 'su' ending (archaic)": ("Verb", ["4-dan", "す", "archaic"]),
    "Yodan verb with 'tsu' ending (archaic)": ("Verb", ["4-dan", "つ", "archaic"]),
    "adjectival nouns or quasi-adjectives (keiyodoshi)": ("Adjective", ["な"]),
    "adjective (keiyoushi)": ("Adjective", ["い"]),
    "adjective (keiyoushi) - yoi/ii class": ("Adjective", ["い", "よい/いい"]),
    "adverb (fukushi)": ("Adverb", []),
    "adverb taking the 'to' particle": ("Adverb", []),
    "archaic/formal form of na-adjective": ("Adjective", ["な", "archaic"]),
    "auxiliary": ("Auxiliary", []),
    "auxiliary adjective": ("Auxiliary Adjective", []),
    "auxiliary verb": ("Auxiliary", []),
    "conjunction": ("Conjunction", []),
    "copula": ("Copula", []),
    "counter": ("Counter", []),
    "expressions (phrases, clauses, etc.)": ("Expression", []),
    "interjection (kandoushi)": ("Interjection", []),
    "intransitive verb": ("Verb", ["intransitive"]),
    "irregular nu verb": ("Verb", ["irregular nu"]),
    "irregular ru verb, plain form ends with -ri": ("Verb", ["irregular ru"]),
    "noun (common) (futsuumeishi)": ("Noun", []),
    "archaic noun": ("Noun", ["archaic"]),
    "noun or participle which takes the aux. verb suru": ("Verb", ["する"]),
    "noun or verb acting prenominally": ("Noun", ["prenominal"]),
    "noun, used as a prefix": ("Noun", ["prefix"]),
    "noun, used as a suffix": ("Noun", ["suffix"]),
    "nouns which may take the genitive case particle 'no'": ("Noun", []),
    "numeric": ("Numeric", []),
    "particle": ("Particle", []),
    "pre-noun adjectival (rentaishi)": ("Adjective", ["の"]),
    "prefix": ("Prefix", []),
    "pronoun": ("Pronoun", []),
    "su verb - precursor to the modern suru": ("Verb", ["する", "archaic"]),
    "suffix": ("Suffix", []),
    "suru verb - included": ("Verb", ["する"]),
    "suru verb - special class": ("Verb", ["する", "special"]),
    "transitive verb": ("Verb", ["transitive"]),
    "unclassified": ("Unclassified", []),
    "verb unspecified": ("Verb", [])
}

MISC_MAPPING = {
    "archaic": "Archaic",
    "obsolete": "Archaic",
    "abbreviation": "Abbreviation",
    "rare term": "Obscure",
    "historical term": "Old-fashioned",
    "colloquial": "Colloquial",
    "onomatopoeic": "Onomatopoeic",
    "yojijukugo": "Four character compound",
    "idiomatic expression": "Idiomatic",
    "internet slang": "Internet Slang",
    "manga slang": "Manga slang",
    "slang": "Slang",
    "proverb": "Proverb",
    "sonkeigo": "Honorific",
    "honorific": "Honorific",
    "formal or literary": "Literary",
    "derogatory": "Derogatory",
    "teineigo": "Polite",
    "polite": "Polite",
    "kenjougo": "Humble",
    "humble": "Humble",
    "jocular": "Humorous",
    "vulgar": "Vulgar",
    "sensitive": "Sensitive",
    "poetical": "Poetic",
    "familiar language": "Familiar Language",
    "children's language": "Children's language"
}


def format_pos_string(pos_tags, misc_tags):
    pos_groups = {}
    special_modifiers = set()

    for p in pos_tags:
        if p not in POS_MAP: continue
        base_pos, attrs = POS_MAP[p]

        clean_attrs = []
        for attr in attrs:
            if attr == "archaic":
                special_modifiers.add("Archaic")
            elif attr == "suffix":
                if "Suffix" not in pos_groups: pos_groups["Suffix"] = set()
            elif attr == "prefix":
                if "Prefix" not in pos_groups: pos_groups["Prefix"] = set()
            else:
                clean_attrs.append(attr)

        if base_pos not in pos_groups: pos_groups[base_pos] = set()
        pos_groups[base_pos].update(clean_attrs)

    for m in misc_tags:
        m_lower = m.lower()
        for key, label in MISC_MAPPING.items():
            if key in m_lower:
                special_modifiers.add(label)
                break

    formatted_parts = []

    if "Archaic" in special_modifiers:
        formatted_parts.append("Archaic")
        special_modifiers.remove("Archaic")

    for base_pos in sorted(pos_groups.keys()):
        attrs = pos_groups[base_pos]

        if "する" in attrs:
            if "transitive" in attrs and "intransitive" in attrs:
                attrs.discard("transitive")
                attrs.discard("intransitive")

        if attrs:
            def attr_weight(x):
                if "dan" in x or x in ["irregular nu", "irregular ru", "する", "来る", "い", "な", "の", "たる"]:
                    return 1
                elif x in ["ぶ", "ぐ", "く", "む", "ぬ", "る", "す", "つ", "う", "ふ", "いく/ゆく", "ある", "くれる",
                           "ずる"]:
                    return 2
                elif x in ["transitive", "intransitive"]:
                    return 3
                return 4

            sorted_attrs = sorted(list(attrs), key=lambda x: (attr_weight(x), x))
            formatted_parts.append(f"{base_pos} ({', '.join(sorted_attrs)})")
        else:
            formatted_parts.append(base_pos)

    if special_modifiers:
        formatted_parts.extend(sorted(special_modifiers))

    return ", ".join(formatted_parts)


def build_db():
    if not JM_DICT_PATH.exists():
        print(f"Error: Could not find {JM_DICT_PATH}")
        return

    print("Parsing dictionary and flattening entries...")
    # use a tuple (word, reading) as the key
    word_data = defaultdict(lambda: {"pos": set(), "misc": set()})
    tree = ET.parse(JM_DICT_PATH)

    for entry in tree.getroot().findall("entry"):
        kanji_list = [k.find("keb").text for k in entry.findall("k_ele") if k.find("keb") is not None]
        kana_nodes = entry.findall("r_ele")

        pos_set = {p.text for s in entry.findall("sense") for p in s.findall("pos") if p.text}
        misc_set = {m.text for s in entry.findall("sense") for m in s.findall("misc") if m.text}

        pairs = set()

        if kanji_list:
            for r_node in kana_nodes:
                reb = r_node.find("reb").text
                restr_nodes = r_node.findall("re_restr")

                if restr_nodes:
                    for restr in restr_nodes:
                        if restr.text in kanji_list:
                            pairs.add((restr.text, reb))
                else:
                    for k in kanji_list:
                        pairs.add((k, reb))

                # Modified section
                has_uk = any("usually written using kana alone" in m.lower() or m.lower() == "uk" for m in misc_set)
                if has_uk:
                    pairs.add((reb, reb))

        else:
            for r_node in kana_nodes:
                reb = r_node.find("reb").text
                pairs.add((reb, reb))

        for w, r in pairs:
            word_data[(w, r)]["pos"].update(pos_set)
            word_data[(w, r)]["misc"].update(misc_set)

    conn = sqlite3.connect(OUTPUT_DB)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS entries")
    cursor.execute("CREATE TABLE entries (word TEXT, reading TEXT, formatted_pos TEXT)")

    batch = []
    for (word, reading), tags in word_data.items():
        formatted = format_pos_string(tags["pos"], tags["misc"])
        if formatted:
            batch.append((word, reading, formatted))

    cursor.executemany("INSERT INTO entries VALUES (?, ?, ?)", batch)

    cursor.execute("CREATE INDEX idx_word_reading ON entries (word, reading)")
    cursor.execute("CREATE INDEX idx_word ON entries (word)")

    conn.commit()
    conn.close()
    print("Done")


if __name__ == "__main__":
    build_db()