import { useEffect, useRef, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { book, asset } from "../data/content";

export default function Reader() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [progress, setProgress] = useState(0);
  const articleRef = useRef<HTMLElement>(null);

  const index = book.pages.findIndex((p) => p.id === id);
  const page = index >= 0 ? book.pages[index] : null;
  const prev = index > 0 ? book.pages[index - 1] : null;
  const next = index >= 0 && index < book.pages.length - 1 ? book.pages[index + 1] : null;

  // Reset scroll + title on chapter change
  useEffect(() => {
    window.scrollTo(0, 0);
    if (page) document.title = `${page.title} — ${book.title}`;
  }, [id, page]);

  // Reading progress
  useEffect(() => {
    let raf = 0;
    const onScroll = () => {
      cancelAnimationFrame(raf);
      raf = requestAnimationFrame(() => {
        const el = articleRef.current;
        if (!el) return;
        const total = el.offsetTop + el.offsetHeight - window.innerHeight;
        const p = total > 0 ? Math.min(1, Math.max(0, window.scrollY / total)) : 1;
        setProgress(p);
      });
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onScroll);
    onScroll();
    return () => {
      window.removeEventListener("scroll", onScroll);
      window.removeEventListener("resize", onScroll);
      cancelAnimationFrame(raf);
    };
  }, [id]);

  // Keyboard chapter navigation
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.metaKey || e.ctrlKey || e.altKey) return;
      if (e.key === "ArrowRight" && next) navigate(`/read/${next.id}`);
      if (e.key === "ArrowLeft" && prev) navigate(`/read/${prev.id}`);
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [navigate, next, prev]);

  if (!page) {
    return (
      <main className="reader">
        <p className="missing">Chapter not found. <Link to="/">Back to contents</Link>.</p>
      </main>
    );
  }

  return (
    <>
      <div className="progress-track" aria-hidden="true">
        <div className="progress-fill" style={{ transform: `scaleX(${progress})` }} />
      </div>

      <article className="reader" ref={articleRef}>
        {page.hero && (
          <figure className={"hero" + (page.hero.orientation === "portrait" ? " hero-portrait" : "")}>
            {page.hero.orientation === "portrait" && (
              <div
                className="hero-backdrop"
                style={{ backgroundImage: `url(${asset(page.hero.file)})` }}
                aria-hidden="true"
              />
            )}
            <img src={asset(page.hero.file)} alt={page.hero.alt} />
          </figure>
        )}

        <header className="chapter-head">
          <p className="chapter-kicker">{page.kicker}</p>
          <h1 className="chapter-title">{page.title}</h1>
          {page.year && <p className="chapter-year">{page.year}</p>}
          {page.epigraph && (
            <div className="chapter-epigraph" dangerouslySetInnerHTML={{ __html: page.epigraph }} />
          )}
        </header>

        <div className="prose" dangerouslySetInnerHTML={{ __html: page.body }} />

        <nav className="chapter-nav" aria-label="Chapter navigation">
          {prev ? (
            <Link to={`/read/${prev.id}`} className="nav-card prev">
              <span className="nav-dir">‹ Previous</span>
              <span className="nav-name">{prev.title}</span>
            </Link>
          ) : (
            <Link to="/" className="nav-card prev">
              <span className="nav-dir">‹</span>
              <span className="nav-name">Contents</span>
            </Link>
          )}
          {next ? (
            <Link to={`/read/${next.id}`} className="nav-card next">
              <span className="nav-dir">Next ›</span>
              <span className="nav-name">{next.title}</span>
            </Link>
          ) : (
            <Link to="/" className="nav-card next">
              <span className="nav-dir">Finish ›</span>
              <span className="nav-name">Back to Contents</span>
            </Link>
          )}
        </nav>
      </article>
    </>
  );
}
