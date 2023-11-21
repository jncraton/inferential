function placeholderPlaygroundInitialization() {
  document.getElementById('status').textContent = 'Starting up web server'
  setTimeout(function () {
    document.getElementById('status').textContent = 'Downloading assets'
    setTimeout(function () {
      document.getElementById('status').textContent = 'Initializing server'
      setTimeout(loaded, 600)
    }, 1500)
  }, 450)
}
placeholderPlaygroundInitialization()

function loaded() {
  document.getElementById('status').textContent = 'Assets loaded'
}
