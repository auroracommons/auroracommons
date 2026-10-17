// Open the door a link names, so a tap on a door lands with the door open.
// Used by the home page and by Come in, whose doors are addressed as
// come-in#door-1 and onward. With scripts off, every door still opens by
// hand; nothing on either page needs this file to work.
(function () {
  function openNamed() {
    var id = window.location.hash.replace(/^#/, "");
    if (!id) { return; }
    var el = document.getElementById(id);
    if (el && el.tagName === "DETAILS") { el.open = true; }
  }
  openNamed();
  window.addEventListener("hashchange", openNamed);
})();
