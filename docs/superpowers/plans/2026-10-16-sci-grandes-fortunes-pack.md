# Pack « Statuts SCI Grandes Fortunes » : plan d'implémentation

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ajouter au dépôt un pack tabulaire de 68 colonnes qui extrait des statuts de SCI (PDF hétérogènes) des valeurs normalisées et des extraits littéraux.

**Architecture:** Un pack `sci-grandes-fortunes-pack` contenant un seul workflow tabulaire `statuts-sci-grandes-fortunes` (`SKILL.md` + `table-columns.yaml`). Les colonnes sont ajoutées par familles ; un test `unittest` pilote le contenu du YAML, le validateur du dépôt pilote la conformité de structure.

**Tech Stack:** YAML, Markdown, Python 3 (`unittest`, `yaml`), scripts `workflow-schema/validate-workflows.py` et `workflow-schema/generate-tabular-skills.py`.

**Spec:** `docs/superpowers/specs/2026-10-16-sci-statuts-tabular-review-design.md`

## Global Constraints

- Dossier : `tabular-review-workflows/sci-grandes-fortunes-pack/` ; workflow : `statuts-sci-grandes-fortunes/` (slug ASCII de `mike-display-name: "Statuts SCI Grandes Fortunes"`).
- `pack.yaml` : `id: sci-grandes-fortunes`, `license: MIT`, `version: 1.0.0`, `jurisdiction: FR`, publisher `Relais4x100a2` (`https://github.com/Relais4x100a2`).
- `SKILL.md` : `mike-type: tabular`, `mike-availability: add-on`, `language: French`, `jurisdictions: France`, `license: MIT`.
- Formats autorisés : `text`, `date`, `monetary_amount`, `percentage`, `bulleted_list`, `yes_no`, `tag` (tags uniques, non vides, uniquement sur `tag`). Indices contigus à partir de 0, noms uniques, prompts non vides.
- Tout `tag` inclut « Non précisé » (silence des statuts), ou « Non déterminable » quand la date de référence compte. Exceptions : les colonnes de la famille A (indices 0, 4, 5) et la colonne 22 (exactement `["Oui", "Non", "Non déterminable"]`).
- Colonne 55 : exactement `["Totalement libre", "Soumis à agrément", "Libre selon conditions (descendants ou holding qualifiée)", "Non précisé"]`.
- `yes_no` : « Non » = non trouvé dans le PDF fourni.
- Prompts en français, neutres (aucune mention de « grandes fortunes » ni « milliardaire »), sans numéro d'article de loi, d'arrêt ou de montant écrit de mémoire.
- Le bloc `## Instructions` de `SKILL.md` vient de `workflow-schema/generate-tabular-skills.py` ; les consignes propres au pack sont dans une section distincte placée après.
- Ne jamais lire ni committer `backend/.env` ni des statuts réels. Commit uniquement si l'utilisateur l'a demandé.

## Review Focus

- PDF sans statuts (page de garde, extrait Kbis ou PV seuls) : `Type de PDF` et `Confiance globale` doivent le refléter, aucune valeur déduite.
- Modification ou PV postérieur qui contredit les statuts initiaux : l'acte de référence est le dernier état lisible, et les colonnes portent la valeur à jour.
- Répartition du capital sans date de référence connue : `Non déterminable`, pas un pourcentage supposé.
- Clause ambiguë (agrément, majorité) : valeur la moins interprétative, extrait associé renseigné.
- Scan illisible ou OCR partiel : `Lisibilité du PDF` ≠ « bonne » et confiance abaissée, sans remplissage au hasard.

---

## Table des colonnes (source de vérité pour tous les tests)

Index = n° du spec − 1 jusqu'à 24, puis `24bis` → 24, puis n° du spec pour n ≥ 25. Total : 68. Familles : A 0-5, B 6-15, C 16-26, D 27-33, E 34-44, F 45-48, G 49-53, H 54-62, I 63-67.

| i | Nom | Format |
|---|-----|--------|
| 0 | Type de PDF | tag |
| 1 | Acte de référence retenu | text |
| 2 | Date de l'état à jour | date |
| 3 | Nombre de modifications statutaires repérées | tag |
| 4 | Lisibilité du PDF | tag |
| 5 | Confiance globale | tag |
| 6 | Forme et dénomination | text |
| 7 | Date de constitution | date |
| 8 | Durée de la société | tag |
| 9 | Objet : nature | tag |
| 10 | Objet étendu au-delà de l'immobilier | yes_no |
| 11 | Régime fiscal annoncé | tag |
| 12 | Capital social | monetary_amount |
| 13 | Capital variable | yes_no |
| 14 | Capital variable : extrait | text |
| 15 | Siège : ville | text |
| 16 | Nombre d'associés | tag |
| 17 | Part des personnes morales dans le capital | tag |
| 18 | Holding, SCI ou société associée | yes_no |
| 19 | Fondation, trust ou structure étrangère | yes_no |
| 20 | Associé majoritaire : part du capital | percentage |
| 21 | Associé majoritaire : nature | tag |
| 22 | Plusieurs générations associées | tag |
| 23 | Clause sur les comptes courants d'associés | tag |
| 24 | Compte courant d'associé : extrait | text |
| 25 | Parts à droits particuliers | yes_no |
| 26 | Parts à droits particuliers : extrait | text |
| 27 | Parts démembrées dans l'état à jour | tag |
| 28 | Vote des décisions ordinaires (démembrement) | tag |
| 29 | Vote des décisions extraordinaires (démembrement) | tag |
| 30 | Quasi-usufruit | yes_no |
| 31 | Réversion ou usufruit successif | yes_no |
| 32 | Affectation des réserves et bénéfices exceptionnels | tag |
| 33 | Démembrement : extrait | text |
| 34 | Nombre de gérants | tag |
| 35 | Gérant : nature | tag |
| 36 | Gérant nommé par les statuts | yes_no |
| 37 | Durée du mandat du gérant | tag |
| 38 | Étendue des pouvoirs du gérant | tag |
| 39 | Pouvoirs du gérant : extrait | text |
| 40 | Limites aux pouvoirs (autorisation de tiers) | yes_no |
| 41 | Verrouillage de la révocation | tag |
| 42 | Révocation du gérant : extrait | text |
| 43 | Rémunération du gérant | tag |
| 44 | Désignation du successeur du gérant | tag |
| 45 | Comité de surveillance, directoire ou conseil de famille | yes_no |
| 46 | Censeurs | yes_no |
| 47 | Actes du gérant soumis à autorisation d'un organe | yes_no |
| 48 | Gouvernance : extrait | text |
| 49 | Majorité ordinaire | tag |
| 50 | Majorité de modification des statuts | tag |
| 51 | Voix prépondérante | yes_no |
| 52 | Actes réservés aux associés | yes_no |
| 53 | Consultation écrite admise | yes_no |
| 54 | Agrément requis pour cession à un tiers | yes_no |
| 55 | Agrément intrafamilial et holdings | tag |
| 56 | Majorité d'agrément | tag |
| 57 | Agrément : extrait | text |
| 58 | Droit de préemption | yes_no |
| 59 | Inaliénabilité temporaire | yes_no |
| 60 | Exclusion ou retrait | tag |
| 61 | Rachat forcé ou clause texane | yes_no |
| 62 | Mode de valorisation des parts | tag |
| 63 | Continuation en cas de décès | tag |
| 64 | Agrément des héritiers | tag |
| 65 | Protection du conjoint survivant | yes_no |
| 66 | Mandat posthume | yes_no |
| 67 | Décès : extrait | text |

Valeurs de tags : celles du spec (§ Colonnes) et des contraintes ci-dessus ; pour les autres, le constructeur fixe des libellés courts en français incluant « Non précisé » ou « Non déterminable », par exemple tranches `1 à 2 / 3 à 5 / 6 à 10 / plus de 10 / Non déterminable` pour le nombre d'associés ou de gérants, et `Simple / Renforcée / Unanimité / Non précisé` pour les majorités.

---

### Task 1: Test de structure, pack, SKILL.md et familles A et B

**Files:**
- Create: `tests/test_sci_grandes_fortunes_columns.py`
- Create: `tabular-review-workflows/sci-grandes-fortunes-pack/pack.yaml`
- Create: `tabular-review-workflows/sci-grandes-fortunes-pack/statuts-sci-grandes-fortunes/SKILL.md`
- Create: `tabular-review-workflows/sci-grandes-fortunes-pack/statuts-sci-grandes-fortunes/table-columns.yaml` (indices 0 à 15)

**Interfaces:**
- Produces: `EXPECTED: list[tuple[str, str]]` (nom, format) dans le fichier de test, rempli avec les 68 lignes de la table ci-dessus ; `load_columns() -> list[dict]`, qui lit `table-columns.yaml` ; tests ci-dessous. Les tâches 2 à 4 n'ajoutent que des colonnes au YAML.

- [ ] **Step 1: Créer une branche** `git switch -c feat/sci-grandes-fortunes-pack` (le dépôt est sur `main`).

- [ ] **Step 2: Écrire le test** `tests/test_sci_grandes_fortunes_columns.py` (`unittest`), avec ces méthodes. Les tests de colonnes comparent `columns[i]` à `EXPECTED[i]` pour `i < len(columns)` et vérifient ensuite le reste des règles sur les colonnes déjà présentes (tâches suivantes : le nombre final est testé par `test_final_count`, qui est ignoré tant que le YAML est incomplet : `skipUnless(len(columns) == 68)`) :
  - `test_prefix_matches_expected`: pour chaque colonne présente, `(name, format) == EXPECTED[index]` et `index` contigu depuis 0.
  - `test_extrait_columns_are_text`: tout nom se terminant par « : extrait » a le format `text`.
  - `test_tags_have_fallback`: tout `tag` hors indices {0, 4, 5, 22, 55} contient « Non précisé » ou « Non déterminable » ; la colonne 22 vaut exactement `["Oui", "Non", "Non déterminable"]` ; la colonne 55 vaut exactement la liste des contraintes.
  - `test_prompts_neutral_and_sourced`: aucun prompt ne contient « fortune » ni « milliardaire » (insensible à la casse), et aucun ne correspond à `\b(art\.?|article)\s+[LRD]?\d`.
  - `test_review_focus_wording`: le prompt de l'index 1 contient « PV » et « modification » ; le prompt de l'index 20 contient « Non déterminable » ; le prompt de l'index 5 contient « Lisibilité » ; le prompt de l'index 0 contient « page de garde ».
  - `test_final_count`: `len(columns) == 68`.

- [ ] **Step 3: Lancer** `python3 -m unittest tests.test_sci_grandes_fortunes_columns -v`. Attendu : échec (fichier YAML absent).

- [ ] **Step 4: Créer `pack.yaml`** conformément aux contraintes ci-dessus (`$schema: "../../workflow-schema/pack.schema.yaml"`, `title: "Statuts de SCI : grandes fortunes"`, une description en une phrase mentionnant la recherche personnelle non commerciale, `practice: "Droit des sociétés et patrimoine"`, `workflows: ["statuts-sci-grandes-fortunes"]`).

- [ ] **Step 5: Créer `SKILL.md`** : frontmatter conforme aux contraintes ; titre « Statuts SCI Grandes Fortunes » ; section `## Purpose` (une phrase) ; section `## Instructions` (laissée vide ici, remplie par le générateur) ; puis une section `## Consignes de revue` avec ces règles en puces : valeurs neutres sans présupposé de recherche ; identification des pièces du PDF puis acte de référence = état le plus récent lisible ; pas de pourcentage de capital sans date de référence ; « Non » en `yes_no` = non trouvé dans le PDF ; extrait = citation littérale avec numéro d'article ; en cas d'ambiguïté, valeur la moins interprétative ; sortie à vérifier par un humain, aucune analyse juridique.

- [ ] **Step 6: Écrire `table-columns.yaml` pour les indices 0 à 15** avec `$schema: "../../../workflow-schema/table-columns.schema.yaml"`. Chaque `prompt` est une consigne neutre en français d'une à trois phrases ; les `tags` des colonnes 0, 3, 4, 5, 8, 9, 11 sont fixés par le constructeur selon le spec (famille A et B). Le prompt de l'index 0 mentionne la « page de garde » ; celui de l'index 1 demande de citer l'acte de référence et de mentionner « PV » et « modification » postérieurs ; celui de l'index 5 s'appuie sur la « Lisibilité ».

- [ ] **Step 7: Générer les consignes** `python3 workflow-schema/generate-tabular-skills.py`, puis `python3 workflow-schema/validate-workflows.py`. Attendu : « Validated … » sans erreur (si le slug n'est pas accepté, ajuster le `mike-display-name` ou le dossier jusqu'à correspondance).

- [ ] **Step 8: Relancer le test** `python3 -m unittest tests.test_sci_grandes_fortunes_columns -v`. Attendu : PASS (hors `test_final_count`, ignoré).

### Task 2: Famille C, capital et associés (indices 16 à 26)

**Files:**
- Modify: `tabular-review-workflows/sci-grandes-fortunes-pack/statuts-sci-grandes-fortunes/table-columns.yaml`

**Interfaces:**
- Consumes: la table des colonnes ; `EXPECTED` du test.
- Produces: colonnes 16 à 26.

- [ ] **Step 1: Lancer le test** : attendu, `test_prefix_matches_expected` échoue pour les indices manquants une fois la colonne 16 attendue (ajoutez au besoin une vérification que `len(columns) >= 27` via un test `test_family_c` de la forme `assertGreaterEqual(len(columns), 27)`).
- [ ] **Step 2: Ajouter les colonnes 16 à 26.** Contraintes spécifiques : la colonne 20 (`percentage`) dit de répondre « Non déterminable » si la répartition ne l'est pas à la date de référence ; la colonne 22 a exactement `["Oui", "Non", "Non déterminable"]` ; la colonne 24 demande conditions de remboursement, rémunération, blocage, plafonnement, abandon de créance ; les colonnes 18 et 19 sont en `yes_no`.
- [ ] **Step 3: Valider** `python3 -m unittest tests.test_sci_grandes_fortunes_columns -v && python3 workflow-schema/validate-workflows.py`. Attendu : PASS et « Validated … ».

### Task 3: Familles D et E, démembrement et gérance (indices 27 à 44)

**Files:**
- Modify: `tabular-review-workflows/sci-grandes-fortunes-pack/statuts-sci-grandes-fortunes/table-columns.yaml`

**Interfaces:**
- Consumes: Task 2 (YAML à 27 colonnes).
- Produces: colonnes 27 à 44.

- [ ] **Step 1: Ajouter à `test_family_c` un test `test_family_d_e`** (`assertGreaterEqual(len(columns), 45)`) ; le lancer : attendu, échec.
- [ ] **Step 2: Ajouter les colonnes 27 à 44.** Contraintes spécifiques : la colonne 32 a pour tags `Nu-propriétaire`, `Usufruitier`, `Au choix`, `Non précisé` ; la colonne 41 a pour tags `Unanimité`, `Majorité renforcée`, `Juste motif seul`, `Majorité simple`, `Non précisé`.
- [ ] **Step 3: Valider** les mêmes commandes qu'en Task 2. Attendu : PASS.

### Task 4: Familles F, G, H, I et finalisation (indices 45 à 67)

**Files:**
- Modify: `tabular-review-workflows/sci-grandes-fortunes-pack/statuts-sci-grandes-fortunes/table-columns.yaml`
- Modify: `tabular-review-workflows/sci-grandes-fortunes-pack/statuts-sci-grandes-fortunes/SKILL.md` (si le générateur change quelque chose)

**Interfaces:**
- Consumes: Task 3 (YAML à 45 colonnes).
- Produces: colonnes 45 à 67 ; pack complet de 68 colonnes.

- [ ] **Step 1: Lancer** `python3 -m unittest tests.test_sci_grandes_fortunes_columns -v` ; `test_final_count` doit rester ignoré à 45 colonnes.
- [ ] **Step 2: Ajouter les colonnes 45 à 67.** Contraintes spécifiques : la colonne 55 a exactement les quatre tags des contraintes ; les colonnes 49 et 50 partagent les tags `Simple`, `Renforcée`, `Unanimité`, `Non précisé` ; la colonne 62 a pour tags `Expert`, `Formule`, `Valeur fixée`, `Non précisé`.
- [ ] **Step 3: Régénérer et valider** `python3 workflow-schema/generate-tabular-skills.py && python3 workflow-schema/validate-workflows.py && python3 -m unittest tests.test_sci_grandes_fortunes_columns -v`. Attendu : « Validated … », tests PASS, `test_final_count` exécuté et PASS.
- [ ] **Step 4: Vérifier le `git status`** : seuls `docs/`, `tests/` et le dossier du pack sont nouveaux ; aucun `.env`, aucun PDF client ; le fichier `__pycache__` non suivi existait déjà.
- [ ] **Step 5: Commit** (uniquement si l'utilisateur l'a demandé) : `git add tests tabular-review-workflows/sci-grandes-fortunes-pack docs && git commit -m "Ajout du pack Statuts SCI Grandes Fortunes"`, avec la ligne de co-auteur demandée par le contexte.
