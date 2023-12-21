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
}
updateData()
