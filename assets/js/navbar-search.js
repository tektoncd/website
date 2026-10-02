document.addEventListener("keydown", function(event) {
  if (!(event.ctrlKey || event.metaKey) || event.key.toLowerCase() !== "k") {
    return;
  }

  var searchInput = document.querySelector(".tekton-navbar .td-search-input");
  if (searchInput) {
    event.preventDefault();
    searchInput.focus();
  }
});
