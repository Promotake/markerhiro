/* Optional model inspection without an AR marker or webcam. */
(function () {
  'use strict';
  function init() {
    const model = document.querySelector('#previewRobot');
    const label = document.querySelector('#previewStatus');
    const plus = document.querySelector('#zoomIn');
    const minus = document.querySelector('#zoomOut');
    const toggle = document.querySelector('#pausePreview');
    let size = 1.12;
    let rotating = true;

    model.addEventListener('model-loaded', () => { label.textContent = '3D-модель загружена из локального GLB'; });
    model.addEventListener('model-error', (e) => {
      label.textContent = 'Ошибка загрузки модели. Запустите сервер через run_local.bat.';
      console.error(e);
    });
    function zoom(step) {
      size = Math.max(0.65, Math.min(1.70, Math.round((size + step)*100)/100));
      model.setAttribute('scale', `${size} ${size} ${size}`);
    }
    plus.addEventListener('click', () => zoom(0.12));
    minus.addEventListener('click', () => zoom(-0.12));
    toggle.addEventListener('click', () => {
      rotating = !rotating;
      const animation = model.components['animation__rotate'];
      if (animation) {
        if (rotating) animation.resumeAnimation(); else animation.pauseAnimation();
      }
      toggle.textContent = rotating ? '⏸' : '▶';
      toggle.setAttribute('aria-label', rotating ? 'Остановить вращение' : 'Продолжить вращение');
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
