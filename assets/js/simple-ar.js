(() => {
  'use strict';
  function init() {
    const marker = document.getElementById('hiroMarker');
    const scene = document.getElementById('arScene');
    const robot = document.getElementById('robot');
    const asset = document.getElementById('astrobotAsset');
    const box = document.getElementById('status');
    const txt = document.getElementById('statusText');
    if (!marker || !scene || !txt || !box) return;

    let found = false;
    let loaded = false;
    let camera = false;
    let error = '';

    const setStatus = (kind, message) => {
      box.className = 'status' + (kind ? ' ' + kind : '');
      txt.textContent = message;
    };
    const refresh = () => {
      if (error) return setStatus('error', error);
      if (!window.isSecureContext) return setStatus('error', 'Для камеры нужен HTTPS или localhost.');
      if (found) return setStatus('found', loaded ? 'Маркер найден. Робот стоит на маркере.' : 'Маркер найден. Модель ещё загружается…');
      if (camera) return setStatus('', loaded ? 'Камера работает. Наведите на HIRO.' : 'Камера работает. Загружается модель…');
      return setStatus('', loaded ? 'Модель готова. Запуск AR…' : 'Запускаем камеру и модель…');
    };

    const onFound = () => { found = true; refresh(); };
    const onLost = () => { found = false; refresh(); };

    marker.addEventListener('markerFound', onFound);
    marker.addEventListener('markerLost', onLost);
    scene.addEventListener('markerFound', e => { if (e.target === marker) onFound(); });
    scene.addEventListener('markerLost', e => { if (e.target === marker) onLost(); });
    robot.addEventListener('model-loaded', () => { loaded = true; refresh(); });
    robot.addEventListener('model-error', () => { error = 'Ошибка загрузки модели astrobot.glb'; refresh(); });
    asset?.addEventListener('error', () => { error = 'Не удалось загрузить astrobot.glb'; refresh(); });

    const onCamera = () => { camera = true; refresh(); };
    [window, document, scene].forEach(t => {
      t.addEventListener('camera-init', onCamera);
      t.addEventListener('arjs-video-loaded', onCamera);
      t.addEventListener('camera-error', e => {
        error = 'Нет доступа к камере: ' + (e.detail?.message || e.message || 'проверь настройки');
        refresh();
      });
    });

    scene.addEventListener('loaded', refresh);
    refresh();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
