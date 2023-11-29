function placeholderPlaygroundInitialization() {
  document.getElementById('status').textContent = 'Starting up web server'

  setTimeout(function () {
    document.getElementById('status').textContent = 'Starting download'

    setTimeout(function () {
      document.getElementById('status').textContent = 'Downloading model 1'
      const apiUrl = 'http://localhost:5000/api/status'
      let model

      fetch(apiUrl)
        .then(response => {
          if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`)
          }
          return response.json()
        })
        .then(data => {
          model = data
        })
        .catch(error => {
          console.error('Fetch error:', error)
        })

      for (let i = 0; i < 10; i++) {
        setTimeout(function () {
          fetch(apiUrl)
            .then(response => {
              if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`)
              }
              return response.json()
            })
            .then(data => {
              model = data
            })
            .catch(error => {
              console.error('Fetch error:', error)
            })
        }, 1000)
        i = i + 1
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

placeholderPlaygroundInitialization()
