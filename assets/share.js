document.addEventListener("click", function(e){
  var b = e.target && e.target.closest ? e.target.closest("[data-share]") : null;
  if (!b) return;
  var d = { title: b.getAttribute("data-title"), text: b.getAttribute("data-text"), url: b.getAttribute("data-url") };
  if (navigator.share) { navigator.share(d).catch(function(){}); return; }
  var old = b.textContent;
  function done(){ b.textContent = "Link copied"; setTimeout(function(){ b.textContent = old; }, 2000); }
  if (navigator.clipboard && navigator.clipboard.writeText) { navigator.clipboard.writeText(d.text + " " + d.url).then(done, done); }
});
