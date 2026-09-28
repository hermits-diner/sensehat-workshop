// 슬라이드 동작: 크기 맞춤, 넘기기, 코드 색, Scratch 블록, QR, 무지개 LED
const slides = [...document.querySelectorAll('.slide')];
const stage = document.getElementById('stage');
let cur = 0;

// 1600×900 무대를 창 크기에 맞춘다
function fit() {
  const s = Math.min(innerWidth / 1600, innerHeight / 900);
  stage.style.transform = `scale(${s}) translate(-50%, -50%)`;
}
addEventListener('resize', fit);
fit();

function show(n) {
  cur = Math.max(0, Math.min(slides.length - 1, n));
  slides.forEach((s, i) => s.classList.toggle('active', i === cur));
  document.getElementById('count').textContent = `${cur + 1} / ${slides.length}`;
  history.replaceState(null, '', '#' + (cur + 1));
  fitBlocks(slides[cur]);
}

addEventListener('keydown', e => {
  if (['ArrowRight', 'PageDown', ' ', 'Enter'].includes(e.key)) show(cur + 1);
  else if (['ArrowLeft', 'PageUp', 'Backspace'].includes(e.key)) show(cur - 1);
  else if (e.key === 'Home') show(0);
  else if (e.key === 'End') show(slides.length - 1);
  else if (e.key === 'f' || e.key === 'F') document.fullscreenElement ? document.exitFullscreen() : document.documentElement.requestFullscreen();
  else if (e.key === 'n' || e.key === 'N') document.body.classList.toggle('show-notes');
  else return;
  e.preventDefault();
});
addEventListener('click', e => { if (!e.target.closest('a')) show(cur + (e.clientX > innerWidth / 3 ? 1 : -1)); });

// Python 코드에 색 입히기 (주석, 문자열, 키워드, 숫자, 함수 이름)
for (const el of document.querySelectorAll('pre.code:not(.term) code')) {
  const re = /(#.*$)|("[^"]*"|'[^']*')|\b(from|import|def|for|in|while|if|elif|else|True|False|and|or|not|return)\b|\b(\d+(?:\.\d+)?)\b|\b([a-z_]\w*)(?=\()/gm;
  const esc = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  const src = el.textContent;
  let out = '', last = 0, m;
  while ((m = re.exec(src))) {
    out += esc(src.slice(last, m.index));
    const cls = m[1] ? 'c' : m[2] ? 's' : m[3] ? 'k' : m[4] ? 'n' : 'f';
    out += `<span class="${cls}">${esc(m[0])}</span>`;
    last = re.lastIndex;
  }
  el.innerHTML = out + esc(src.slice(last));
}

// Scratch 블록 그리기 → 상자에 맞게 크기 조절
scratchblocks.renderMatching('pre.blocks', { style: 'scratch3', languages: ['en'], scale: 1 });
// 코드가 칸보다 넓으면 글씨를 줄인다
function fitCode(slide) {
  for (const pre of slide.querySelectorAll('pre.code')) {
    let size = parseFloat(getComputedStyle(pre).fontSize);
    while (pre.scrollWidth > pre.clientWidth + 1 && size > 14) pre.style.fontSize = (size -= 1) + 'px';
  }
}
function fitBlocks(slide) {
  fitCode(slide);
  for (const wrap of slide.querySelectorAll('.sbwrap')) {
    const svg = wrap.querySelector('svg');
    if (!svg) continue;
    if (!svg.dataset.w) { svg.dataset.w = svg.getAttribute('width'); svg.dataset.h = svg.getAttribute('height'); }
    const w = +svg.dataset.w, h = +svg.dataset.h;
    const maxW = wrap.clientWidth - 28, maxH = 440;
    const k = Math.min(1.6, maxW / w, maxH / h);
    svg.setAttribute('width', w * k); svg.setAttribute('height', h * k);
    svg.setAttribute('viewBox', `0 0 ${w} ${h}`);
  }
}

// QR코드 (영상·자료 링크를 휴대폰으로)
for (const el of document.querySelectorAll('.qrcode')) {
  new QRCode(el, { text: el.dataset.url, width: 210, height: 210, correctLevel: QRCode.CorrectLevel.M });
}

// 부팅 무지개 LED
for (const el of document.querySelectorAll('.led.rainbow')) {
  for (let y = 0; y < 8; y++) for (let x = 0; x < 8; x++) {
    const i = document.createElement('i');
    i.style.setProperty('--c', `hsl(${(x + y) * 26}, 100%, 55%)`);
    el.appendChild(i);
  }
}

show((parseInt(location.hash.slice(1)) || 1) - 1);
