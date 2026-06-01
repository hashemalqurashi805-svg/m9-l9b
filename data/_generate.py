"""Generate recipes_kg.ttl + train/dev/test.jsonl deterministically.

Developer helper — not part of the learner workflow. The generated files
are committed in the template repo; learners do not run this script.

Usage:
    cd starter
    python -m data._generate

This rewrites:
    data/recipes_kg.ttl
    data/train.jsonl    (140 docs)
    data/dev.jsonl      (30 docs)
    data/test.jsonl     (30 docs)

Reproducibility: random seed pinned to 20260531. Identical re-runs
produce identical output.
"""

import json
import random
from pathlib import Path

SEED = 20260531
NS = "http://aispire.example.org/recipes/"
HERE = Path(__file__).parent


# -----------------------------------------------------------------------------
# KG content
# -----------------------------------------------------------------------------

# (uri_local, prefLabel, altLabels, ner_label_hint) — ner_label_hint is the
# NER label spaCy would plausibly emit on this surface form in recipe text.
INGREDIENTS = [
    ("eggplant", "eggplant", ["aubergine"], "PRODUCT"),
    ("basil", "basil", ["sweet basil"], "PRODUCT"),
    ("salt", "salt", [], "PRODUCT"),
    ("parmesan", "parmesan", ["parmigiano"], "PRODUCT"),
    ("tomato", "tomato", [], "PRODUCT"),
    ("garlic", "garlic", [], "PRODUCT"),
    ("orangeFruit", "orange", ["naranja"], "PRODUCT"),  # ambiguous w/ Color
    ("turkeyMeat", "turkey", ["tom"], "PRODUCT"),       # ambiguous w/ Cuisine
]

COLORS = [
    ("orangeColor", "orange", ["amber"]),               # ambiguous w/ Ingredient
]

# Cuisines with parent subclasses
CUISINES_LEAF = [
    ("Italian", "italian", [], "European"),
    ("French", "french", [], "European"),
    ("Greek", "greek", ["hellenic"], "European"),
    ("Thai", "thai", ["siamese"], "Asian"),
    ("Japanese", "japanese", [], "Asian"),
    ("Mexican", "mexican", [], None),
    ("turkeyCuisine", "turkish", ["turkey"], None),     # ambiguous w/ Ingredient
]

CUISINES_PARENT = [
    ("European", "european", []),
    ("Asian", "asian", []),
]

AUTHORS = [
    ("annaAuthor", "anna", [], "PERSON"),
    ("sarahAuthor", "sarah", [], "PERSON"),
    ("marcoAuthor", "marco", [], "PERSON"),
    ("yukiAuthor", "yuki", [], "PERSON"),
    ("rajAuthor", "raj", [], "PERSON"),
]

# Recipes — instances of :Recipe with cuisine, ingredient, author, popularity.
# (uri_local, name, cuisine_local, ingredient_local, author_local, popularity)
RECIPES = [
    ("r01", "Eggplant Parmesan", "Italian", "eggplant", "marcoAuthor", 0.91),
    ("r02", "Basil Pasta", "Italian", "basil", "marcoAuthor", 0.85),
    ("r03", "Provencal Stew", "French", "tomato", "annaAuthor", 0.74),
    ("r04", "Garlic Confit", "French", "garlic", "annaAuthor", 0.66),
    ("r05", "Greek Salad", "Greek", "tomato", "sarahAuthor", 0.78),
    ("r06", "Thai Basil Stir Fry", "Thai", "basil", "yukiAuthor", 0.82),
    ("r07", "Spicy Thai Eggplant", "Thai", "eggplant", "yukiAuthor", 0.71),
    ("r08", "Sushi Roll", "Japanese", "salt", "yukiAuthor", 0.88),
    ("r09", "Tacos al Pastor", "Mexican", "tomato", "rajAuthor", 0.83),
    ("r10", "Roast Turkey", "Italian", "turkeyMeat", "marcoAuthor", 0.69),
    ("r11", "Orange Salad", "French", "orangeFruit", "annaAuthor", 0.62),
    ("r12", "Turkish Eggplant", "turkeyCuisine", "eggplant", "rajAuthor", 0.64),
    ("r13", "Margherita Pizza", "Italian", "tomato", "marcoAuthor", 0.94),
    ("r14", "Pesto Genovese", "Italian", "basil", "marcoAuthor", 0.81),
    ("r15", "Ratatouille", "French", "eggplant", "annaAuthor", 0.76),
    ("r16", "Bouillabaisse", "French", "salt", "annaAuthor", 0.70),
    ("r17", "Moussaka", "Greek", "eggplant", "sarahAuthor", 0.79),
    ("r18", "Spanakopita", "Greek", "salt", "sarahAuthor", 0.72),
    ("r19", "Pad Thai", "Thai", "garlic", "yukiAuthor", 0.89),
    ("r20", "Green Curry", "Thai", "basil", "yukiAuthor", 0.84),
    ("r21", "Ramen", "Japanese", "garlic", "yukiAuthor", 0.92),
    ("r22", "Miso Soup", "Japanese", "salt", "yukiAuthor", 0.77),
    ("r23", "Enchiladas", "Mexican", "tomato", "rajAuthor", 0.80),
    ("r24", "Mexican Mole", "Mexican", "garlic", "rajAuthor", 0.73),
    ("r25", "Lasagna", "Italian", "parmesan", "marcoAuthor", 0.86),
    ("r26", "Coq au Vin", "French", "garlic", "annaAuthor", 0.75),
    ("r27", "Souvlaki", "Greek", "garlic", "sarahAuthor", 0.71),
    ("r28", "Tom Yum", "Thai", "garlic", "yukiAuthor", 0.83),
    ("r29", "Turkish Kofte", "turkeyCuisine", "turkeyMeat", "rajAuthor", 0.68),
    ("r30", "Citrus Salad", "Mexican", "orangeFruit", "rajAuthor", 0.65),
]


def write_kg():
    """Emit recipes_kg.ttl. Returns the triple count (approximate)."""
    lines = []
    a = lines.append
    a("@prefix : <http://aispire.example.org/recipes/> .")
    a("@prefix skos: <http://www.w3.org/2004/02/skos/core#> .")
    a("@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .")
    a("@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .")
    a("@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .")
    a("")
    a("# ---- Classes ----")
    for cls in ["Ingredient", "Color", "Cuisine", "Author", "Recipe"]:
        a(f":{cls} a rdfs:Class ; rdfs:label \"{cls}\" .")
    a("")
    a("# ---- Cuisine subclass hierarchy ----")
    for local, label, alts in CUISINES_PARENT:
        a(f":{local} a :Cuisine ; skos:prefLabel \"{label}\" .")
    for local, label, alts, parent in CUISINES_LEAF:
        head = f":{local} a :Cuisine"
        if parent:
            head += f" ; rdfs:subClassOf :{parent}"
        head += f" ; skos:prefLabel \"{label}\""
        for alt in alts:
            head += f" ; skos:altLabel \"{alt}\""
        head += " ."
        a(head)
    a("")
    a("# ---- Ingredients ----")
    for local, label, alts, _ in INGREDIENTS:
        line = f":{local} a :Ingredient ; skos:prefLabel \"{label}\""
        for alt in alts:
            line += f" ; skos:altLabel \"{alt}\""
        line += " ."
        a(line)
    a("")
    a("# ---- Colors (ambiguity sources) ----")
    for local, label, alts in COLORS:
        line = f":{local} a :Color ; skos:prefLabel \"{label}\""
        for alt in alts:
            line += f" ; skos:altLabel \"{alt}\""
        line += " ."
        a(line)
    a("")
    a("# ---- Authors ----")
    for local, label, alts, _ in AUTHORS:
        line = f":{local} a :Author ; skos:prefLabel \"{label}\""
        for alt in alts:
            line += f" ; skos:altLabel \"{alt}\""
        line += " ."
        a(line)
    a("")
    a("# ---- Recipes (instances) ----")
    for uri, name, cuisine, ing, author, pop in RECIPES:
        a(
            f":{uri} a :Recipe ; "
            f":name \"{name}\" ; "
            f":cuisine :{cuisine} ; "
            f":primaryIngredient :{ing} ; "
            f":authoredBy :{author} ; "
            f":popularityScore \"{pop}\"^^xsd:float ."
        )
    a("")
    out = HERE / "recipes_kg.ttl"
    out.write_text("\n".join(lines) + "\n")
    # crude triple count — each non-blank, non-comment line is roughly one
    # subject block; predicate count is the real metric. We'll count `;` + lines
    # ending in ` .` to approximate.
    body = out.read_text()
    triples = body.count(" ;") + body.count(" a ")  # rough lower bound
    return triples


# -----------------------------------------------------------------------------
# Document generation
# -----------------------------------------------------------------------------

# Build the surface-form -> (uri, ner_label, kg_type) index. This is the
# oracle the generator uses to write gold annotations. The reference
# linker reconstructs an equivalent index from the KG + NER_LABEL_TO_KG_TYPE.

KG_TYPE = {
    "Ingredient": f"{NS}Ingredient",
    "Color": f"{NS}Color",
    "Cuisine": f"{NS}Cuisine",
    "Author": f"{NS}Author",
}

# (surface_form_lower, [(uri, kg_type)], ner_label_for_doc)
# Disambiguation key for the generator: when emitting an ambiguous surface
# form, we pick which sense based on context (an adjacent cuisine implies
# the ingredient sense for "orange" vs. color, etc.).

# Unambiguous entries
UNAMBIG = {
    "eggplant":  (f"{NS}eggplant", "Ingredient", "PRODUCT"),
    "aubergine": (f"{NS}eggplant", "Ingredient", "PRODUCT"),
    "basil":     (f"{NS}basil", "Ingredient", "PRODUCT"),
    "salt":      (f"{NS}salt", "Ingredient", "PRODUCT"),
    "parmesan":  (f"{NS}parmesan", "Ingredient", "PRODUCT"),
    "tomato":    (f"{NS}tomato", "Ingredient", "PRODUCT"),
    "garlic":    (f"{NS}garlic", "Ingredient", "PRODUCT"),
    "italian":   (f"{NS}Italian", "Cuisine", "NORP"),
    "french":    (f"{NS}French", "Cuisine", "NORP"),
    "greek":     (f"{NS}Greek", "Cuisine", "NORP"),
    "hellenic":  (f"{NS}Greek", "Cuisine", "NORP"),
    "thai":      (f"{NS}Thai", "Cuisine", "NORP"),
    "japanese":  (f"{NS}Japanese", "Cuisine", "NORP"),
    "mexican":   (f"{NS}Mexican", "Cuisine", "NORP"),
    "european":  (f"{NS}European", "Cuisine", "NORP"),
    "asian":     (f"{NS}Asian", "Cuisine", "NORP"),
    "anna":      (f"{NS}annaAuthor", "Author", "PERSON"),
    "sarah":     (f"{NS}sarahAuthor", "Author", "PERSON"),
    "marco":     (f"{NS}marcoAuthor", "Author", "PERSON"),
    "yuki":      (f"{NS}yukiAuthor", "Author", "PERSON"),
    "raj":       (f"{NS}rajAuthor", "Author", "PERSON"),
}

# Ambiguous: two senses per surface form
AMBIG = {
    "orange": [
        (f"{NS}orangeFruit", "Ingredient", "PRODUCT"),
        (f"{NS}orangeColor", "Color", "PRODUCT"),
    ],
    "turkey": [
        (f"{NS}turkeyMeat", "Ingredient", "PRODUCT"),
        (f"{NS}turkeyCuisine", "Cuisine", "NORP"),
    ],
}

# NIL surface forms — not in KG
NILS = ["cinnamon", "quinoa", "priya", "peruvian"]


# Sentence templates. {ingredient}, {cuisine}, {author} slots filled randomly.
TEMPLATES = [
    "Try this {ingredient} {cuisine} recipe by {author}.",
    "A classic {cuisine} dish: {ingredient} sauteed with {ingredient2}.",
    "{author} shares a quick {ingredient} idea for weeknight dinners.",
    "Looking for {cuisine} ideas? {author}'s {ingredient} is a winner.",
    "{ingredient} pairs beautifully with {ingredient2} in this {cuisine} bowl.",
    "{author}'s blog features a new {cuisine} {ingredient} recipe.",
    "This {cuisine}-style {ingredient} stew comes from {author}.",
    "{ingredient} season is here — {author} recommends a {cuisine} preparation.",
]


def _make_doc(rng, doc_id, force_ambig=False, force_nil=False):
    """Generate one doc.

    The generator picks a template, fills slots, then walks the resulting
    text to compute span char offsets — gold annotations track real
    positions in the emitted string.
    """
    ingredient = rng.choice(["eggplant", "basil", "tomato", "garlic", "parmesan", "salt", "aubergine"])
    ingredient2 = rng.choice(["basil", "tomato", "garlic"])
    cuisine = rng.choice(["italian", "french", "greek", "thai", "japanese", "mexican", "european", "asian"])
    author = rng.choice(["anna", "sarah", "marco", "yuki", "raj"])

    # Inject ambiguity / NIL based on flags
    if force_ambig:
        ingredient = rng.choice(["orange", "turkey"])
    if force_nil:
        slot_to_nil = rng.choice(["ingredient", "cuisine", "author"])
        nil_val = rng.choice(NILS)
        if slot_to_nil == "ingredient":
            ingredient = nil_val
        elif slot_to_nil == "cuisine":
            cuisine = nil_val
        else:
            author = nil_val

    template = rng.choice(TEMPLATES)
    text = template.format(
        ingredient=ingredient,
        ingredient2=ingredient2,
        cuisine=cuisine,
        author=author.capitalize(),
    )

    # Walk the text and identify NER spans. We use a deterministic surface-form
    # scan: known surface forms (case-insensitive) become spans.
    ner_spans = []
    gold = []

    # Scan all known surface forms in order of length (longest first to avoid
    # nested matches).
    surface_index = {}
    for sf, info in UNAMBIG.items():
        surface_index[sf] = ("UNAMBIG", info)
    for sf, info in AMBIG.items():
        surface_index[sf] = ("AMBIG", info)
    for sf in NILS:
        surface_index[sf] = ("NIL", None)

    # Find non-overlapping spans.
    occupied = [False] * len(text)
    candidates_in_order = sorted(surface_index.keys(), key=lambda s: -len(s))
    for sf in candidates_in_order:
        lower = text.lower()
        start = 0
        while True:
            i = lower.find(sf, start)
            if i == -1:
                break
            j = i + len(sf)
            # word-boundary check
            left_ok = i == 0 or not text[i - 1].isalpha()
            right_ok = j == len(text) or not text[j].isalpha()
            if left_ok and right_ok and not any(occupied[i:j]):
                for k in range(i, j):
                    occupied[k] = True
                kind, info = surface_index[sf]
                # NER label: derived from the KG type when known; for NIL we
                # guess a plausible label from the slot family.
                if kind == "UNAMBIG":
                    uri, kg_type, ner_label = info
                    ner_spans.append({"text": text[i:j], "label": ner_label, "start": i, "end": j})
                    gold.append({"span_start": i, "span_end": j, "gold_uri": uri})
                elif kind == "AMBIG":
                    # Pick sense by context: if an unambiguous cuisine is in
                    # the same text, the ingredient sense wins; otherwise pick
                    # whichever sense's NER label appears most natural.
                    senses = info  # list of (uri, kg_type, ner_label)
                    # Default to first sense (Ingredient), unless the text
                    # contains a parent cuisine hint pointing at the other.
                    chosen = senses[0]
                    for s_uri, s_type, s_label in senses:
                        if s_type == "Cuisine" and any(
                            cu in lower for cu in ["italian", "french", "greek", "thai", "japanese", "european", "asian"]
                        ):
                            # cuisine sense unlikely in a recipe already typed as another cuisine
                            chosen = senses[0]
                            break
                    uri, kg_type, ner_label = chosen
                    ner_spans.append({"text": text[i:j], "label": ner_label, "start": i, "end": j})
                    gold.append({"span_start": i, "span_end": j, "gold_uri": uri})
                else:
                    # NIL — emit ner span with no gold URI. Pick a label.
                    ner_spans.append({"text": text[i:j], "label": "PRODUCT", "start": i, "end": j})
                    gold.append({"span_start": i, "span_end": j, "gold_uri": None})
            start = j

    # Sort by span start.
    ner_spans.sort(key=lambda s: s["start"])
    gold.sort(key=lambda g: g["span_start"])

    return {
        "doc_id": doc_id,
        "text": text,
        "ner_spans": ner_spans,
        "gold": gold,
    }


def generate_split(rng, n, prefix, ambig_target_pct=0.18, nil_target_pct=0.07):
    """Generate a list of n docs with target ambig/nil rates."""
    docs = []
    # Estimate per-doc spans ~3 to budget; we'll oversample then trim.
    target_ambig_docs = int(round(n * ambig_target_pct * 3))
    target_nil_docs = int(round(n * nil_target_pct * 3))
    for i in range(n):
        force_ambig = i < target_ambig_docs
        force_nil = (i >= target_ambig_docs) and (i < target_ambig_docs + target_nil_docs)
        doc = _make_doc(rng, f"{prefix}-{i:04d}", force_ambig=force_ambig, force_nil=force_nil)
        # Reject docs with zero ner_spans
        if not doc["ner_spans"]:
            doc = _make_doc(rng, f"{prefix}-{i:04d}", force_ambig=False, force_nil=False)
        docs.append(doc)
    rng.shuffle(docs)
    return docs


def write_split(docs, name):
    out = HERE / name
    with out.open("w") as f:
        for d in docs:
            f.write(json.dumps(d) + "\n")
    return len(docs)


def main():
    rng = random.Random(SEED)
    triples = write_kg()
    train = generate_split(rng, 140, "train")
    dev = generate_split(rng, 30, "dev")
    test = generate_split(rng, 30, "test")
    n_train = write_split(train, "train.jsonl")
    n_dev = write_split(dev, "dev.jsonl")
    n_test = write_split(test, "test.jsonl")
    print(f"KG triples (approx): {triples}")
    print(f"train.jsonl: {n_train} docs")
    print(f"dev.jsonl:   {n_dev} docs")
    print(f"test.jsonl:  {n_test} docs")


if __name__ == "__main__":
    main()
