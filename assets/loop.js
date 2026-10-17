// The one repeat interaction of this site: one small act for another
// person, its effect shown, a thank you by the name the person chose,
// and one next act offered. State lives only in this device's
// localStorage under tc_loop. Nothing is sent anywhere, no one is
// scored, no streak is kept, and the page says all of that beside the
// act. With scripts off, the act and its link stand as plain text.
(function () {
  var panel = document.getElementById("one-act");
  if (!panel) { return; }
  var KEY = "tc_loop";
  var store = { acts: [], name: "", visits: 0 };
  try {
    var raw = window.localStorage.getItem(KEY);
    if (raw) { var parsed = JSON.parse(raw); if (parsed) { store = parsed; } }
  } catch (e) {}
  function save() {
    try { window.localStorage.setItem(KEY, JSON.stringify(store)); } catch (e) {}
  }
  var freshSession = false;
  try { freshSession = !window.sessionStorage.getItem("tc_seen"); } catch (e) {}
  if (freshSession) {
    store.visits = (store.visits || 0) + 1;
    try { window.sessionStorage.setItem("tc_seen", "1"); } catch (e) {}
    save();
  }

  var ACTS = {
    "check-listing": {
      t: "Check one listing in Ground", m: "About 3 minutes",
      text: "Open the provider's own page, confirm the address and hours, and say so where it files.",
      href: "https://github.com/topsoilcommons/ground/issues/new?title=Check%20a%20listing",
      effect: "That listing's check date moves to today, and it stays true for the next person who needs it tonight.",
      past: "checked one listing in Ground", next: "add-listing"
    },
    "add-listing": {
      t: "Add one listing to Ground", m: "About 5 minutes",
      text: "Name a source of help with no listing yet, with its address and hours from the provider's own page.",
      href: "https://github.com/topsoilcommons/ground/issues/new?title=Add%20a%20listing",
      effect: "A new source of help enters the board, marked as proposed until a second person checks it.",
      past: "added one listing to Ground", next: "witness"
    },
    "witness": {
      t: "Witness one moment to the Index", m: "About 5 minutes",
      text: "File what you saw, with its time and place: a photo, a sound, or plain words.",
      href: "https://topsoilcommons.github.io/index/",
      effect: "What you saw enters the shared timeline as a claim, and a second person can now check it.",
      past: "witnessed one moment to the Index", next: "check-claim"
    },
    "check-claim": {
      t: "Check one claim in Atlas", m: "About 5 minutes",
      text: "Recompute one claim's seal and log what you get, whether it matches or not.",
      href: "https://github.com/topsoilcommons/atlas/issues/new?title=Check%20a%20claim",
      effect: "A proof now has a second pair of eyes on it. If it failed, it becomes a correction in the open, never a secret.",
      past: "checked one claim in Atlas", next: "run-finding"
    },
    "run-finding": {
      t: "Run one finding in Foundations", m: "About 3 minutes",
      text: "Run one demonstration, then say where it lost you.",
      href: "foundations",
      effect: "Your note makes the next version clearer for everyone who runs it after you.",
      past: "ran one finding in Foundations", next: "check-listing"
    },
    "street": {
      t: "Add the thing your street already has", m: "About 2 minutes",
      text: "A market, a cleanup, a game: name it, so your place shows up for the next person who feels alone.",
      href: "https://topsoilcommons.org/come-in#door-4",
      effect: "Your street's good thing is now visible to the next person who opens this page feeling the same way you did.",
      past: "added the thing your street already has", next: "witness"
    },
    "give": {
      t: "Pick one act to give", m: "Your pace",
      text: "Read the acts on Come in and pick by what you hold: time, local knowledge, a skill, a language, a car, surplus food, a room. Money is not among them yet: it moves only through a fiscal host, and that door stays shut until one is appointed.",
      href: "https://topsoilcommons.org/come-in#door-7",
      effect: "You chose by what you hold, with the act's minutes and what it changes stated before you commit to anything.",
      past: "picked an act to give", next: "check-listing"
    },
    "listing-true": {
      t: "Keep your own listing true", m: "About 10 minutes",
      text: "Check your hours and address as they stand on the board, and correct what moved.",
      href: "https://topsoilcommons.org/come-in#door-8",
      effect: "The cheapest true fact in this system is current again, checked by the person who knows it best.",
      past: "kept a listing true", next: "check-listing"
    }
  };
  var DOOR_ACT = { "1": "check-listing", "2": "add-listing", "3": "witness",
    "4": "street", "5": null, "6": "check-claim", "7": "give", "8": "listing-true" };
  var WITNESS = [
    "Lately, in the open: on October 17, 2026, a warming center in the Bronx was added to Ground from the City Comptroller's own page, so someone cold tonight finds a door that is really open.",
    "Lately, in the open: on October 17, 2026, a walkthrough written by Wedajo Getachew, a volunteer, was landed in Cohort and credited to them as first author in the public ledger.",
    "Lately, in the open: on October 16, 2026, the first pull request from an outside contributor was merged into Machine, and the contributor was credited in the public ledger.",
    "Lately, in the open: on October 16, 2026, 52 listings across 6 places were added to Ground, every one checked against its provider's own page before it stood.",
    "Lately, in the open: on October 15, 2026, 8 listings near New Rochelle passed their check, and 4 were dropped for failing it, so no one travels to a door that is not there.",
    "Lately, in the open: on October 16, 2026, a warming space at Harlem Hospital was added to Ground from the City of New York's own page, open 24 hours a day."
  ];
  var MONTHS = ["January","February","March","April","May","June","July",
    "August","September","October","November","December"];
  var witEl = document.getElementById("oa-wit");
  var bodyEl = document.getElementById("oa-body");
  var current = "check-listing";

  function dayOfYear() {
    var now = new Date();
    return Math.floor((now - new Date(now.getFullYear(), 0, 0)) / 86400000);
  }
  function fmtDate(iso) {
    var d = new Date(iso + "T12:00:00");
    return MONTHS[d.getMonth()] + " " + d.getDate() + ", " + d.getFullYear();
  }
  function todayIso() {
    var d = new Date();
    function p(n) { return (n < 10 ? "0" : "") + n; }
    return d.getFullYear() + "-" + p(d.getMonth() + 1) + "-" + p(d.getDate());
  }
  function pickWitness() {
    if (!store.acts.length && store.visits <= 1) { return 0; }
    return (dayOfYear() + store.visits + store.acts.length) % WITNESS.length;
  }
  function setWitness() { witEl.textContent = WITNESS[pickWitness()]; }

  function renderAct(id) {
    current = id;
    var a = ACTS[id];
    bodyEl.innerHTML =
      '<p class="oa-act"><strong></strong> <span class="oa-text"></span></p>' +
      '<p class="oa-row"><a class="oa-go" target="_blank" rel="noopener">Start the act</a>' +
      '<button type="button" class="oa-btn" id="oa-done">I did it</button></p>' +
      '<p class="oa-note">No account, no fee, and this site collects nothing about you. ' +
      'If you finish an act, this device remembers it, only here, so your next visit picks up where you left off.</p>';
    bodyEl.querySelector(".oa-act strong").textContent = a.t + ".";
    bodyEl.querySelector(".oa-text").textContent = a.m + ". " + a.text;
    var go = bodyEl.querySelector(".oa-go");
    go.setAttribute("href", a.href);
    document.getElementById("oa-done").addEventListener("click", complete);
  }
  function renderRest() {
    current = null;
    bodyEl.innerHTML =
      '<p class="oa-act">Nothing is asked on a hard day. ' +
      '<a href="https://topsoilcommons.github.io/still/">Open Still and breathe</a>: ' +
      'a slow pacer, a short check in, and crisis lines checked at their sources. ' +
      'On a better day, one act waits here: check that one crisis line still answers.</p>' +
      '<p class="oa-note">This site collects nothing about you.</p>';
  }
  function renderReturn() {
    var last = store.acts[store.acts.length - 1];
    var a = ACTS[last.id];
    var nextId = a ? a.next : "check-listing";
    renderAct(nextId);
    var back = document.createElement("p");
    back.className = "oa-act";
    back.innerHTML = "<strong>Welcome back.</strong> <span></span>";
    back.querySelector("span").textContent =
      "Your act still stands: on " + fmtDate(last.date) + " you " +
      (a ? a.past : "did one small act") +
      ". If you filed it, it stands in the public record under the name you chose. " +
      "This page knows only because this device remembers; nothing was sent anywhere. " +
      "Here is the next step on the ladder, when you are ready.";
    bodyEl.insertBefore(back, bodyEl.firstChild);
  }
  function complete() {
    if (!current) { return; }
    var a = ACTS[current];
    store.acts.push({ id: current, date: todayIso() });
    save();
    bodyEl.innerHTML =
      '<p class="oa-thanks" tabindex="-1">Thank you<span id="oa-thanks-name"></span>.</p>' +
      '<p class="oa-act"><strong>What it did:</strong> <span class="oa-effect"></span></p>' +
      '<p class="oa-act">It stands when it lands in the record: the place the act opened is where it files, ' +
      'in the open, under your name, a stage name, or no name, as you chose.</p>' +
      '<p class="oa-row"><label class="oa-note" for="oa-name">Be thanked by name here? Write it once. It stays on this device.</label></p>' +
      '<p class="oa-row"><input class="oa-name" id="oa-name" type="text" maxlength="40" autocomplete="off">' +
      '<button type="button" class="oa-btn" id="oa-name-btn">Use this name</button></p>' +
      '<p class="oa-row"><a class="oa-go" id="oa-next" target="_blank" rel="noopener"></a>' +
      '<button type="button" class="oa-btn" id="oa-pass">Hand this act to one person</button>' +
      '<button type="button" class="oa-btn" id="oa-undo">Take it back</button></p>' +
      '<p class="oa-note" id="oa-pass-note"></p>';
    bodyEl.querySelector(".oa-effect").textContent = a.effect;
    var next = ACTS[a.next];
    var nextEl = document.getElementById("oa-next");
    nextEl.setAttribute("href", next.href);
    nextEl.textContent = "Next act: " + next.t + ", " + next.m.toLowerCase();
    applyName();
    document.getElementById("oa-name-btn").addEventListener("click", function () {
      var v = document.getElementById("oa-name").value.replace(/[<>&]/g, "").trim();
      store.name = v.slice(0, 40);
      save();
      applyName();
    });
    document.getElementById("oa-pass").addEventListener("click", function () {
      var note = document.getElementById("oa-pass-note");
      var payload = { title: "Topsoil Commons", text: a.t + ", " + a.m.toLowerCase() + ". One small act at Topsoil Commons.", url: a.href };
      if (navigator.share) { navigator.share(payload).catch(function () {}); return; }
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(payload.text + " " + payload.url).then(
          function () { note.textContent = "Copied. Hand it to one person."; },
          function () { note.textContent = "Copy this link: " + payload.url; });
      } else { note.textContent = "Copy this link: " + payload.url; }
    });
    document.getElementById("oa-undo").addEventListener("click", function () {
      store.acts.pop();
      save();
      renderAct(current);
    });
    var th = bodyEl.querySelector(".oa-thanks");
    if (th && th.focus) { th.focus(); }
  }
  function applyName() {
    var el = document.getElementById("oa-thanks-name");
    if (el) { el.textContent = store.name ? ", " + store.name : ""; }
    var input = document.getElementById("oa-name");
    if (input && store.name) { input.value = store.name; }
  }
  function actForDoor(num) {
    if (!(num in DOOR_ACT)) { return; }
    if (DOOR_ACT[num] === null) { renderRest(); } else { renderAct(DOOR_ACT[num]); }
  }

  setWitness();
  if (store.acts.length) { renderReturn(); } else {
    if (store.visits > 1) {
      var rot = ["check-listing", "check-claim", "witness"];
      renderAct(rot[(dayOfYear() + store.visits) % rot.length]);
    } else { renderAct("check-listing"); }
  }
  var doors = document.querySelectorAll(".frontdoors details");
  for (var i = 0; i < doors.length; i++) {
    (function (d) {
      d.addEventListener("toggle", function () {
        if (d.open) { actForDoor(d.id.replace("home-door-", "")); }
      });
    })(doors[i]);
  }
  function doorFromHash() {
    var m = window.location.hash.match(/^#door-(\d)$/);
    if (m) { actForDoor(m[1]); }
    var h = window.location.hash.match(/^#home-door-(\d)$/);
    if (h) { actForDoor(h[1]); }
  }
  doorFromHash();
  window.addEventListener("hashchange", doorFromHash);
})();
