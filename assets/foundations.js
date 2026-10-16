(function(){
  var reduced = !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
  function animate(dur, step, done){
    if (reduced || dur <= 0) { step(1); if (done) { done(); } return; }
    var t0 = null;
    function frame(ts){
      if (!t0) { t0 = ts; }
      var p = Math.min(1, (ts - t0) / dur);
      step(p);
      if (p < 1) { requestAnimationFrame(frame); }
      else if (done) { done(); }
    }
    requestAnimationFrame(frame);
  }
  function finish(btn, result){
    result.hidden = false;
    btn.disabled = false;
    btn.textContent = 'Run again';
  }

  /* Cash transfers, Kenya: 193 marks, one per dollar. The starting value,
     158, stands filled before any run. The rise, 35, stands outlined and
     fills as the run counts up to 193. */
  (function(){
    var marks = document.getElementById('cash-marks');
    var num = document.getElementById('cash-num');
    var btn = document.getElementById('cash-btn');
    var result = document.getElementById('cash-result');
    var cells = [];
    for (var i = 0; i < 193; i++) {
      var s = document.createElement('span');
      if (i < 158) s.className = 'on';
      marks.appendChild(s);
      cells.push(s);
    }
    btn.addEventListener('click', function(){
      btn.disabled = true;
      result.hidden = true;
      animate(1500, function(p){
        var lit = Math.round(35 * p);
        num.textContent = String(158 + Math.round(35 * p));
        for (var j = 0; j < 35; j++) { cells[158 + j].className = j < lit ? 'on' : ''; }
      }, function(){ finish(btn, result); });
    });
  })();

  /* False news travels faster: false reaches 1,500 about six times sooner. */
  (function(){
    var fNum = document.getElementById('race-false-num');
    var tNum = document.getElementById('race-true-num');
    var fFill = document.getElementById('race-false-fill');
    var tFill = document.getElementById('race-true-fill');
    var btn = document.getElementById('race-btn');
    var result = document.getElementById('race-result');
    btn.addEventListener('click', function(){
      btn.disabled = true;
      result.hidden = true;
      var doneCount = 0;
      function oneDone(){ if (++doneCount === 2) { finish(btn, result); } }
      animate(1000, function(p){
        var v = Math.round(1500 * p);
        fNum.textContent = v.toLocaleString('en-US');
        fFill.style.width = (100 * p) + '%';
      }, oneDone);
      animate(6000, function(p){
        var v = Math.round(1500 * p);
        tNum.textContent = v.toLocaleString('en-US');
        tFill.style.width = (100 * p) + '%';
      }, oneDone);
    });
  })();

  /* Connection and survival: each tap adds ten ties among 100 people. */
  (function(){
    var people = document.getElementById('ties-people');
    var svg = document.getElementById('ties-svg');
    var num = document.getElementById('ties-num');
    var conn = document.getElementById('ties-conn');
    var index = document.getElementById('ties-index');
    var btn = document.getElementById('ties-btn');
    var result = document.getElementById('ties-result');
    var seed = 7;
    function rand(){
      seed |= 0; seed = seed + 0x6D2B79F5 | 0;
      var t = Math.imul(seed ^ seed >>> 15, 1 | seed);
      t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
      return ((t ^ t >>> 14) >>> 0) / 4294967296;
    }
    function center(i){ return [ (i % 10) * 10 + 5, Math.floor(i / 10) * 10 + 5 ]; }
    var cells = [];
    for (var i = 0; i < 100; i++) {
      var cell = document.createElement('div');
      cell.className = 'cell';
      var dot = document.createElement('span');
      cell.appendChild(dot);
      people.appendChild(cell);
      cells.push(dot);
    }
    /* A fixed order in which people become connected, and fixed tie pairs. */
    var perm = [];
    for (var a = 0; a < 100; a++) { perm.push(a); }
    for (var b = 99; b > 0; b--) {
      var k = Math.floor(rand() * (b + 1));
      var tmp = perm[b]; perm[b] = perm[k]; perm[k] = tmp;
    }
    var pairs = [];
    for (var q = 0; q < 100; q++) {
      var x = Math.floor(rand() * 100);
      var y = Math.floor(rand() * 100);
      if (y === x) { y = (y + 1) % 100; }
      pairs.push([x, y]);
    }
    var lines = [];
    var NS = 'http://www.w3.org/2000/svg';
    for (var m = 0; m < 100; m++) {
      var ln = document.createElementNS(NS, 'line');
      var c1 = center(pairs[m][0]);
      var c2 = center(pairs[m][1]);
      ln.setAttribute('x1', c1[0]); ln.setAttribute('y1', c1[1]);
      ln.setAttribute('x2', c2[0]); ln.setAttribute('y2', c2[1]);
      ln.style.display = 'none';
      svg.appendChild(ln);
      lines.push(ln);
    }
    var ties = 0;
    function render(){
      num.textContent = String(ties);
      conn.textContent = String(Math.min(100, ties));
      index.textContent = String(100 + Math.round(50 * ties / 100));
      for (var j = 0; j < 100; j++) {
        lines[j].style.display = j < ties ? '' : 'none';
        cells[perm[j]].className = j < ties ? 'on' : '';
      }
    }
    btn.addEventListener('click', function(){
      if (ties >= 100) { return; }
      ties = Math.min(100, ties + 10);
      render();
      if (ties >= 100) {
        result.hidden = false;
        btn.disabled = true;
        btn.textContent = 'Done';
      }
    });
  })();

  /* Citizen report cards, Uganda: the after count falls by one third. */
  (function(){
    var num = document.getElementById('cards-num');
    var fill = document.getElementById('cards-fill');
    var btn = document.getElementById('cards-btn');
    var result = document.getElementById('cards-result');
    btn.addEventListener('click', function(){
      btn.disabled = true;
      result.hidden = true;
      animate(1200, function(p){
        var v = Math.round(100 - 33 * p);
        num.textContent = String(v);
        fill.style.width = v + '%';
      }, function(){ finish(btn, result); });
    });
  })();

  /* AI help and novices: both rise, the novice by more. */
  (function(){
    var aNum = document.getElementById('ai-avg-num');
    var nNum = document.getElementById('ai-nov-num');
    var aFill = document.getElementById('ai-avg-fill');
    var nFill = document.getElementById('ai-nov-fill');
    var btn = document.getElementById('ai-btn');
    var result = document.getElementById('ai-result');
    btn.addEventListener('click', function(){
      btn.disabled = true;
      result.hidden = true;
      animate(1600, function(p){
        var a = Math.round(100 + 14 * p);
        var n = Math.round(100 + 34 * p);
        aNum.textContent = String(a);
        nNum.textContent = String(n);
        aFill.style.width = (a / 134 * 100) + '%';
        nFill.style.width = (n / 134 * 100) + '%';
      }, function(){ finish(btn, result); });
    });
  })();
})();
