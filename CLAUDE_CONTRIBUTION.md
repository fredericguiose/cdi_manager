# CLAUDE_CONTRIBUTION.md

> **Instruction pour toute IA intervenant sur ce projet :**
> À chaque intervention (création de fichier, modification de logique, ajout de fonctionnalité, correction de bug, refactoring...), tu dois ajouter une entrée dans la section **Journal des contributions** ci-dessous. Format : date ISO, modèle IA, rôle clair, fichiers touchés, description concise de ce qui a été fait et pourquoi.

---

## Architecture du projet

**Nom :** CDI Manager
**Objectif :** Gérer les emprunts de livres par des élèves du primaire (projet NSI lycée 1ère année).
**Stack :** Python 3.14, Flask, fichiers CSV comme base de données, frontend HTML statique.
**Gestionnaire de dépendances :** Poetry

### Structure des dossiers

```
cdi_manager/
├── backend/
│   ├── main.py          # Point d'entrée Flask (vide pour l'instant)
│   └── utils.py         # Fonctions utilitaires : validation et conversion de types
├── data/
│   ├── models.py        # Couche d'accès aux données (CRUD sur CSV) : _create, _update, _delete, _get
│   ├── schemas.py       # Définition des schémas de données (ELEVES, LIVRES, EMPRUNTS)
│   ├── eleves.csv       # Données des élèves
│   ├── livres.csv       # Données des livres
│   └── emprunts.csv     # Données des emprunts
├── frontend/
│   ├── index.html       # Page principale (vide pour l'instant)
│   └── add_eleve.html   # Page ajout élève (vide pour l'instant)
├── tests/
│   ├── test_models.py   # Tests unitaires sur la couche models
│   └── data/
│       └── get_eleves.csv  # Données de test pour _get
├── .env                 # Variables d'environnement (non versionné)
├── .env.example         # Template des variables d'environnement
├── OBJECTIF.MD          # Cahier des charges initial
├── pyproject.toml       # Configuration Poetry + dépendances
└── poetry.lock          # Lockfile des dépendances
```

### Schémas de données (`data/schemas.py`)

| Entité   | Champs                                                                                                                                           |
| -------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| ELEVES   | `id` (int), `first_name` (str), `last_name` (str), `age` (int), `grade` (str), `image_url` (str)                                                 |
| LIVRES   | `ibm` (str), `title` (str), `author` (str), `year_published` (int), `image_url` (str), `description` (str), `category_id` (int), `status` (bool) |
| EMPRUNTS | `id` (int), `eleve_id` (int), `book_id` (int), `status` (bool)                                                                                   |

### Règles métier (OBJECTIF.MD)

- Un élève ne peut emprunter qu'**un seul livre** à la fois.
- Les emprunts sont tracés avec un champ `est_rendu` (mappé sur `status`).

### Couche `data/models.py`

Fonctions CRUD génériques opérant sur des fichiers CSV via `csv.DictReader` / `csv.DictWriter` :

- `_get(model, structure, query, primary_key)` — lecture filtrée, implémentée
- `_create(model, structure)` — squelette déclaré, non implémenté
- `_update(model, structure, query)` — squelette déclaré, non implémenté
- `_delete(model, structure, query, all)` — implémentation partielle (logique de filtrage incomplète)

### Couche `backend/utils.py`

- `is_structured(data, structure)` — vérifie qu'un dict correspond à un schéma (clés + types)
- `convert_to_type(value, expected_type)` — convertit une chaîne CSV en type Python (`int`, `float`, `bool`, `str`)
- `convert_row_to_type(row, structure)` — applique `convert_to_type` à chaque champ d'une ligne CSV

---

## Journal des contributions

### 2026-05-27 — Claude Sonnet 4.6 (Anthropic)

**Rôle :** Analyse du projet et initialisation du fichier de suivi des contributions

**Fichiers créés :**

- `CLAUDE_CONTRIBUTION.md` (ce fichier)

**Description :**
Première intervention sur le projet. Lecture complète de la codebase pour cartographier l'architecture existante : schémas de données, couche models (CRUD CSV), utilitaires de conversion, tests unitaires, frontend HTML, configuration Poetry. Création de ce fichier de traçabilité à la demande du propriétaire du projet afin que toutes les IA intervenant ultérieurement documentent leurs contributions de manière claire et structurée.

**Aucun code modifié lors de cette intervention.**

---

### 2026-05-27 — Claude Sonnet 4.6 (Anthropic)

**Rôle :** Configuration de l'environnement de développement VS Code — indentation Python

**Fichiers modifiés :**
- `.vscode/settings.json`

**Description :**
Correction de l'indentation Python forcée à 2 espaces par Prettier. Ajout d'un bloc `[python]` dans les settings VS Code pour surcharger Prettier : `tabSize: 4`, `insertSpaces: true`, et `defaultFormatter` pointant sur `ms-python.python`. Prettier reste actif sur les autres types de fichiers (HTML, JSON, etc.). Conforme à la PEP 8 (4 espaces).

---

### 2026-05-27 — Claude Sonnet 4.6 (Anthropic)

**Rôle :** Correction de l'indentation Python via `.editorconfig` et `.prettierignore`

**Fichiers créés :**
- `.editorconfig`
- `.prettierignore`

**Description :**
La correction via `settings.json` était insuffisante : les logs Prettier montraient qu'il cherchait un `.editorconfig` local et n'en trouvait pas (`inferredParser: null` pour Python). Création d'un `.editorconfig` avec indentation 4 espaces pour `*.py` (2 espaces par défaut pour les autres fichiers). Création d'un `.prettierignore` excluant `*.py` car Prettier n'a pas de parser Python natif.

---

### 2026-05-27 — Claude Sonnet 4.6 (Anthropic)

**Rôle :** Rédaction du README (FR + EN)

**Fichiers modifiés / créés :**
- `README.md`
- `README_EN.md`

**Description :**
Réécriture du README à la demande de l'auteur. Présentation de l'objectif du projet (gestion d'emprunts NSI Première), de la stack (Flask, HTML/CSS/JS, CSV, Poetry), du périmètre du devoir NSI (`data/`, `cli/`, `tests/`) vs bonus (API + frontend). Ajout des commandes pour lancer les tests, le CLI, l'API et Docker (compose prod/dev). Version anglaise créée en parallèle (`README_EN.md`).

---

### 2026-05-27 — Claude Haiku 4.5 (Anthropic)

**Rôle :** Modification des fichiers `__main__.py` pour utiliser une lambda

**Fichiers modifiés :**
- `tests/__main__.py`
- `tests/api/__main__.py`
- `tests/cli/__main__.py`
- `tests/data/__main__.py`

**Description :**
Remplacement du contenu de tous les fichiers `__main__.py` du dossier `tests`. Utilisation d'une lambda pour encapsuler l'appel à `_run()` avec `pathlib.Path(__file__).parent`. L'import `run` a été renommé en `_run` pour éviter les conflits, et une lambda `run` a été créée pour fournir une interface simple : `run = lambda: _run(pathlib.Path(__file__).parent)`.

---

### 2026-05-27 — Claude Opus 4.7 (Anthropic)

**Rôle :** Correction d'une récursion infinie — propagation du pattern lambda à tous les sous-dossiers de tests

**Fichiers modifiés :**
- `tests/api/routes/__main__.py`
- `tests/cli/managers/__main__.py`
- `tests/cli/managers/books/__main__.py`
- `tests/cli/managers/loans/__main__.py`
- `tests/cli/managers/students/__main__.py`
- `tests/data/books/__main__.py`
- `tests/data/loans/__main__.py`
- `tests/data/students/__main__.py`

**Description :**
Lors de la précédente intervention, seuls les 4 `__main__.py` de premier niveau (`tests/`, `tests/api/`, `tests/cli/`, `tests/data/`) avaient été modifiés. Les 8 `__main__.py` des sous-dossiers (`routes/`, `managers/`, `books/`, `loans/`, `students/`) conservaient l'ancien code `from tests import run; run()`. Quand `tests/__init__.py:run()` les importait et appelait `module.run()`, ces fichiers exécutaient `run()` **sans argument**, ce qui retombait sur la valeur par défaut `target=pathlib.Path(__file__).parent` (pointant vers `tests/`) — provoquant une boucle de récursion infinie (`RecursionError`). Tous les sous-dossiers utilisent désormais le même pattern lambda passant explicitement le chemin courant.

---

### 2026-05-27 — Claude Haiku 4.5 (Anthropic)

**Rôle :** Code review et conseils d'amélioration — `data/utils/types.py`

**Fichiers analysés :**
- `data/utils/types.py`

**Description :**
Revue du fichier utilitaire `types.py` pour vérifier la qualité du code (note : 6/10 initial). Identification de plusieurs problèmes : logique cassée ligne 35 (`None and print()` n'exécute jamais le print), indentation incohérente, détection incomplète des entiers négatifs, typos systématiques (`schem` au lieu de `schema`). Fourniture de conseils adaptés aux contraintes NSI (interdiction d'utiliser `raise` pour les exceptions). Suggestion d'utiliser `print() or None` sur une seule ligne pour combiner affichage et retour de `None`, où `or` agit comme un "et logique" exécutant les deux conditions séquentiellement avant de retourner `None`.

---

### 2026-05-27 — Claude Haiku 4.5 (Anthropic)

**Rôle :** Correction des imports relatifs dans `data/db.py`

**Fichiers modifiés :**
- `data/db.py`

**Description :**
Correction des imports Python qui échouaient avec `python -m tests.data.test_db`. Passage des imports absolus (`from utils.types` et `from schemas`) aux imports relatifs (`from .utils.types` et `from .schemas`) pour que le module soit importable peu importe le contexte d'exécution. Les imports relatifs avec `.` indiquent "dans le même package" et fonctionnent correctement avec `-m`.

---

### 2026-05-28 — Claude Sonnet 4.6 (Anthropic)

**Rôle :** Ajout de la fonction factory `make_db` dans `data/db.py`

**Fichiers modifiés :**
- `data/db.py`

**Description :**
Ajout de `make_db(schema_name, schemas_path)` en bas de `db.py`. Cette factory retourne un tuple `(get, create, delete, update)` dont chaque fonction est liée par closure au `schema_name` et `schemas_path` fournis. Permet de créer une abstraction par schéma en une ligne (`get, create, delete, update = make_db("STUDENTS")`), sans dupliquer de logique. La factory corrige aussi le piège de l'argument mutable par défaut en utilisant `query=None` suivi de `query or {}`.

---

### 2026-05-28 — Claude Sonnet 4.6 (Anthropic)

**Rôle :** Correction de 5 bugs critiques dans `data/db.py` et écriture des tests CRUD dans `tests/data/test_db.py`

**Fichiers modifiés :**
- `data/db.py`
- `tests/data/test_db.py`
- `tests/data/_schemas_test_db/students.csv`

**Description :**
Correction de 5 bugs qui empêchaient toute exécution des fonctions CRUD : (1) `dict.keys()[0]` ne supporte pas l'indexation en Python 3, remplacé par `list(...)[0]` dans `_create` et `_get_with_primary` ; (2) `_get_with_primary` n'avait pas de paramètre `primary_key_value` et utilisait `primary_key[0]`/`primary_key[1]` (indexation de string au lieu d'accès dict) ; (3) `_delete` et `_update` passaient `None` comme query à `_get` au lieu d'utiliser les keyword args ; (4) `_get_with_query` comparait des valeurs typées avec des strings CSV brutes, corrigé avec `str(value)` ; (5) `_entry_exist` n'acceptait pas `schemas_path`. Refactoring du cache : `_cache.pop(schema_name, None)` sur mutation plutôt que mise à jour sélective. Ajout d'un second étudiant dans le CSV de test. Écriture de 12 tests couvrant GET (all, query, primary key), CREATE (un, plusieurs, doublon ignoré), DELETE (match, no match), UPDATE (match, no match) — tous passent.
