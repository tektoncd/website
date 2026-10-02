(function () {
  const toc = document.querySelector(".page-rail #TableOfContents");
  const header = document.querySelector("body > header");
  const scrollBtn = document.querySelector(".page-rail__top");
  if (!toc && !scrollBtn) {
    return;
  }

  const scroller = function () {
    return document.scrollingElement || document.documentElement;
  };

  const atBottom = function () {
    const el = scroller();
    return el.scrollHeight - el.scrollTop - el.clientHeight <= 80;
  };

  const toggleTop = function () {
    if (scrollBtn) {
      scrollBtn.classList.toggle("is-visible", atBottom());
    }
  };

  if (toc) {
    const links = Array.prototype.slice.call(toc.querySelectorAll('a[href^="#"]'));
    const headings = [];
    for (let i = 0; i < links.length; i++) {
      const id = decodeURIComponent((links[i].getAttribute("href") || "").replace(/^#/, ""));
      const heading = id ? document.getElementById(id) : null;
      if (heading) {
        headings.push({ id: heading.id, el: heading, link: links[i] });
      }
    }

    if (headings.length) {
      const offset = function () {
        return (header ? header.getBoundingClientRect().height : 64) + 24;
      };

      const setActive = function (id) {
        for (let i = 0; i < headings.length; i++) {
          const active = headings[i].id === id;
          headings[i].link.classList.toggle("is-active", active);
          if (active) {
            headings[i].link.setAttribute("aria-current", "location");
          } else {
            headings[i].link.removeAttribute("aria-current");
          }
        }
      };

      const updateToc = function () {
        if (atBottom()) {
          setActive(headings[headings.length - 1].id);
          return;
        }

        const line = offset();
        let current = headings[0];
        for (let i = 0; i < headings.length; i++) {
          if (headings[i].el.getBoundingClientRect().top - line <= 0) {
            current = headings[i];
          }
        }
        setActive(current.id);
      };

      document.addEventListener("scroll", updateToc, { passive: true, capture: true });
      updateToc();
    }
  }

  if (scrollBtn) {
    scrollBtn.addEventListener("click", function (event) {
      event.preventDefault();
      scroller().scrollTo({ top: 0, behavior: "smooth" });
    });
    document.addEventListener("scroll", toggleTop, { passive: true, capture: true });
    toggleTop();
  }
})();
