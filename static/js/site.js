/* Comportamentos do site: tema claro/escuro, abas dos prints,
   copiar e-mail e o terminal "digitando" no topo.
   Cada parte confere se o elemento existe, porque nem toda página tem todos. */
(function () {
  /* ---------- Tema claro/escuro ----------
     O tema salvo já foi aplicado por um script curtinho no <head> (base.html),
     antes da página aparecer. Aqui só cuidamos do botão. */
  var root = document.documentElement;
  var btn = document.getElementById('theme-btn');

  function temaDoSistema() {
    try { return matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'; }
    catch (e) { return 'light'; }
  }
  function temaAtual() { return root.getAttribute('data-theme') || temaDoSistema(); }
  function pintarBotao() {
    if (!btn) return;
    var escuro = temaAtual() === 'dark';
    // Ícone de <svg> não aceita .hidden = true (isso só existe em elementos HTML),
    // por isso usamos toggleAttribute, que liga/desliga o atributo hidden de verdade.
    document.getElementById('ic-moon').toggleAttribute('hidden', escuro);
    document.getElementById('ic-sun').toggleAttribute('hidden', !escuro);
    document.getElementById('theme-lbl').textContent = escuro ? 'claro' : 'escuro';
  }

  if (btn) {
    pintarBotao();
    btn.addEventListener('click', function () {
      var novo = temaAtual() === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', novo);
      try { localStorage.setItem('tl-theme', novo); } catch (e) {}
      pintarBotao();
    });
    try { matchMedia('(prefers-color-scheme: dark)').addEventListener('change', pintarBotao); } catch (e) {}
  }

  /* ---------- Abas dos prints ----------
     Cada grupo de abas tem data-tabs="slug"; as imagens do mesmo projeto
     têm data-g="slug". Clicar numa aba mostra só a imagem com o mesmo data-i. */
  document.querySelectorAll('.tabs').forEach(function (grupo) {
    var g = grupo.getAttribute('data-tabs');
    grupo.querySelectorAll('button').forEach(function (aba) {
      aba.addEventListener('click', function () {
        var i = aba.getAttribute('data-i');
        grupo.querySelectorAll('button').forEach(function (x) {
          x.setAttribute('aria-pressed', x === aba ? 'true' : 'false');
        });
        document.querySelectorAll('img[data-g="' + g + '"]').forEach(function (img) {
          img.hidden = img.getAttribute('data-i') !== i;
        });
      });
    });
  });

  /* ---------- Copiar e-mail ---------- */
  var botaoEmail = document.getElementById('copy-email');
  if (botaoEmail) {
    var rotulo = document.getElementById('email-lbl');
    var email = botaoEmail.getAttribute('data-email');
    botaoEmail.addEventListener('click', function () {
      var deuCerto = function () {
        rotulo.textContent = 'e-mail · copiado';
        setTimeout(function () { rotulo.textContent = 'e-mail · copiar'; }, 1800);
      };
      var selecionar = function () {  // plano B: seleciona o texto pra pessoa copiar
        var r = document.createRange();
        r.selectNodeContents(document.getElementById('email-text'));
        var s = getSelection(); s.removeAllRanges(); s.addRange(r);
      };
      try { navigator.clipboard.writeText(email).then(deuCerto, selecionar); }
      catch (e) { selecionar(); }
    });
  }

  /* ---------- Terminal digitando ----------
     O HTML do terminal já vem completo do Django (funciona sem JavaScript).
     Aqui a gente apaga e "redigita" linha por linha. */
  var term = document.getElementById('term');
  if (!term) return;
  var reduzirMovimento = false;
  try { reduzirMovimento = matchMedia('(prefers-reduced-motion: reduce)').matches; } catch (e) {}
  if (reduzirMovimento) return;

  var linhas = Array.prototype.slice.call(term.querySelectorAll('.ln'));
  var ultima = linhas.pop();  // a linha com o cursor piscando fica pro final
  var dados = linhas.map(function (l) {
    var ehComando = l.firstElementChild && l.firstElementChild.classList.contains('p');
    return { html: l.innerHTML, classe: l.className, cmd: ehComando,
             texto: ehComando ? l.textContent.replace(/^\$\s*/, '') : '' };
  });
  term.innerHTML = '';
  var i = 0;

  function proxima() {
    if (i >= dados.length) { term.appendChild(ultima); return; }
    var d = dados[i++];
    var ln = document.createElement('div');
    ln.className = d.classe;
    term.appendChild(ln);
    if (d.cmd) {
      ln.innerHTML = '<span class="p">$</span> <span class="tx"></span><span class="caret"></span>';
      var tx = ln.querySelector('.tx'), k = 0;
      (function digitar() {
        if (k <= d.texto.length) {
          tx.textContent = d.texto.slice(0, k++);
          setTimeout(digitar, 45 + Math.random() * 45);
        } else {
          ln.innerHTML = d.html;
          setTimeout(proxima, 260);
        }
      })();
    } else {
      ln.innerHTML = d.html;
      setTimeout(proxima, 110);
    }
  }
  setTimeout(proxima, 400);
})();
