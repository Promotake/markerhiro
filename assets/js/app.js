/* LR4: AR.js marker events and camera/asset status. */
(() => {
  'use strict';
  function init() {
    const marker = document.getElementById('hiroMarker');
    const robot = document.getElementById('robot');
    const scene = document.getElementById('arScene');
    const asset = document.getElementById('astrobotAsset');
    const statusRoot = document.getElementById('status');
    const statusText = document.getElementById('statusText');
    const spinButton = document.getElementById('toggleSpin');
    if (!marker || !robot || !scene || !statusRoot || !statusText) return;

    let found = false;
    let loaded = false;
    let cameraReady = false;
    let spin = true;
    let problem = '';
    function status(kind, message) {
      statusRoot.className = 'status ' + kind;
      statusText.textContent = message;
    }
    function refresh() {
      if (problem) return status('error', problem);
      if (!window.isSecureContext) return status('error', 'Для камеры нужен HTTPS или localhost.');
      if (found) return status('found', loaded ? 'Маркер найден! Робот привязан к HIRO.' : 'Маркер найден. Загружается робот…');
      if (cameraReady) return status('waiting', loaded ? 'Камера запущена. Ищем HIRO…' : 'Камера запущена. Загружается робот…');
      return status('loading', loaded ? 'Робот готов. Запуск AR-трекера…' : 'Запускаем камеру и робот…');
    }
    function onFound() { found = true; refresh(); }
    function onLost() { found = false; refresh(); }
    marker.addEventListener('markerFound', onFound);
    marker.addEventListener('markerLost', onLost);
    // Some AR.js versions dispatch markerFound on the scene rather than the marker.
    scene.addEventListener('markerFound', ev => { if (ev.target === marker) onFound(); });
    scene.addEventListener('markerLost', ev => { if (ev.target === marker) onLost(); });
    robot.addEventListener('model-loaded', () => { loaded = true; refresh(); });
    robot.addEventListener('model-error', () => { problem = 'Ошибка загрузки 3D-модели. Проверь assets/models/astrabot.glb'; refresh(); });
    asset?.addEventListener('error', () => { problem = 'Не загрузился astrobot.glb'; refresh(); });
    // AR.js raises camera-init and arjs-video-loaded on window/document depending on build.
    function onCamera() { cameraReady = true; refresh(); }
    for (const target of [window, document, scene]) {
      target.addEventListener('camera-init', onCamera);
      target.addEventListener('arjs-video-loaded', onCamera);
      target.addEventListener('camera-error', e => { problem = 'Нет доступа к камере: ' + (e.detail?.message || e.message || 'проверь настройки'); refresh(); });
    }
    scene.addEventListener('loaded', refresh);
    spinButton?.addEventListener('click', () => {
      spin = !spin;
      const anim = robot.components['animation__spin'];
      if (anim) { if (spin) anim.resumeAnimation(); else anim.pauseAnimation(); }
      spinButton.innerHTML = spin ? '⏸ <span>Вращение</span>' : '▶ <span>Вращение</span>';
    });
    refresh();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
