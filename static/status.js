// This script fetches and displays the status of pre-trained models from the API, indicating whether each model is ready or not. It dynamically updates the HTML content with the current status and sets a periodic refresh to keep the information up to date.

async function updateData() {
  let response = await fetch('/api/status')
  let status = await response.json()

  document.getElementById('status').innerHTML = status.models
    .map(m => `<p>${m.loaded ? '✔' : '❌'} ${m.name}`)
    .join('')

  if (!status.loadedAll) setTimeout(updateData, 5000)
}
updateData()
