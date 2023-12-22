// This script interacts with an API to perform natural language processing using pre-trained models. It includes functions to check the availability of models, handle user input, and display the API response dynamically on the HTML page.

// Get elements from html
const button = document.getElementById('submitButton')
const output = document.getElementById('outputResponse')
const input = document.getElementById('input')
const modelSelect = document.getElementById('modelSelect')
const loadingSpinner = document.getElementById('loadingSpinner')

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

// Event Listeners
button.addEventListener('click', displayCompletion)
input.addEventListener('keydown', function (e) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    if (!button.disabled) {
      displayCompletion()
    }
  }
})

async function displayCompletion() {
  button.disabled = true
  loadingSpinner.classList.remove('spinner-hidden')

  let response = await fetch(
    '/api?' +
      new URLSearchParams({ input: input.value, model: modelSelect.value }),
  )

  const textStream = response.body.getReader()
  const decoder = new TextDecoder()
  completion = ''

  while (true) {
    output.innerText = completion
    let { done, value } = await textStream.read()
    if (done) break
    completion += decoder.decode(value)
  }

  button.disabled = false
  loadingSpinner.classList.add('spinner-hidden')
}
