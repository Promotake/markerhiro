/* Lab 4: AR marker state, camera requirements and a simple model control. */
(function () {
  'use strict';
  function init() {
    const statusEl = document.querySelector('#status');
    const statusText = document.querySelector('#statusText');
    const marker = document.querySelector('#hiroMarker');
    const robot = document.querySelector('#robot');
    const asset = document.querySelector('#astrobotAsset');
    const scene = document.querySelector('#arScene');
    const spinButton = document.querySelector('#toggleSpin');
    let markerVisible = false;
    let modelLoaded = false;
    let spinEnabled = true;

    function status(kind, text) {
      statusEl.className = 'status ' + kind;
      statusText.textContent = text;
    }
    function updateStatus() {
      if (!window.isSecureContext) {
        status('error', 'Камера телефона работает только через HTTPS (или localhost на ПК).');
      } else if (markerVisible && modelLoaded) {
        status('found', 'Маркер найден — 3D-модель привязана к нему!');
      } else if (markerVisible) {
        status('loading', 'Маркер найден. Загружается 3D-модель…');
      } else if (modelLoaded) {
        status('waiting', 'Модель готова. Покажите камере маркер HIRO.');
      } else {
        status('loading', 'Камера запускается, 3D-модель загружается…');
      }
    }

    marker.addEventListener('markerFound', function () {
      markerVisible = true;
      updateStatus();
    });
    marker.addEventListener('markerLost', function () {
      markerVisible = false;
      updateStatus();
    });
    robot.addEventListener('model-loaded', function () {
      modelLoaded = true;
      updateStatus();
    });
    robot.addEventListener('model-error', function (error) {
      console.error('Cannot load astrobot.glb', error);
      status('error', 'Не удалось загрузить astrobot.glb — проверьте сервер и путь к файлу.');
    });
    asset.addEventListener('error', function (error) {
      console.error('Asset loading error:', error);
      status('error', 'Файл модели не загружен. Не открывайте index.html через file://.');
    });
    scene.addEventListener('loaded', updateStatus);

    if (location.protocol === 'file:') {
      status('error', 'Нужен веб-сервер! На ПК запустите run_local.bat; на телефоне — HTTPS.');
    } else {
      updateStatus();
    }

    spinButton.addEventListener('click', function () {
      const anim = robot.components['animation__spin'];
      spinEnabled = !spinEnabled;
      if (anim) {
        if (spinEnabled) anim.resumeAnimation(); else anim.pauseAnimation();
      }
      spinButton.innerHTML = spinEnabled ? '⏸ <span>Вращение</span>' : '▶ <span>Вращение</span>';
      spinButton.setAttribute('aria-pressed', String(!spinEnabled));
    });

    window.addEventListener('unhandledrejection', function (event) {
      console.warn('AR initialization warning:', event.reason);
    });
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
