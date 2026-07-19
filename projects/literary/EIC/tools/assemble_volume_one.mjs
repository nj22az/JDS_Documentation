#!/usr/bin/env node

import { readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const project = join(here, "..");
const canon = join(project, "manuscript-live-canon");
const output = join(
  project,
  "manuscript-editorial",
  "volume-one-the-venture-integrated.md",
);

const chapters = [
  "01-1603-the-boy-who-signed.md",
  "02-1603-dutch-courage.md",
  "03-1612-the-return.md",
  "02-1626-the-man-who-came-back-wrong.md",
  "04-1629-the-south-land.md",
  "05-1635-last-orders.md",
];

function manuscriptBody(path) {
  const source = readFileSync(path, "utf8").replace(
    /^---\r?\n[\s\S]*?\r?\n---\r?\n/,
    "",
  );

  return source
    .split(/\r?\n/)
    .map((line) => {
      const heading = /^(#{1,5})(\s+.*)$/.exec(line);
      return heading ? `#${heading[1]}${heading[2]}` : line;
    })
    .join("\n")
    .trim();
}

const sections = chapters.map((file) => manuscriptBody(join(canon, file)));
const document = [
  "<!-- generated-volume-one-development-manuscript -->",
  "<!-- source: manuscript-live-canon; run tools/assemble_volume_one.mjs -->",
  "",
  "# The Venture",
  "",
  "*1603–1635*",
  "",
  ...sections.flatMap((section, index) =>
    index === sections.length - 1 ? [section] : [section, "", "---", ""],
  ),
  "",
].join("\n");

writeFileSync(output, document, "utf8");
