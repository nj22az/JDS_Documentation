import raw from "./content.json";

export interface Asset {
  id: string;
  file: string;
  alt: string;
  caption?: string;
  orientation?: "portrait" | "landscape";
}

export interface Page {
  id: string;
  kicker: string;
  year: string;
  title: string;
  epigraph: string;
  hero: Asset | null;
  body: string;
}

export interface Credit {
  id: string;
  file: string;
  alt: string;
  title: string;
  caption: string;
  source_url: string;
  source_note: string;
  creator: string;
  date: string;
  license: string;
}

export interface Book {
  title: string;
  subtitle: string;
  cover: Asset | null;
  pages: Page[];
  credits: Credit[];
}

export const book = raw as Book;

/** Turn build-relative "assets/..." paths into app-relative "./assets/...". */
export function asset(path: string): string {
  return "./" + path.replace(/^\.?\//, "");
}
