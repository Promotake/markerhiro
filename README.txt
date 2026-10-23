LR4: исправление наложения камеры и робота на iPhone

Причина предыдущей регрессии: videoTexture=true был включен при работе с
маркерной AR. В этом исправлении возвращен videoTexture=false,
а стандартный видеопоток AR.js расположен ПОД прозрачным WebGL-canvas.
Камера и робот используют ОДИН видеопоток.

Публикация:
1. В репозитории https://github.com/promotake/markerhiro замените
   index.html и hiro_preset.html из этого патча.
2. Добавьте test.html в корень (необязательно, только для проверки).
3. Для полной замены добавьте папки assets/models и marker из полного архива.
4. Проверьте, что в корне доступны marker/square_marker.patt,
   marker/square_marker.png и assets/models/astrabot.glb.
5. После Commit changes на телефоне откройте:
   https://promotake.github.io/markerhiro/?v=overlay5
6. На компьютере выведите новый square_marker.png, не старый HIRO.

На главной странице НЕТ надписей и кнопок - только камера и робот
над маркером. Отдельная страница test.html показывает диагностику:
https://promotake.github.io/markerhiro/test.html?v=overlay5

Проверить реальную камеру iPhone можно только после публикации на GitHub Pages.
