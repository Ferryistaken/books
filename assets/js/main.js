(() => {
  // Theme switch
  const body = document.body;
  const lamp = document.getElementById("mode");
  const data = body.getAttribute("data-theme");

  const initTheme = (state) => {
    if (state === "dark") {
      body.setAttribute("data-theme", "dark");
    } else if (state === "light") {
      body.removeAttribute("data-theme");
    } else {
      localStorage.setItem("theme", data);
    }
  };

  const toggleTheme = (state) => {
    if (state === "dark") {
      localStorage.setItem("theme", "light");
      body.removeAttribute("data-theme");
    } else if (state === "light") {
      localStorage.setItem("theme", "dark");
      body.setAttribute("data-theme", "dark");
    } else {
      initTheme(state);
    }
  };

  initTheme(localStorage.getItem("theme"));

  lamp.addEventListener("click", () =>
    toggleTheme(localStorage.getItem("theme"))
  );

  // Blur the content when the menu is open
  const cbox = document.getElementById("menu-trigger");

  cbox.addEventListener("change", function () {
    const area = document.querySelector(".wrapper");
    this.checked
      ? area.classList.add("blurry")
      : area.classList.remove("blurry");
  });
})();

// Only trigger if service workers are supported in browser.
if ('serviceWorker' in navigator) {
  // Wait until window is loaded before registering.
  window.addEventListener('load', () => {
    // Register the service worker with "/" as it's scope.
    navigator.serviceWorker.register('/sw.js', { scope: '/' })
      // Output success/failure of registration.
      .then(() => console.log('SW registered'))
      .catch(() => console.error('SW registration failed'));
  });
}
