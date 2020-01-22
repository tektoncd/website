function getKatacodaLnk (katacodaSrc) {
  const elems = katacodaSrc.split('/');
  return `${elems[0]}/scenarios/${elems[1]}`;
}

function openModal () {
  const modal = document.getElementById('tutorialModal');
  const katacodaSrc = modal.getAttribute('data-katacoda-src');
  const katacodaLnk = getKatacodaLnk(katacodaSrc);
  const githubLnk = modal.getAttribute('data-github-src');
  const qwiklabsLnk = modal.getAttribute('data-qwiklabs-src');

  modal.classList.add('show');
  modal.setAttribute('style', 'display: block;');
  document.getElementsByClassName('td-section')[0].classList.add('modal-open');
  const backdrop = document.createElement('div');
  backdrop.classList.add('modal-backdrop', 'fade', 'show');
  document.getElementsByTagName('body')[0].appendChild(backdrop);
  document.getElementById('katacoda-button').setAttribute('href', `https://katacoda.com/${katacodaLnk}`);
  document.getElementById('github-button').setAttribute('href', `https://github.com/${githubLnk}`);
  document.getElementById('qwiklabs-button').setAttribute('href', `https://qwiklabs.com/${qwiklabsLnk}`);

  const scenario = document.getElementById('embedded-katacoda-scenario');
  const katacodaCanvasNode = document.createElement('div');
  katacodaCanvasNode.setAttribute('id', 'katacoda-scenario');
  katacodaCanvasNode.setAttribute('data-katacoda-id', katacodaSrc);
  katacodaCanvasNode.setAttribute('data-katacoda-color', '004d7f');
  katacodaCanvasNode.setAttribute('style', 'height: 900px; padding-top: 20px;');
  const katacodaScriptNode = document.createElement('script');
  katacodaScriptNode.setAttribute('id', 'katacoda-scenario-script');
  katacodaScriptNode.setAttribute('src', '//katacoda.com/embed.js');
  scenario.appendChild(katacodaCanvasNode);
  scenario.appendChild(katacodaScriptNode);
}

function closeModal () {
  const modal = document.getElementById('tutorialModal');

  document.getElementById('embedded-katacoda-scenario').removeChild(
    document.getElementById('katacoda-scenario')
  );
  document.getElementById('embedded-katacoda-scenario').removeChild(
    document.getElementById('katacoda-scenario-script')
  );
  modal.classList.remove('show');
  modal.setAttribute('style', 'display: none;');
  document.getElementsByClassName('td-section')[0].classList.remove('modal-open');
  const backdrop = document.getElementsByClassName('modal-backdrop')[0];
  document.getElementsByTagName('body')[0].removeChild(backdrop);
  document.getElementById('katacoda-button').removeAttribute('href');
  document.getElementById('github-button').removeAttribute('href');
  document.getElementById('qwiklabs-button').removeAttribute('href');
}
