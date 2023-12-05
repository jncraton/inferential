// Get elements from html
const button = document.getElementById('submitButton')
const output = document.getElementById('outputResponse')
const input = document.getElementById('input')
const modelSelect = document.getElementById('modelSelect')

async function checkModelStatus() {
  let models_status = await fetch('/api/status').then(response =>
    response.json(),
  )
  if (models_status.loadedAll) {
    input.innerText = ''
    input.disabled = false
    button.disabled = false
  } else {
    setTimeout(checkModelStatus, 5000)
  }
}
checkModelStatus()

let isWaiting = false // Flag to track if waiting for API response

// Event Listeners
button.addEventListener('click', submitButton)
input.addEventListener('keydown', function (e) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    if (!isWaiting) {
      submitButton()
    }
  }
})
const loadingSpinner = document.getElementById('loadingSpinner')
// Function calls fetch API upon prompt submission
function submitButton() {
  if (isWaiting) {
    return // Do nothing if waiting for response
  }

  isWaiting = true // Set flag to indicate waiting for API response
  button.disabled = true
  loadingSpinner.style.display = 'block'

  fetch(
    '/api?' +
      new URLSearchParams({ input: input.value, model: modelSelect.value }),
  )
    .then(response => {
      const textStream = response.body.getReader()
      let accumulatedData = '' // To accumulate the data
      const decoder = new TextDecoder()

      function readAndDisplay() {
        textStream.read().then(({ done, value }) => {
          if (done) {
            isWaiting = false // Reset flag when API response is complete
            button.disabled = false
            loadingSpinner.style.display = 'none'
            return // All tokens have been received
          }
          accumulatedData += decoder.decode(value) // Accumulate the received text
          output.innerText = accumulatedData
          readAndDisplay() // Continue reading and displaying
        })
      }

      readAndDisplay() // Start the process
    })
    .catch(err => {
      console.error(err)
      loadingSpinner.style.display = 'none' // Hide loading spinner on error
    })
}
