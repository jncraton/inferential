function initializePlayground() {
  document.getElementById('status').textContent = 'Starting up web server'
  setTimeout(function () {
    document.getElementById('status').textContent = 'Downloading assets'
    setTimeout(function () {
      document.getElementById('status').textContent = 'Initializing server'
      setTimeout(function () {
        loaded()
      }, 600)
    }, 1500)
  }, 450)
}

function loaded() {
  document.getElementById('status').textContent = 'Assets loaded'
  var Header = document.getElementById('Header')
  Header.innerHTML = '<a href="http://127.0.0.1:5000/playground">Playground</a>'
}

//if (!localStorage.getItem('pageLoaded')) {
// This will only run when the page is loaded for the first time
initializePlayground()

// Set the flag in localStorage so the if statement will not pass again when navigated back
//localStorage.setItem('pageLoaded', 'true');
//}
//else {
//loaded();
//}
