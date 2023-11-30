let statusElement = document.getElementById('status')

async function updateData() {
  let models_status = await fetch('/api/status').then(response =>
    response.json(),
  )
  //Get the number of models
  let size = Object.keys(models_status.models).length

  // TODO (PR#57): Make the data in models_status more readable for the status page.

 
  statusElement.innerHTML = " "
    for(let i = 0; i < size; i++){
      if(models_status.models[i].loaded){
        statusElement.innerHTML += JSON.stringify(models_status.models[i].name).replace(/(['"])/g, "") + " is loaded!" + "<br>"
      }
      statusElement.innerHTML += JSON.stringify(models_status.models[i].name).replace(/(['"])/g, "") + " is loading! <br>"
    }


  if (!models_status.loadedAll) window.setTimeout(updateData, 5000)
}
updateData()
