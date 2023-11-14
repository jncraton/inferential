function initializePlayground() {
  document.getElementById('status').textContent = 'Starting up web server'
  setTimeout(function () {
    document.getElementById('status').textContent = 'Downloading assets'
    setTimeout(function () {
      document.getElementById('status').textContent = 'Initializing server'
      setTimeout(function () {
        document.getElementById('status').textContent = 'Redirecting'
        setTimeout(function () {
          window.location.href = '/playground'
        }, 12)
      }, 600)
    }, 1500)
  }, 450)
}

initializePlayground()
