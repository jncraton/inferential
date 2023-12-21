// This script fetches and displays the status of pre-trained models from the API, indicating whether each model is ready or not. It dynamically updates the HTML content with the current status and sets a periodic refresh to keep the information up to date.

async function updateData() {
  let response = await fetch('/api/status')
  let status = await response.json()

  document.getElementById('status').innerHTML = ''

  status.models.forEach(model => {
    plt = document.createElement('div')
    document.getElementById('status').append(plt)

    title = ` Tokens/min for ${model.name}${model.loaded ? '' : ' (Offline)'}`
    Plotly.newPlot(
      plt,
      [
        {
          x: Array.from(new Array(60), (_, i) => -i),
          y: model.tokens_per_min,
        },
      ],
      {
        title: title,
        height: 240,
        margin: { l: 32, r: 32, b: 32, t: 32 },
      },
    )
  })

  if (!status.loadedAll) setTimeout(updateData, 5000)
}
updateData()
