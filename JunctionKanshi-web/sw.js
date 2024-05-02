/* 
Copyright (c) 2023 Parking Miru Web Engine By Karin Vitoonkijvanit

*** Unauthorized modification of files in Parking Miru Web Engine
shall not be held liable for any damages or errors. and
It is a disruption of Parking Miru Web Engine's system. *** 
*/

const CACHE_NAME = "JunctionKanshi-0.0.2";
const OFFLINE_URL = "offline.html";
const assets = [
  "/",
  "/index.html",
  "/live.html",
  "/offline.html",
  // css
  "/css/mobile.css",
  // js
  "/js/app.js",
  "/js/loader.js",
  "/js/mobileScript.js",
  "/js/num.js",
  "/js/wow.min.js",
  // img
  "/img/JunctionKanshiIcon.ico",
  "/img/JunctionKanshiIcon.png",
  "/img/JunctionKanshiIcon144x144.png",
  "/img/JunctionKanshiIcon512x512.png",
  "/img/ring-resize-white-36.svg",
];

self.addEventListener("install", (installEvent) => {
  installEvent.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      cache.addAll(assets);
      cache.add(new Request(OFFLINE_URL, { cache: "reload" }));
    })
  );
});

self.addEventListener("fetch", (event) => {
  // Only call event.respondWith() if this is a navigation request
  // for an HTML page.
  if (event.request.mode === "navigate") {
    event.respondWith(
      (async () => {
        try {
          // First, try to use the navigation preload response if it's
          // supported.
          const preloadResponse = await event.preloadResponse;
          if (preloadResponse) {
            return preloadResponse;
          }

          // Always try the network first.
          const networkResponse = await fetch(event.request);
          return networkResponse;
        } catch (error) {
          // catch is only triggered if an exception is thrown, which is
          // likely due to a network error.
          // If fetch() returns a valid HTTP response with a response code in
          // the 4xx or 5xx range, the catch() will NOT be called.
          console.log("Fetch failed; returning offline page instead.", error);

          const cache = await caches.open(CACHE_NAME);
          const cachedResponse = await cache.match(OFFLINE_URL);
          return cachedResponse;
        }
      })()
    );
  }
});
