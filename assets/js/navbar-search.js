var shortcut = document.querySelector(".tekton-navbar__search-shortcut");
var searchInput = document.querySelector(".tekton-navbar .td-search-input");
var platform = ((navigator.userAgentData && navigator.userAgentData.platform) || navigator.platform || "") + " " + navigator.userAgent;
var isMobileOrTablet = /Android|iPhone|iPad|iPod/i.test(platform) ||
  (window.matchMedia && window.matchMedia("(pointer: coarse)").matches);

if (shortcut && !isMobileOrTablet) {
  if (/Mac/i.test(platform)) {
    shortcut.textContent = "⌘ K";
  }

  shortcut.hidden = false;
}

if (searchInput && !isMobileOrTablet) {
  document.addEventListener("keydown", function(event) {
    if (!(event.ctrlKey || event.metaKey) || event.key.toLowerCase() !== "k") {
      return;
    }

    if (searchInput.getClientRects().length) {
      event.preventDefault();
      searchInput.focus();
    }
  });
}
