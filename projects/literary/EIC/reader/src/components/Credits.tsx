import { useEffect } from "react";
import { Link } from "react-router-dom";
import { book, asset } from "../data/content";

export default function Credits() {
  useEffect(() => {
    document.title = `Visual Credits — ${book.title}`;
    window.scrollTo(0, 0);
  }, []);

  return (
    <article className="reader credits">
      <header className="chapter-head">
        <p className="chapter-kicker">Appendix</p>
        <h1 className="chapter-title">Visual Credits</h1>
      </header>
      <div className="prose">
        <p>
          This edition uses local copies of public-domain, CC0, and selected Creative
          Commons archival images, one author photograph, and a generated cover
          illustration. Full credits are listed below.
        </p>
      </div>
      <ul className="credit-list">
        {book.credits.map((c) => (
          <li key={c.id} id={c.id} className="credit-item">
            <img src={asset(c.file)} alt={c.alt} loading="lazy" />
            <div>
              <h2>{c.title}</h2>
              {c.caption && <p className="credit-cap">{c.caption}</p>}
              <p className="credit-meta">
                <strong>Source:</strong>{" "}
                {c.source_url ? (
                  <a href={c.source_url} rel="noopener noreferrer" target="_blank">
                    {c.title}
                  </a>
                ) : (
                  c.source_note || "Generated for this edition"
                )}
                <br />
                <strong>Creator:</strong> {c.creator || "Unknown"}
                {c.date ? ` · ${c.date}` : ""}
                <br />
                <strong>License:</strong> {c.license || "See source"}
              </p>
            </div>
          </li>
        ))}
      </ul>
      <nav className="chapter-nav">
        <Link to="/" className="nav-card prev">
          <span className="nav-dir">‹</span>
          <span className="nav-name">Contents</span>
        </Link>
      </nav>
    </article>
  );
}
