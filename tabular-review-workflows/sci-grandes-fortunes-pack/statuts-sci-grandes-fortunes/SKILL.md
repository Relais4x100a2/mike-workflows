---
name: "statuts-sci-grandes-fortunes"
description: "Use this workflow to review French SCI (société civile immobilière) articles of association, including amendments and shareholder resolutions bundled in the same PDF, and extract normalised values and verbatim excerpts into the tabular review columns defined in table-columns.yaml. Column prompts are in French."
license: "MIT"
metadata:
  version: "1.0.0"
  author: "Relais4x100a2"
  language: "French"
  mike-display-name: "Statuts SCI Grandes Fortunes"
  mike-type: "tabular"
  mike-availability: "add-on"
  practice: "Droit des sociétés et patrimoine"
  jurisdictions: "France"
---
# Statuts SCI Grandes Fortunes

## Purpose

Use this workflow to review French SCI articles of association and extract structured information into the tabular review columns defined in `table-columns.yaml`.

## Instructions

- Apply each column prompt in `table-columns.yaml` to each document independently.
- Extract only information supported by the document text.
- Include clause references, section names, dates, amounts, party names, and defined terms where available.
- If responsive information is not found, return an empty value or a concise "Not found" response.
- Keep cell outputs concise while including enough context to make each extracted value useful.
- Do not invent citations, facts, parties, dates, rights, obligations, or financial consequences.
- Render the completed results as an exportable Excel (`.xlsx`) file. If Excel output is not possible, render the results as a Markdown table.
## Consignes de revue

- Un PDF peut contenir une page de garde, les statuts initiaux, des modifications, des procès-verbaux (PV) et d'autres pièces. Identifiez d'abord les pièces présentes, puis retenez comme acte de référence l'état le plus récent lisible des statuts, modifié par les décisions postérieures.
- Les valeurs sont neutres : extrayez ce que dit le texte, sans présupposer de stratégie patrimoniale.
- Ne donnez un pourcentage de capital ou une répartition que si la date de référence est connue ; sinon répondez « Non déterminable ».
- Pour les colonnes oui/non, « Non » signifie que la clause n'a pas été trouvée dans le PDF fourni. Elle peut figurer dans une pièce absente : tenez compte du type de PDF, de la date de l'état à jour et de la confiance globale.
- Une colonne « extrait » reprend la citation littérale de la clause avec son numéro d'article, sans paraphrase.
- Si une clause est ambiguë, retenez la valeur la moins interprétative et documentez-la dans l'extrait associé.
- Le résultat est un relevé de travail à vérifier par un humain, pas une analyse ni un avis juridique.
