"""JDS Document Studio — a local web app that creates JDS-compliant documents.

The package is split into a pure-Python core (numbering, registry, templates) that
carries the JDS-critical logic and is unit-tested, plus thin engine/server layers
that shell out to the existing JDS scripts and expose an HTTP API.
"""

__version__ = "A"
