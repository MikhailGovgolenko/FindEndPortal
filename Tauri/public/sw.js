const CACHE_VERSION = 'v1';
const CACHE_NAME = `findendportal-${CACHE_VERSION}`;

const FILES_TO_CACHE = [
  '/FindEndPortal/',
  '/FindEndPortal/index.html',
  '/FindEndPortal/manifest.webmanifest',
  '/FindEndPortal/favicon.png',
  '/FindEndPortal/apple-touch-icon.png'
];

// Install - кеширует необходимые файлы
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(FILES_TO_CACHE).catch(err => {
        console.warn('Cache.addAll error:', err);
      });
    })
  );
});

// Fetch - возвращает кеш, если доступно
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // Если в пути нет /FindEndPortal/, просто передаём запрос
  if (!url.pathname.startsWith('/FindEndPortal/')) {
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

// Activate - очищает старые кеши
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});
