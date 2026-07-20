import { useEffect } from "react";
import { Link } from "react-router-dom";
import { book, asset } from "../data/content";

export default function Contents() {
  useEffect(() => {
    document.title = book.title;
    window.scrollTo(0, 0);
  }, []);

  const visiblePages = book.pages.filter((page) => !page.hidden);
  const firstChapter = visiblePages.find((page) => page.kicker.startsWith("Chapter")) ?? visiblePages[0];

  return (
    <main className="contents" lang="en">
      <section className="cover">
        {book.cover && (
          <div className="cover-art">
            <img src={asset(book.cover.file)} alt={book.cover.alt} />
          </div>
        )}
        <p className="cover-kicker">Illustrated Reading Edition</p>
        <h1 className="cover-title">{book.title}</h1>
        <p className="cover-sub">{book.subtitle}</p>
        <Link className="btn-primary" to={`/read/${firstChapter.id}`}>
          Start Reading
        </Link>
      </section>

      <nav className="toc" aria-label="Contents">
        <ol>
          {visiblePages.map((p) => (
            <li key={p.id}>
              <Link to={`/read/${p.id}`} className="toc-row">
                {p.hero && (
                  <span className="toc-thumb">
                    <img src={asset(p.hero.file)} alt="" loading="lazy" />
                  </span>
                )}
                <span className="toc-copy">
                  <span className="toc-kicker">{p.kicker}</span>
                  <span className="toc-title">{p.title}</span>
                </span>
                {p.year && <span className="toc-year">{p.year}</span>}
                <span className="toc-chevron" aria-hidden="true">›</span>
              </Link>
            </li>
          ))}
        </ol>
      </nav>

      <footer className="contents-foot">
        <Link to="/credits">Visual Credits</Link>
        <span className="dot">·</span>
        <span>Five centuries on the Thames</span>
      </footer>
    </main>
  );
}
