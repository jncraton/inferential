let statusElement = document.getElementById('status')

async function updateData() {
  let models_status = await fetch('/api/status').then(response =>
    response.json(),
  )

  statusElement.innerHTML = models_status.models.map(model => `${model.name}: ${model.loaded ? 'Ready' : 'Not ready'}`).join('<br>');
  
  if (!models_status.loadedAll) window.setTimeout(updateData, 5000)
}
updateData()
