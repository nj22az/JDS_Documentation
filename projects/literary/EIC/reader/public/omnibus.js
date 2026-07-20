(function () {
  "use strict";

  var config = window.FRONT_ROW_OMNIBUS;
  if (!config) {
    throw new Error("omnibus-config.js must load before omnibus.js");
  }

  var illustrationData = window.FRONT_ROW_OMNIBUS_ILLUSTRATIONS;
  if (!illustrationData) {
    throw new Error("omnibus-illustrations.js must load before omnibus.js");
  }

  var books = config.books;

  var bookById = {};
  books.forEach(function (book) {
    bookById[book.id] = book;
  });

  var readingSpeed = config.readingSpeed;
  function formatNumber(value) {
    return String(value).replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  }

  function displayWords(value) {
    return formatNumber(value < 100 ? value : Math.round(value / 100) * 100);
  }

  function readingMinutes(words) {
    return Math.max(1, Math.round(words / readingSpeed));
  }

  function displayReadingTime(minutes) {
    if (minutes < 60) return minutes + " min";
    var hours = Math.floor(minutes / 60);
    var remainder = minutes % 60;
    return hours + " hr" + (remainder ? " " + remainder + " min" : "");
  }

  var readerBookIds = config.readerBookIds;
  var chapterWords = config.chapterWords;

  var readerBookById = {};
  readerBookIds.forEach(function (ids, index) {
    ids.forEach(function (id) {
      readerBookById[id] = books[index];
    });
  });

  var chapterTaglines = config.chapterTaglines;

  function addTagline(link, id) {
    var text = chapterTaglines[id];
    if (!text) return;
    var copy = link.querySelector(".toc-copy") || link;
    if (copy.querySelector(".toc-desc")) return;
    var desc = document.createElement("span");
    desc.className = "toc-desc";
    desc.textContent = text;
    copy.appendChild(desc);
  }

  function routeId() {
    var match = window.location.hash.match(/#\/read\/([^/?]+)/);
    return match ? match[1] : "";
  }

  function linkId(link) {
    var href = link.getAttribute("href") || "";
    var match = href.match(/#\/read\/([^/?]+)/);
    return match ? match[1] : "";
  }

  function updateCover(contents) {
    var cover = contents.querySelector(".cover");
    if (!cover) return;

    var kicker = cover.querySelector(".cover-kicker");
    var subtitle = cover.querySelector(".cover-sub");
    var startButton = cover.querySelector(".btn-primary");

    if (kicker) kicker.textContent = "Six books · 1603–2019";
    if (subtitle) subtitle.textContent = "Five centuries of the East India Company, observed from one Thames-side tavern.";
    if (startButton) startButton.textContent = "Begin with Book One";
  }

  function addBookStats(link, book) {
    var copy = link.querySelector(".toc-copy") || link;
    if (copy.querySelector(".toc-book-stats")) return;

    var stats = document.createElement("span");
    stats.className = "toc-book-stats";
    stats.title = "Estimated at " + readingSpeed + " words per minute";
    stats.innerHTML =
      "<span>" + displayWords(book.words) + " words</span>" +
      "<span aria-hidden=\"true\">·</span>" +
      "<span>≈ " + displayReadingTime(readingMinutes(book.words)) + "</span>";
    copy.appendChild(stats);
  }

  function addChapterStats(link, id) {
    var words = chapterWords[id];
    if (!words) return;

    var copy = link.querySelector(".toc-copy") || link;
    if (copy.querySelector(".toc-chapter-stats")) return;

    var minutes = readingMinutes(words);
    var stats = document.createElement("span");
    stats.className = "toc-chapter-stats";
    stats.title = "Estimated at " + readingSpeed + " words per minute";
    stats.setAttribute(
      "aria-label",
      displayWords(words) + " words. Estimated reading time " + displayReadingTime(minutes) + "."
    );
    stats.innerHTML =
      "<span>" + displayWords(words) + " words</span>" +
      "<span aria-hidden=\"true\">·</span>" +
      "<span>≈ " + displayReadingTime(minutes) + "</span>";
    copy.appendChild(stats);
  }

  function labelBookRow(link, book) {
    var kicker = link.querySelector(".toc-kicker");
    var title = link.querySelector(".toc-title");
    var year = link.querySelector(".toc-year");

    link.classList.add("toc-book-row");
    link.classList.remove("toc-chapter-row");
    link.setAttribute("data-book", book.numeral);
    if (kicker) {
      kicker.textContent = book.numeral === "V"
        ? "Book " + book.word + " · Compact edition"
        : "Book " + book.word;
    }
    if (title) title.textContent = book.title;

    if (!year) {
      year = document.createElement("span");
      year.className = "toc-year";
      var chevron = link.querySelector(".toc-chevron");
      link.insertBefore(year, chevron || null);
    }
    year.textContent = book.years;
    addBookStats(link, book);
  }

  function labelEpilogueRow(link, id) {
    var kicker = link.querySelector(".toc-kicker");
    link.classList.add("toc-chapter-row", "toc-epilogue-row");
    if (kicker) kicker.textContent = "Epilogue";
    addChapterStats(link, id);
  }

  function labelChapterRow(link, id) {
    link.classList.add("toc-chapter-row");
    addChapterStats(link, id);
  }

  function labelMetaRow(link) {
    link.classList.add("toc-meta-row");
  }

  function addReferenceLabel(link) {
    var item = link.closest("li");
    if (!item || item.parentNode.querySelector(".toc-section-label")) return;

    var label = document.createElement("li");
    label.className = "toc-section-label";
    label.textContent = "Reference";
    item.parentNode.insertBefore(label, item);
  }

  function updateContents(contents) {
    updateCover(contents);

    var toc = contents.querySelector(".toc");
    if (!toc) return;
    toc.setAttribute("aria-label", "Six books and their chapters");

    if (!toc.querySelector(".toc-heading")) {
      var heading = document.createElement("header");
      heading.className = "toc-heading";
      heading.innerHTML =
        "<h2>Reading order</h2>" +
        "<p>Choose a book, or continue chapter by chapter.</p>";
      toc.insertBefore(heading, toc.firstChild);
    }

    toc.querySelectorAll("a.toc-row").forEach(function (link) {
      var id = linkId(link);
      if (id === "00-frontmatter" || id === "book-one-character-bible") {
        link.closest("li").hidden = true;
      } else if (bookById[id]) {
        labelBookRow(link, bookById[id]);
      } else if (id === "part-six-afterlives") {
        labelEpilogueRow(link, id);
      } else if (id === "00a-foreword") {
        labelMetaRow(link);
      } else if (id.indexOf("appendix-") === 0) {
        addReferenceLabel(link);
        labelMetaRow(link);
      } else {
        labelChapterRow(link, id);
      }
      addTagline(link, id);
    });
  }

  var watchmansIllustrations = illustrationData.watchmans;

  function watchmansFigure(item) {
    var figure = document.createElement("figure");
    figure.className = "fig watchmans-plate";
    figure.setAttribute("data-watchmans-plate", item.file);

    var image = document.createElement("img");
    image.src = "assets/img/watchmans-daughter/" + item.file;
    image.alt = item.alt;
    image.loading = "lazy";
    image.decoding = "async";

    var caption = document.createElement("figcaption");
    caption.textContent = item.caption;

    figure.appendChild(image);
    figure.appendChild(caption);
    return figure;
  }

  function applyWatchmansIllustrations(reader) {
    var coverPath = "assets/img/watchmans-daughter/00-cover.jpg";
    var hero = reader.querySelector(".hero");
    var heroImage = hero && hero.querySelector("img");
    var heroBackdrop = hero && hero.querySelector(".hero-backdrop");

    if (heroImage && heroImage.getAttribute("src") !== coverPath) {
      heroImage.src = coverPath;
      heroImage.alt = "Su Zhang standing at the threshold of the family laundry between warm lamplight and the cold Limehouse morning.";
    }
    if (heroBackdrop) heroBackdrop.style.backgroundImage = "url(" + coverPath + ")";

    var prose = reader.querySelector(".prose");
    if (!prose) return;

    watchmansIllustrations.forEach(function (item) {
      if (prose.querySelector('[data-watchmans-plate="' + item.file + '"]')) return;

      var paragraph = Array.prototype.find.call(prose.querySelectorAll("p"), function (candidate) {
        return candidate.textContent.indexOf(item.after) !== -1;
      });

      if (paragraph) paragraph.insertAdjacentElement("afterend", watchmansFigure(item));
    });
  }

  var chapterOneIllustrations = illustrationData.chapterOne;

  function chapterOneFigure(item) {
    var figure = document.createElement("figure");
    figure.className = "fig chapter-one-figure";
    figure.setAttribute("data-chapter-one-plate", item.file);

    var image = document.createElement("img");
    image.src = item.file.indexOf("../") === 0
      ? "assets/img/" + item.file.slice(3)
      : "assets/img/chapter-one/" + item.file;
    image.alt = item.alt;
    image.loading = "lazy";
    image.decoding = "async";

    var caption = document.createElement("figcaption");
    caption.textContent = item.caption;

    figure.appendChild(image);
    figure.appendChild(caption);
    return figure;
  }

  function insertChapterOneFigure(prose, item) {
    if (prose.querySelector('[data-chapter-one-plate="' + item.file + '"]')) return;

    var paragraph = Array.prototype.find.call(prose.children, function (candidate) {
      return candidate.tagName === "P" && candidate.textContent.indexOf(item.after) !== -1;
    });
    if (!paragraph) return;
    paragraph.insertAdjacentElement("afterend", chapterOneFigure(item));
  }

  function bookPageScore(node) {
    if (node.tagName === "H2") return 70;
    if (node.tagName === "FIGURE") return 275;
    if (node.tagName === "BLOCKQUOTE") return 110;
    if (node.tagName === "HR") return 45;
    if (node.tagName === "TABLE") return 260;
    if (node.tagName === "PRE") return 180;
    var words = (node.textContent.trim().match(/\S+/g) || []).length;
    if (node.tagName === "UL" || node.tagName === "OL") return words + 90;
    return words + 28;
  }

  function buildBookPages(prose, pageMeta) {
    if (prose.querySelector(".book-spreads")) return;

    var nodes = Array.prototype.slice.call(prose.children);
    var pages = [];
    var page;
    var pageScore = 0;
    var pageLimit = 430;

    function startPage() {
      page = document.createElement("div");
      page.className = "book-page";
      pages.push(page);
      pageScore = 0;
    }

    startPage();
    nodes.forEach(function (node, index) {
      var score = bookPageScore(node);
      var nextScore = nodes[index + 1] ? bookPageScore(nodes[index + 1]) : 0;
      var wouldOverflow = pageScore > 0 && pageScore + score > pageLimit;
      var wouldOrphanHeading = node.tagName === "H2" && pageScore > 0 && pageScore + score + nextScore > pageLimit;

      if (wouldOverflow || wouldOrphanHeading) startPage();
      page.appendChild(node);
      pageScore += score;
    });

    for (var pair = 0; pair + 1 < pages.length; pair += 2) {
      var leftPage = pages[pair];
      var rightPage = pages[pair + 1];
      var leftScore = Array.prototype.reduce.call(leftPage.children, function (total, child) {
        return total + bookPageScore(child);
      }, 0);
      var rightScore = Array.prototype.reduce.call(rightPage.children, function (total, child) {
        return total + bookPageScore(child);
      }, 0);

      while (rightScore < leftScore * .65 && leftPage.children.length > 1) {
        var moved = leftPage.lastElementChild;
        var movedScore = bookPageScore(moved);
        rightPage.insertBefore(moved, rightPage.firstChild);
        leftScore -= movedScore;
        rightScore += movedScore;
      }
    }

    var book = document.createElement("div");
    book.className = "book-spreads";
    pages.forEach(function (currentPage, index) {
      var isLeftPage = index % 2 === 0;
      var footer = document.createElement("span");
      footer.className = "book-page-footer";
      footer.setAttribute("aria-hidden", "true");
      footer.textContent = pageMeta.footer;

      currentPage.setAttribute(
        "data-running-head",
        isLeftPage ? pageMeta.collectionTitle : pageMeta.chapterHead
      );
      currentPage.appendChild(footer);

      if (index % 2 === 0) {
        var spread = document.createElement("section");
        spread.className = "book-spread";
        spread.setAttribute("aria-label", "Reading spread " + (Math.floor(index / 2) + 1));
        book.appendChild(spread);
      }

      currentPage.classList.add(isLeftPage ? "book-page--left" : "book-page--right");
      book.lastElementChild.appendChild(currentPage);
    });

    if (pages.length % 2 !== 0) {
      var blank = document.createElement("div");
      blank.className = "book-page book-page--right book-page--blank";
      blank.setAttribute("aria-hidden", "true");
      book.lastElementChild.appendChild(blank);
    }

    prose.appendChild(book);
  }

  function applyChapterOneArtwork(reader) {
    var heroPath = "assets/img/chapter-one/01-rain-at-wapping.jpg";
    var hero = reader.querySelector(".hero");
    var heroImage = hero && hero.querySelector("img");

    if (heroImage && heroImage.getAttribute("src") !== heroPath) {
      heroImage.src = heroPath;
      heroImage.alt = "Wapping Wall in three days of rain, with warm tavern windows beside the dark Thames in 1603.";
    }

    var prose = reader.querySelector(".prose");
    if (!prose) return;
    chapterOneIllustrations.forEach(function (item) {
      insertChapterOneFigure(prose, item);
    });
  }

  function applyBookLayout(reader, id) {
    var book = readerBookById[id];
    if (!book) return;

    var head = reader.querySelector(".chapter-head");
    var kicker = head && head.querySelector(".chapter-kicker");
    var title = head && head.querySelector(".chapter-title");
    var year = head && head.querySelector(".chapter-year");
    var kickerText = kicker ? kicker.textContent.trim() : "";
    var titleText = title ? title.textContent.trim() : book.title;
    var yearText = year ? year.textContent.trim() : "";
    var chapterHead = [kickerText, titleText].filter(Boolean).join(" · ");
    var footerPeriod = yearText || book.years;

    var prose = reader.querySelector(".prose");
    if (!prose) return;
    reader.classList.add("reader--book-layout");
    buildBookPages(prose, {
      collectionTitle: "The Front-Row Seat",
      chapterHead: chapterHead,
      footer: "Book " + book.word + " · " + book.title + " · " + footerPeriod
    });
  }

  function updateReader(reader, id) {
    // The Wapping Twelve ledger is reachable only from Book One's own pages:
    // drop any prev/next card that would surface it in the linear reading flow.
    reader.querySelectorAll(".chapter-nav a").forEach(function (card) {
      if (linkId(card) === "book-one-character-bible") card.remove();
    });

    var head = reader.querySelector(".chapter-head");
    if (!head) return;

    var kicker = head.querySelector(".chapter-kicker");
    var title = head.querySelector(".chapter-title");
    var book = bookById[id];

    if (book) {
      if (kicker) {
        kicker.textContent = id === "12-1888-the-watchmans-daughter"
          ? "Book Five · Compact Edition"
          : "Book " + book.word;
      }
      if (title) title.textContent = book.title;

      document.title = book.title + " — The Front-Row Seat";
    }

    if (id === "part-six-afterlives") {
      if (kicker) kicker.textContent = "Book Six · Epilogue";
      document.title = "Afterlives — The Front-Row Seat";
    }

    if (id === "12-1888-the-watchmans-daughter") {
      applyWatchmansIllustrations(reader);
    }

    if (id === "01-1603-the-boy-who-signed") {
      applyChapterOneArtwork(reader);
    }

    applyBookLayout(reader, id);
  }

  var pending = false;
  var observer;
  function enhance() {
    pending = false;
    if (observer) observer.disconnect();

    try {
      var contents = document.querySelector("main.contents");
      if (contents) updateContents(contents);

      var reader = document.querySelector("article.reader");
      if (reader) updateReader(reader, routeId());
    } finally {
      if (observer) {
        observer.observe(document.getElementById("root"), { childList: true, subtree: true });
      }
    }
  }

  function scheduleEnhancement() {
    if (pending) return;
    pending = true;
    window.requestAnimationFrame(enhance);
  }

  observer = new MutationObserver(scheduleEnhancement);
  observer.observe(document.getElementById("root"), { childList: true, subtree: true });
  window.addEventListener("hashchange", scheduleEnhancement);
  window.addEventListener("DOMContentLoaded", scheduleEnhancement);
  scheduleEnhancement();
})();
