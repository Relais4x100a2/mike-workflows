# Revue tabulaire des statuts de SCI (grandes fortunes) : conception

## Intention

Projet de recherche personnel, non commercial, à visée scientifique, sur l'usage de la SCI dans la structuration du patrimoine immobilier des grandes fortunes françaises. Le corpus compte quelques centaines de SCI dont des milliardaires sont associés ou dirigeants. On cherche à faire émerger des tendances de façon exploratoire, sans question tranchée à l'avance.

Le workflow est un pack tabulaire Mike : une ligne par PDF (une SCI), une colonne par point extrait. Les valeurs doivent être normalisées pour permettre un traitement statistique, avec une auditabilité minimale sur les clauses sensibles.

## Objectifs

- Extraire environ 55 points normalisés (colonnes `tag`, `yes_no`, `percentage`, `date`) répartis en 9 familles.
- Doubler une dizaine de points sensibles d'une colonne `text` d'extrait littéral avec numéro d'article, pour le contrôle qualité et l'évolution du codebook.
- Identifier l'« état à jour » des statuts dans des PDF hétérogènes (pages de garde, statuts initiaux, modifications, PV, pièces diverses).

## Non-objectifs

- Aucune analyse juridique ni conseil : extraction seulement.
- Pas de lecture des comptes ni de la comptabilité : seules les clauses statutaires comptent (les comptes courants, par exemple, ne sont observés que par la clause).
- Pas d'enrichissement externe (Pappers, registres) : le workflow ne lit que le PDF fourni.
- Pas d'article de loi, arrêt ou montant écrit de mémoire dans les prompts.

## Anti-objectifs

- Un prompt qui présuppose la thèse (« les grandes fortunes verrouillent le pouvoir ») et biaise l'extraction : les prompts restent neutres et demandent ce que dit le texte.
- Une valeur plausible mais inventée quand le PDF est muet : la valeur « Non précisé » ou « Non déterminable » doit toujours exister et être préférée à une déduction.
- Un état à jour reconstitué à tort en ignorant une modification ou un PV postérieur.

## Contraintes

- Contraintes du dépôt (`CLAUDE.md`, `CONTRIBUTING.md`) : dossier du pack dans `tabular-review-workflows/*-pack/` avec `pack.yaml` ; `table-columns.yaml` aux formats autorisés (`text`, `date`, `monetary_amount`, `percentage`, `bulleted_list`, `yes_no`, `tag` avec tags uniques) ; indices contigus à partir de 0 ; `name` du workflow = slug ASCII du `mike-display-name` ; `python3 workflow-schema/validate-workflows.py` doit passer ; `SKILL.md` généré par `workflow-schema/generate-tabular-skills.py`, consignes spécifiques placées dans une section après le bloc généré.
- Langue des prompts et du `SKILL.md` : français.
- Ne jamais lire ni committer `backend/.env` ni des documents clients (les statuts du corpus ne sont pas versionnés).
- Tout tag est à valeurs fermées et inclut « Non précisé » (silence des statuts) ; les familles dépendant de la date de référence ajoutent « Non déterminable ».

## Décisions prises avec l'utilisateur

- Repartir de zéro sur le fond (droit français) plutôt que d'adapter un pack étranger.
- 8 familles de départ plus une famille de gouvernance : Identité et cadre ; Capital et associés ; Démembrement ; Gérance ; Gouvernance et organes de contrôle ; Décisions collectives ; Circulation des parts ; Décès et transmission ; Qualité de l'extraction.
- Ajouts retenus : capital variable ; clause statutaire sur les comptes courants d'associés ; parts à droits particuliers (veto, fondateurs) ; affectation des réserves et bénéfices exceptionnels en cas de démembrement ; verrouillage de la révocation du gérant ; comité de surveillance, directoire ou conseil de famille, censeurs et autorisation préalable ; agrément libre pour les holdings familiales ; clause de rachat forcé (« texane »).
- Convention `yes_no` : le format n'admet que deux états ; « Non » signifie « non trouvé dans le PDF fourni ». Un PDF incomplet peut donc produire un faux « Non » ; la famille A (type de PDF, date de l'état à jour, confiance) sert à filtrer ces cas à l'analyse. Seules les colonnes où « Non déterminable » compte vraiment sont typées `tag`.
- Nom d'affichage « Statuts SCI Grandes Fortunes » ; dossier de workflow = slug ASCII correspondant (`statuts-sci-grandes-fortunes`) dans `tabular-review-workflows/sci-grandes-fortunes-pack/`.
- Licence MIT.
- Approche hybride : colonnes normalisées pour la statistique, colonnes `text` d'extrait littéral uniquement pour les clauses sensibles.

## Colonnes

Convention : `[tag]` valeurs fermées, `[oui/non]` = `yes_no`, `[%]` = `percentage`, `[date]`, `[text]` extrait littéral avec numéro d'article. Les valeurs précises des tags sont listées dans `table-columns.yaml`.

**A. Qualité de l'extraction (en tête, pour piloter la lecture)**
1. Type de PDF [tag] : statuts seuls / statuts + modifications / statuts + PV / autre
2. Acte de référence retenu [text]
3. Date de l'état à jour [date]
4. Nombre de modifications statutaires repérées [tag : 0 / 1 / 2 à 3 / 4 et plus / Non déterminable]
5. Lisibilité du PDF [tag : bonne / partielle / mauvaise]
6. Confiance globale [tag : élevée / moyenne / faible]

**B. Identité et cadre**
7. Forme et dénomination [text]
8. Date de constitution [date]
9. Durée de la société [tag]
10. Objet : nature [tag : gestion patrimoniale / familiale / construction-vente / mixte / autre]
11. Objet : étendu au-delà de l'immobilier [oui/non]
12. Régime fiscal annoncé [tag : IR / IS / non précisé]
13. Capital social [monetary_amount]
14. Capital variable [oui/non]
15. Capital variable : extrait [text]
16. Siège : ville [text]

**C. Capital et associés**
17. Nombre d'associés [tag par tranches]
18. Part des personnes morales dans le capital [tag par tranches]
19. Présence d'une holding, SCI ou société associée [oui/non]
20. Présence d'une fondation, d'un trust ou d'une structure étrangère [oui/non]
21. Associé majoritaire : part du capital [%]
22. Associé majoritaire : nature [tag : personne physique / société / fondation ou trust / non déterminable]
23. Plusieurs générations associées [tag : Oui / Non / Non déterminable] (typé tag : le format yes_no n'admet que deux états)
24. Clause sur les comptes courants d'associés [tag : aucune / rémunération fixée / blocage ou plafond / les deux]
24bis. Compte courant d'associé : extrait [text] (conditions de remboursement, rémunération, blocage, plafonnement, abandon de créance)
25. Parts à droits particuliers (veto, fondateurs) [oui/non]
26. Parts à droits particuliers : extrait [text]

**D. Démembrement**
27. Parts démembrées dans l'état à jour [tag : aucune / en partie / majoritairement / non déterminable]
28. Qui vote les décisions ordinaires [tag : usufruitier / nu-propriétaire / répartition / non précisé]
29. Qui vote les décisions extraordinaires [tag idem]
30. Quasi-usufruit prévu [oui/non]
31. Réversion ou usufruit successif [oui/non]
32. Affectation des réserves et bénéfices exceptionnels [tag : nu-propriétaire / usufruitier / au choix / non précisé]
33. Démembrement : extrait [text]

**E. Gérance**
34. Nombre de gérants [tag par tranches]
35. Gérant : nature [tag : personne physique / personne morale / mixte]
36. Gérant nommé par les statuts [oui/non]
37. Durée du mandat [tag : illimitée / déterminée / non précisé]
38. Étendue des pouvoirs [tag : générale / limitée par liste / non précisé]
39. Pouvoirs : extrait [text]
40. Limites aux pouvoirs (autorisation préalable de tiers) [oui/non]
41. Verrouillage de la révocation [tag : unanimité / majorité renforcée / juste motif seul / majorité simple / non précisé]
42. Révocation : extrait [text]
43. Rémunération du gérant [tag : gratuit / fixée par décision / fixée par statuts / non précisé]
44. Désignation du successeur [tag : prévue nominativement / par décision / non précisé]

**F. Gouvernance et organes de contrôle**
45. Comité de surveillance, directoire ou conseil de famille [oui/non]
46. Censeurs [oui/non]
47. Séparation contrôle / gestion : actes soumis à autorisation [oui/non]
48. Gouvernance : extrait [text]

**G. Décisions collectives**
49. Majorité ordinaire [tag : simple / renforcée / unanimité / non précisé]
50. Majorité pour modifier les statuts [tag idem]
51. Voix prépondérante attribuée [oui/non]
52. Actes réservés aux associés (vente d'actif, hypothèque, bail) [oui/non]
53. Consultation écrite admise [oui/non]

**H. Circulation des parts**
54. Agrément requis pour cession à un tiers [oui/non]
55. Agrément intrafamilial et holdings [tag : Totalement libre / Soumis à agrément / Libre selon conditions (descendants ou holding qualifiée) / Non précisé]
56. Majorité d'agrément [tag]
57. Agrément : extrait [text]
58. Droit de préemption [oui/non]
59. Inaliénabilité temporaire [oui/non]
60. Exclusion ou retrait [tag : exclusion / retrait / les deux / aucun]
61. Clause de rachat forcé ou « texane » [oui/non]
62. Mode de valorisation des parts [tag : expert / formule / valeur fixée / non précisé]

**I. Décès et transmission**
63. Continuation en cas de décès [tag : continue / dissolution / non précisé]
64. Agrément des héritiers [tag : libre / soumis / non précisé]
65. Protection du conjoint survivant [oui/non]
66. Mandat posthume [oui/non]
67. Décès : extrait [text]

(Total : 68 colonnes, numérotées 0 à 67 dans le YAML ; la colonne 24bis s'insère après la 24 ; les extraits `text` sont au nombre de dix environ et ne couvrent que les clauses sensibles. Le nombre exact et la répartition peuvent bouger sans changer le design.)

## Comportement attendu du workflow

- Identifier d'abord les pièces du PDF (statuts, modifications, PV) et choisir l'acte de référence : la version la plus récente des statuts, modifiée par les décisions postérieures lisibles.
- Ne retenir la répartition du capital que si la date de référence est connue ; à défaut, `Non déterminable`.
- Toute clause ambiguë reçoit la valeur la moins interprétative et la mention dans l'extrait associé.
- Cellule `text` : citation littérale, numéro d'article, pas de paraphrase.

## Laissé au constructeur

- Nom exact du workflow et du pack (`mike-display-name`, slug, `id` du pack).
- Libellés précis des tags, tranches et ordre définitif des colonnes.
- Rédaction détaillée des prompts et des consignes spécifiques du `SKILL.md`.
- Libellés finaux de l'extrait de la colonne 24bis.
