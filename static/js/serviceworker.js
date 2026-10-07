const CACHE_NAME = 'hangarin-cache-v1';

const PRECACHE = [
  '/offline/',
  '/static/css/bootstrap.min.css',
  '/static/css/ready.css',
  '/static/img/icon-192.png',
];

self.addEventListener('install', function (event) {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(function (cache) {
        // allSettled: one missing file won't break the install
        return Promise.allSettled(PRECACHE.map(function (url) {
          return cache.add(url);
        }));
      })
      .then(function () { return self.skipWaiting(); })
  );
});

self.addEventListener('activate', function (event) {
  event.waitUntil(
    caches.keys()
      .then(function (keys) {
        return Promise.all(
          keys.filter(function (k) { return k !== CACHE_NAME; })
              .map(function (k) { return caches.delete(k); })
        );
      })
      .then(function () { return self.clients.claim(); })
  );
});

self.addEventListener('fetch', function (event) {
  var req = event.request;
  if (req.method !== 'GET') return;

  var url = new URL(req.url);
  if (url.origin !== location.origin) return;

  // Static files: cache first
  if (url.pathname.startsWith('/static/')) {
    event.respondWith(
      caches.match(req).then(function (cached) {
        return cached || fetch(req).then(function (res) {
          var copy = res.clone();
          caches.open(CACHE_NAME).then(function (c) { c.put(req, copy); });
          return res;
        });
      })
    );
    return;
  }

  // Pages: always try the network, show the offline page if it fails
  if (req.mode === 'navigate') {
    event.respondWith(
      fetch(req).catch(function () { return caches.match('/offline/'); })
    );
  }
});