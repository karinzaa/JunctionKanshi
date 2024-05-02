if ("serviceWorker" in navigator) {
  window.addEventListener("load", function () {
    navigator.serviceWorker
      .register("sw.js")
      .then((res) => console.log("service worker registered: " + res.scope))
      .catch((err) => console.log("service worker not registered", err));
  });
}
