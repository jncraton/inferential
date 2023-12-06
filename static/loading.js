// This script fetches and displays the status of pre-trained models from the API, indicating whether each model is ready or not. It dynamically updates the HTML content with the current status and sets a periodic refresh to keep the information up to date.

let statusElement = document.getElementById('status')

async function updateData() {
  let models_status = await fetch('/api/status').then(response =>
    response.json(),
  )

  statusElement.innerHTML = models_status.models
    .map(model => `${model.name}: ${model.loaded ? 'Ready' : 'Not ready'}`)
    .join('<br>')

  if (!models_status.loadedAll) window.setTimeout(updateData, 5000)
}
updateData()
