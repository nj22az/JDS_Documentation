import { Link, useLocation } from "react-router-dom";
import { book } from "../data/content";
import { ChevronLeft } from "./icons";

export default function TopBar({ onOpenSettings }: { onOpenSettings: () => void }) {
  const { pathname } = useLocation();
  const readMatch = pathname.match(/^\/read\/(.+)$/);
  const onContents = pathname === "/" || pathname === "";

  let title = book.title;
  if (readMatch) {
    const page = book.pages.find((p) => p.id === decodeURIComponent(readMatch[1]));
    if (page) title = page.title;
  } else if (pathname === "/credits") {
    title = "Visual Credits";
  }

  return (
    <header className="topbar">
      <div className="topbar-inner">
        <div className="topbar-left">
          {!onContents && (
            <Link to="/" className="tb-btn tb-back" aria-label="Contents">
              <ChevronLeft size={20} />
              <span>Contents</span>
            </Link>
          )}
        </div>
        <div className="topbar-title" title={title}>
          {title}
        </div>
        <div className="topbar-right">
          <button className="tb-btn tb-aa" onClick={onOpenSettings} aria-label="Reading settings">
            <span aria-hidden="true">A</span>
            <span aria-hidden="true" className="tb-aa-small">a</span>
          </button>
        </div>
      </div>
    </header>
  );
}
