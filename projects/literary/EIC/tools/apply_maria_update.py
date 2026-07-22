#!/usr/bin/env python3
"""Apply the approved Book One updates to the Front-Row Seat reader bundle.

Steps (all in-place on an already-copied NEW bundle file; nothing is deleted):
1. Replace the `book-one-character-bible` page body with the approved Rev-B.
2. Insert the authorized ten-names beat at the end of 19-1625 §III.
3. Apply the five queued appendix-1b corrections.
4. Rename Mara -> Maria (word-boundary) in the bundle, omnibus-config.js and
   omnibus-illustrations.js; update affected word counts.
Run from the-front-row-seat/ directory.
"""
import re
import importlib.util

spec = importlib.util.spec_from_file_location(
    "ilp",
    "/home/user/JDS_Documentation/projects/literary/EIC/tools/inject_live_reader_pages.py",
)
ilp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ilp)

NEW_BUNDLE = "app/index-h4v2n8t3.js"
BIBLE_MD = (
    "/home/user/JDS_Documentation/projects/literary/EIC/"
    "manuscript-editorial/book-one-character-bible-proposed.md"
)

src = open(NEW_BUNDLE).read()


def words_of_html(markup):
    return len(re.sub(r"<[^>]+>", " ", markup).split())


def set_words(text, page_id, new_count):
    i = text.find('{id:"%s"' % page_id)
    j = text.find("`,hidden:", i)
    k = text.find(",words:", j)
    e = text.find(",", k + 7)
    old = int(text[k + 7:e])
    return text[:k] + ",words:%d" % new_count + text[e:], old


def replace_body(text, page_id, new_html):
    i = text.find('{id:"%s"' % page_id)
    assert i >= 0, page_id
    b = text.find("body:`", i) + 6
    e = text.find("`,hidden:", b)
    return text[:b] + ilp.template_literal(new_html) + text[e:]


# 1. Bible Rev-B body ------------------------------------------------------
md = open(BIBLE_MD).read()
md = re.sub(r"<!--[\s\S]*?-->\n?", "", md)
md = re.split(r"\n---\n", md)[0]
body = ilp.markdown_body(md)
assert "The Machine" in body and "Keeper" in body and "Maria" in body
src = replace_body(src, "book-one-character-bible", body)
src, old_w = set_words(src, "book-one-character-bible", words_of_html(body))
print("bible words:", old_w, "->", words_of_html(body))

# 2. Ten-names beat in 19-1625 --------------------------------------------
anchor = "partly drawn against.</p>"
assert src.count(anchor) == 1
insert = (
    "\n<p>One more thing crosses the water before the pens. Tom's list has "
    "kept ten blank lines above the entry he corrected — <em>names not yet "
    "recovered</em>, a boatswain's hand — and Mara read them for what they "
    "were, and said nothing. When the release comes down to the gate, a "
    "folded slip rides among the papers: ten names in a clerk's exact Dutch, "
    "no note attached, no fee entered. Tom writes them one by one into the "
    "spaces that were kept for them. He does not ask. She does not offer. "
    "The lines the account left open are people now, and neither of them "
    "will ever say why she could do it.</p>"
)
src = src.replace(anchor, anchor + insert, 1)
delta_batavia = words_of_html(insert)
src, old_w = set_words(src, "19-1625-batavia", old_w_dummy := 0)
# set_words wrote 0; fix with the real value based on the recorded old count
src, _zero = set_words(src, "19-1625-batavia", old_w + delta_batavia)
print("batavia words:", old_w, "->", old_w + delta_batavia)

# 3. Appendix-1b corrections ----------------------------------------------
REPLACEMENTS = [
    (
        "and, around 1772, one foreign sailor named James Holman",
        "and, in his Canton years, one foreign sailor named James Holman",
    ),
    (
        "His wrist, wrecked by a tea-chest around 1772, was set in a factory lane",
        "His wrist, wrecked by a tea-chest in his Canton years, was set in a factory lane",
    ),
    (
        "going on record with the Gazette man anyway",
        "going on record with the Member's man anyway",
    ),
    (
        "Gwen's wartime notebook (1940). Only the building holds all of it, "
        "until Hannah finds the hoard during a cellar refit in 2019 — counts "
        "it, understands none of it, and leaves it exactly where it lies.",
        "Gwen's wartime notebook (1940). The keepers add papers of their own "
        "— Bell's confession, an index sheet begun the week of the storm, "
        "Mara's warning home, a fold of blue cloth — curated, not left; that "
        "is a different verb, and the house knows the difference. Only the "
        "building holds all of it, until Hannah finds the hoard during a "
        "cellar refit in 2019 — counts it, understands none of it, and "
        "divides its keeping so that no single owner can ever hold the whole "
        "account.",
    ),
    (
        "The young keeper of 1701 never met Maggie, but the woman who "
        "trained her — Joan — was trained by Maggie herself. After that the "
        "line runs Bess (1770), Martha",
        "The young keeper of 1701 — the same woman who read the room in "
        "1696; the house held one keeper across those reigns, not two — "
        "never met Maggie, but the woman who trained her — Joan — was "
        "trained by Maggie herself. A man has held the lease more than once "
        "and held it honestly; the keeping never passed through him. After "
        "that the line runs through the Finch women — Bess (1770) is one of "
        "them, and there is more than one Bess behind this bar before the "
        "next century settles — then Martha",
    ),
]
appendix_delta = 0
for old, new in REPLACEMENTS:
    count = src.count(old)
    assert count == 1, ("MISSING/AMBIGUOUS", old[:60], count)
    src = src.replace(old, new, 1)
    appendix_delta += len(new.split()) - len(old.split())
i = src.find('{id:"appendix-1b-character-map"')
j = src.find(",words:", src.find("`,hidden:", i))
e = src.find(",", j + 7)
aw = int(src[j + 7:e])
src = src[:j] + ",words:%d" % (aw + appendix_delta) + src[e:]
print("appendix-1b words:", aw, "->", aw + appendix_delta)

# 4. Renames ---------------------------------------------------------------
n = len(re.findall(r"\bMara\b", src))
src = re.sub(r"\bMara\b", "Maria", src)
print("bundle renames:", n)
open(NEW_BUNDLE, "w").write(src)

for fname in ("omnibus-config.js", "omnibus-illustrations.js"):
    text = open(fname).read()
    c = len(re.findall(r"\bMara\b", text))
    text = re.sub(r"\bMara\b", "Maria", text)
    text = text.replace(
        '"19-1625-batavia":%d' % old_w,
        '"19-1625-batavia":%d' % (old_w + delta_batavia),
    )
    open(fname, "w").write(text)
    print(fname, "renames:", c)

print("OK")
