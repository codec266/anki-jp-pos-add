<div align="center">
    <img src="doc/images/logo.png">
    <p><em>Add japanese parts of speech to your cards!</em></p>
<p>

[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![JMdict](https://img.shields.io/badge/JMdict-EDRDG-blue)](https://www.edrdg.org/jmdict/j_jmdict.html)
</p>
</div>

## 📝 Description

**Japanese Part of Speech** is an offline Anki add-on that fetches and assigns Japanese parts of speech to your cards. It uses a bundled SQLite database built from JMdict, allowing it to function entirely locally without external API calls.

## 🏷️ Part of Speech Formatting

**Examples of data mapping:**

| Raw JMdict Part of Speech | Formatted Output |
| :--- | :--- |
| Godan verb with 'ku' ending <br> *+ transitive verb* | **Verb (5-dan, く, transitive)** |
| adjectival nouns or quasi-adjectives (keiyodoshi) <br> *+ slang* | **Adjective (な), Slang** |
| noun or participle which takes the aux. verb suru <br> *+ sonkeigo* | **Verb (する), Honorific** |
| Godan verb - Iku/Yuku special class <br> *+ historical term* | **Verb (5-dan, いく/ゆく), Old-fashioned** |
| Yodan verb with 'bu' ending (archaic) | **Archaic, Verb (4-dan, ぶ)** |

### Supported Categories
* **Core POS:** Noun, Verb, Adjective, Adverb, Particle, Copula, Counter, etc.
* **Verb/Adjective Classes:** 1-dan, 5-dan, 4-dan, irregular, suru, い-adj, な-adj, たる-adj.
* **Stylistic/Misc Labels:** Colloquial, Slang, Honorific, Humble, Polite, Obscure, Onomatopoeic, Idiomatic, Vulgar, Internet Slang, and more.