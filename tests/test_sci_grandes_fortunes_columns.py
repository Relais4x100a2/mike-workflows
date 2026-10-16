import re
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
COLUMNS_FILE = (
    ROOT / "tabular-review-workflows" / "sci-grandes-fortunes-pack"
    / "statuts-sci-grandes-fortunes" / "table-columns.yaml"
)

EXPECTED = [
    ("Type de PDF", "tag"),
    ("Acte de référence retenu", "text"),
    ("Date de l'état à jour", "date"),
    ("Nombre de modifications statutaires repérées", "tag"),
    ("Lisibilité du PDF", "tag"),
    ("Confiance globale", "tag"),
    ("Forme et dénomination", "text"),
    ("Date de constitution", "date"),
    ("Durée de la société", "tag"),
    ("Objet : nature", "tag"),
    ("Objet étendu au-delà de l'immobilier", "yes_no"),
    ("Régime fiscal annoncé", "tag"),
    ("Capital social", "monetary_amount"),
    ("Capital variable", "yes_no"),
    ("Capital variable : extrait", "text"),
    ("Siège : ville", "text"),
    ("Nombre d'associés", "tag"),
    ("Part des personnes morales dans le capital", "tag"),
    ("Holding, SCI ou société associée", "yes_no"),
    ("Fondation, trust ou structure étrangère", "yes_no"),
    ("Associé majoritaire : part du capital", "percentage"),
    ("Associé majoritaire : nature", "tag"),
    ("Plusieurs générations associées", "tag"),
    ("Clause sur les comptes courants d'associés", "tag"),
    ("Compte courant d'associé : extrait", "text"),
    ("Parts à droits particuliers", "yes_no"),
    ("Parts à droits particuliers : extrait", "text"),
    ("Parts démembrées dans l'état à jour", "tag"),
    ("Vote des décisions ordinaires (démembrement)", "tag"),
    ("Vote des décisions extraordinaires (démembrement)", "tag"),
    ("Quasi-usufruit", "yes_no"),
    ("Réversion ou usufruit successif", "yes_no"),
    ("Affectation des réserves et bénéfices exceptionnels", "tag"),
    ("Démembrement : extrait", "text"),
    ("Nombre de gérants", "tag"),
    ("Gérant : nature", "tag"),
    ("Gérant nommé par les statuts", "yes_no"),
    ("Durée du mandat du gérant", "tag"),
    ("Étendue des pouvoirs du gérant", "tag"),
    ("Pouvoirs du gérant : extrait", "text"),
    ("Limites aux pouvoirs (autorisation de tiers)", "yes_no"),
    ("Verrouillage de la révocation", "tag"),
    ("Révocation du gérant : extrait", "text"),
    ("Rémunération du gérant", "tag"),
    ("Désignation du successeur du gérant", "tag"),
    ("Comité de surveillance, directoire ou conseil de famille", "yes_no"),
    ("Censeurs", "yes_no"),
    ("Actes du gérant soumis à autorisation d'un organe", "yes_no"),
    ("Gouvernance : extrait", "text"),
    ("Majorité ordinaire", "tag"),
    ("Majorité de modification des statuts", "tag"),
    ("Voix prépondérante", "yes_no"),
    ("Actes réservés aux associés", "yes_no"),
    ("Consultation écrite admise", "yes_no"),
    ("Agrément requis pour cession à un tiers", "yes_no"),
    ("Agrément intrafamilial et holdings", "tag"),
    ("Majorité d'agrément", "tag"),
    ("Agrément : extrait", "text"),
    ("Droit de préemption", "yes_no"),
    ("Inaliénabilité temporaire", "yes_no"),
    ("Exclusion ou retrait", "tag"),
    ("Rachat forcé ou clause texane", "yes_no"),
    ("Mode de valorisation des parts", "tag"),
    ("Continuation en cas de décès", "tag"),
    ("Agrément des héritiers", "tag"),
    ("Protection du conjoint survivant", "yes_no"),
    ("Mandat posthume", "yes_no"),
    ("Décès : extrait", "text"),
]

FALLBACK_EXEMPT = {0, 4, 5, 22, 55}
AGREMENT_TAGS = [
    "Totalement libre",
    "Soumis à agrément",
    "Libre selon conditions (descendants ou holding qualifiée)",
    "Non précisé",
]


def load_columns():
    return yaml.safe_load(COLUMNS_FILE.read_text(encoding="utf-8"))["columns"]


class SciColumnsTest(unittest.TestCase):
    def setUp(self):
        self.columns = load_columns()

    def test_prefix_matches_expected(self):
        for i, column in enumerate(self.columns):
            self.assertEqual(column["index"], i)
            self.assertEqual((column["name"], column["format"]), EXPECTED[i])

    def test_extrait_columns_are_text(self):
        for column in self.columns:
            if column["name"].endswith(": extrait"):
                self.assertEqual(column["format"], "text", column["name"])

    def test_tags_have_fallback(self):
        for column in self.columns:
            if column["format"] != "tag" or column["index"] in FALLBACK_EXEMPT:
                continue
            tags = column["tags"]
            self.assertTrue(
                "Non précisé" in tags or "Non déterminable" in tags, column["name"]
            )
        by_index = {c["index"]: c for c in self.columns}
        if 22 in by_index:
            self.assertEqual(by_index[22]["tags"], ["Oui", "Non", "Non déterminable"])
        if 55 in by_index:
            self.assertEqual(by_index[55]["tags"], AGREMENT_TAGS)

    def test_prompts_neutral_and_sourced(self):
        for column in self.columns:
            prompt = column["prompt"].lower()
            self.assertNotIn("fortune", prompt, column["name"])
            self.assertNotIn("milliardaire", prompt, column["name"])
            self.assertIsNone(
                re.search(r"\b(art\.?|article)\s+[lrd]?\d", prompt), column["name"]
            )

    def test_review_focus_wording(self):
        prompts = {c["index"]: c["prompt"] for c in self.columns}
        self.assertIn("PV", prompts[1])
        self.assertIn("modification", prompts[1])
        self.assertIn("page de garde", prompts[0])
        self.assertIn("Lisibilité", prompts[5])
        if 20 in prompts:
            self.assertIn("Non déterminable", prompts[20])

    def test_family_c(self):
        self.assertGreaterEqual(len(self.columns), 27)

    def test_family_d_e(self):
        self.assertGreaterEqual(len(self.columns), 45)

    def test_final_count(self):
        self.assertEqual(len(self.columns), 68)


if __name__ == "__main__":
    unittest.main()
