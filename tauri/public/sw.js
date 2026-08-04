const CACHE_VERSION = 'v3'; // Переключаем на v3, чтобы снести старый кэш findendportal-v2
const CACHE_NAME = `findendportal-${CACHE_VERSION}`;

// В массиве оставляем только те файлы, которые РЕАЛЬНО лежат в твоей папке Tauri/public
const FILES_TO_CACHE = [
  '/FindEndPortal/',
  '/FindEndPortal/index.html',
  '/FindEndPortal/manifest.webmanifest',
  '/FindEndPortal/favicon-v2.png' // Указываем актуальное имя новой иконки
];

// Install - кеширует необходимые файлы
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(FILES_TO_CACHE);
    }).then(() => {
      return self.skipWaiting(); // Принудительно заставляем новый воркер активироваться, не дожидаясь закрытия вкладок
    }).catch(err => {
      console.warn('Cache.addAll error (проверь, все ли файлы существуют в public):', err);
    })
  );
});

// Fetch - для страницы сначала сеть (network-first), для остального - кеш, если доступно
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // Если в пути нет /FindEndPortal/, просто передаём запрос
  if (!url.pathname.startsWith('/FindEndPortal/')) {
    return;
  }

  // Навигационные запросы (открытие страницы): всегда сначала сеть,
  // чтобы пользователь получал свежий index.html. Кэш - только fallback оффлайн.
  if (request.mode === 'navigate') {
    event.respondWith(
      fetch(request)
        .then((response) => {
          if (!response || response.status !== 200) {
            return response;
          }

          // Обновляем закешированную страницу свежим ответом
          const responseToCache = response.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put('/FindEndPortal/', responseToCache);
            cache.put('/FindEndPortal/index.html', responseToCache);
          });

          return response;
        })
        .catch(() =>
          caches.match(request).then((response) => {
            if (response) {
              return response;
            }
            return caches.match('/FindEndPortal/');
          })
        )
    );
    return;
  }

  event.respondWith(
    caches.match(request).then((response) => {
      if (response) {
        return response;
      }

      return fetch(request)
        .then((response) => {
          // Не кешируем неуспешные запросы
          if (!response || response.status !== 200) {
            return response;
          }

          // Кешируем успешный ответ
          const responseToCache = response.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(request, responseToCache);
          });

          return response;
        })
        .catch(() => {
          // Если нет интернета, возвращаем кеш
          return caches.match(request);
        });
    })
  );
});

// Activate - полностью очищает старое хранилище findendportal-v2
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            return caches.delete(cacheName); // Удаляем v1 намертво
          }
        })
      );
    }).then(() => {
      return self.clients.claim(); // Сразу берем под контроль все открытые страницы
    })
  );
});