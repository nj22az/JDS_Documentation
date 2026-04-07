"""prompts.py — Dynamic prompt templating.

Syntax: {option1|option2|option3} picks one at random.
Nesting supported: {a {red|blue} car|a {big|small} dog}

Example:
  "a {beautiful|stunning} {Vietnamese|Japanese} woman in a {red|blue} dress"
  → "a stunning Vietnamese woman in a blue dress"
"""

import re
import random


def expand(template, rng=None):
    """Expand all {a|b|c} blocks in template, return one resolved string."""
    if rng is None:
        rng = random.Random()

    # Resolve innermost braces first (no nested braces inside)
    pattern = re.compile(r'\{([^{}]+)\}')

    while pattern.search(template):
        def _pick(m):
            options = m.group(1).split("|")
            return rng.choice(options).strip()
        template = pattern.sub(_pick, template)

    # Clean up double spaces
    return re.sub(r'  +', ' ', template).strip()


def expand_batch(template, count=4, seed=None):
    """Generate `count` different expansions from the same template."""
    base_seed = seed if seed is not None else random.randint(0, 2**32)
    results = []
    for i in range(count):
        rng = random.Random(base_seed + i)
        results.append(expand(template, rng))
    return results


def has_dynamic(text):
    """Return True if text contains {a|b} patterns."""
    return bool(re.search(r'\{[^{}]*\|[^{}]*\}', text))
