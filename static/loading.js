let statusElement = document.getElementById('status')

async function updateData() {
  let models_status = await fetch('/api/status').then(response =>
    response.json(),
  )

  // TODO (PR#57): Make the data in models_status more readable for the status page.
  statusElement.innerText = JSON.stringify(
    models_status,
    undefined,
    2,
  ).replaceAll(' ', '\u00a0')

  if (!models_status.loadedAll) window.setTimeout(updateData, 5000)
}
updateData()
