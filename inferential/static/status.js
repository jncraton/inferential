async function updateData() {
  let response = await fetch('/api/status')
  let status = await response.json()

  document.getElementById('status').innerHTML = ''

  status.models.forEach(model => {
    plt = document.createElement('div')
    document.getElementById('status').append(plt)

    Plotly.newPlot(
      plt,
      [
        {
          x: Array.from(new Array(60), (_, i) => -i),
          y: model.tokens_per_min.map(x => x / 60),
        },
      ],
      {
        title: `${model.name}${model.loaded ? '' : ' (Offline)'}`,
        height: 320,
        xaxis: { title: 'Minutes' },
        yaxis: { title: 'Tokens/s' },
      },
    )
  })
}
updateData()
