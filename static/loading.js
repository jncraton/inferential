/*function placeholderPlaygroundInitialization() {
    document.getElementById('status').textContent = 'Starting up web server'
    setTimeout(function () {
        document.getElementById('status').textContent = 'Starting download'
        setTimeout(function () {
            document.getElementById('status').textContent = 'Downloading model 1'
            var model = 0;
            fetch('/api/status'
            ).then(response =>{
              model = response.text
            }).catch(err=>{
              console.log(err)
            })
            while (model < 1){
                setTimeout(function () {
                    fetch('/api/status'
                    ).then(response =>{
                    model = response.text
                    }).catch(err=>{
                    console.log(err)
                    })
                }, 1000)
            }
            document.getElementById('status').textContent = 'Downloading model 2'
            while (model < 2){
                setTimeout(function () {
                    fetch('/api/status'
                    ).then(response =>{
                    model = response.text
                    }).catch(err=>{
                    console.log(err)
                    })
                }, 1000)
            }
            document.getElementById('status').textContent = 'All Models Downloaded'
            setTimeout(function () {
                document.getElementById('status').textContent = 'Setting up'
                setTimeout(function () {
                    document.getElementById('status').textContent = 'Done!'
                }, 50)
            }, 50)
        }, 50)
    }, 50)
  }

  placeholderPlaygroundInitialization()*/

const apiUrl = 'http://localhost:5000/api/status'

let model
setTimeout(function () {
  fetch(apiUrl)
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`)
      }
      return response.json()
    })
    .then(data => {
      // Store the fetched data in the "status" variable
      model = data
    })
    .catch(error => {
      console.error('Fetch error:', error)
    })

  document.getElementById('status').textContent = model
}, 10000)
