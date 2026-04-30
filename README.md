<div align="center">
    <img src="doc/images/logo.png" alt="banner">
    <p><em>Add japanese parts of speech to your cards!</em></p>
<p>

[![AnkiWeb](https://img.shields.io/badge/AnkiWeb-Download-blue?logo=anki)](#)
[![License](https://img.shields.io/badge/license-MIT-green?logo=open-source-initiative)](LICENSE)
[![Ko-fi](https://img.shields.io/badge/Ko--fi-Support-red?logo=ko-fi)](https://ko-fi.com/codec266)
[![JMdict](https://img.shields.io/badge/JMdict-EDRDG-blue?logo=sqlite)](https://www.edrdg.org/jmdict/j_jmdict.html)</p>
</div>

## 📝 Description

**Japanese Part of Speech** is an offline Anki add-on that fetches and assigns Japanese parts of speech to your cards. It uses a bundled SQLite database built from JMdict, allowing it to function entirely locally without external API calls.

## 🚀 Usage

### 1. Initial Setup (Field Mapping)
The first time you use the add-on on a new Note Type, it needs to know which fields to use.
* By default, it looks for fields named `Expression`, `Kana Reading`, and `Part of Speech`.
* If your fields are named differently, a dialog box will appear prompting you to map them. 
* These settings are saved automatically, so you only have to do this once per Note Type.

### 2. Updating a Single Note
* Open the Anki Editor (either by clicking **Add** from the main window or editing a note in the **Browser**).
* Enter your target word into your expression field.
* Click the `品` button in the editor toolbar. 
* The add-on will read the word and reading, fetch the data, and populate the part of speech field instantly.

### 3. Bulk Operations
To process multiple notes or manage the add-on, click **Tools** > **Part of Speech** in the main Anki window. You have the following options:
* **bulk add:** Automatically fetch and populate missing part of speech data for all notes in a selected deck and note type.
* **bulk remove:** Clear the part of speech field from a specific deck and note type.
* **find empty:** Opens the Anki Browser with a pre-configured search query to show all notes missing part of speech data.
* **reset mappings:** Clears your saved field configurations if you modify your note types or made a mistake during setup.

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

## 🛠️ Development
The add-on relies on a pre-built `jmdict.db` SQLite database.

To rebuild or update the database locally:
1. Download `JMdict_e.gz` from [EDRDG](https://www.edrdg.org/jmdict/j_jmdict.html) and extract it.
2. After extracting `JMdict_e`, add a `.xml` file extension by renaming it.
3. Place the file inside the same directory as the [jmdict_parse.py](tools/jmdict_parse.py) script.
4. Run the build script.

## ☕ Support
If you found this helpful, you can support me here:

<a href="https://ko-fi.com/codec266">
  <img src="https://cdn.prod.website-files.com/5c14e387dab576fe667689cf/670f5a01cf2da94a032117b9_support_me_on_kofi_red.png" height="40" alt="Support me on Ko-fi">
</a>

## ⚖️ License & Acknowledgements

### MIT License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for full details.

### JMdict (EDRDG)
This add-on uses the JMdict dictionary file. These files are the property of the Electronic Dictionary Research and Development Group, and are used in conformance with the Group's licence.

> **ELECTRONIC DICTIONARY RESEARCH AND DEVELOPMENT GROUP**
> **GENERAL DICTIONARY LICENCE STATEMENT**
> 
> This dictionary file is the property of the Electronic Dictionary Research and Development Group (EDRDG), and is used in conformance with the Group's [licence](https://www.edrdg.org/edrdg/licence.html).