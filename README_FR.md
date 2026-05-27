# CDI Manager

Plateforme de gestion des emprunts de livres pour une école primaire. Projet réalisé dans le cadre du devoir de NSI (Première).

L'application permet de gérer les élèves, les livres et les emprunts — un élève ne peut emprunter qu'un seul livre à la fois.

## Périmètre du devoir NSI

La partie évaluée concerne principalement :

- `data/` — modèles et accès aux données (CSV)
- `cli/` — interface en ligne de commande
- `tests/data/` et `tests/cli/` — tests associés

Le reste (API Flask, frontend HTML/CSS/JS) est du bonus et reflète un intérêt personnel de l'auteur. L'examinateur est libre d'y jeter un œil.

## Stack technique

- **Backend** : Python 3.14, Flask
- **Frontend** : HTML, CSS, JavaScript
- **Données** : fichiers CSV
- **Dépendances** : Poetry

## Lancer le projet

### Prérequis

```bash
poetry install
```

### Tests

```bash
poetry run pytest tests/data/
poetry run pytest tests/cli/
# Tous les tests
poetry run pytest
```

### CLI

```bash
poetry run python -m cli
```

### API + Frontend

```bash
poetry run flask --app backend/main.py run
```

### Docker

```bash
# Production
docker compose -f docker-compose.prod.yml up -d

# Développement
docker compose -f docker-compose.dev.yml up -d
```
