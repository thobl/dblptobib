function getNextSibling (elem, selector) {
  var sibling = elem.nextElementSibling;
  while (sibling) {
    if (sibling.matches(selector)) return sibling;
    sibling = sibling.nextElementSibling
  }
};

document.addEventListener('click', function () {
  if (!event.target.classList.contains('pub_bibtex_toggle')) return;

  let bibtex = getNextSibling(event.target.parentElement, '.pub_bibtex')
  if (bibtex.style.display === "none") {
    bibtex.style.display = "block";
  } else {
    bibtex.style.display = "none";
  }

}, false);
