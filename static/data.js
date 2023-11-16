// Get elements from html
const button = document.getElementById('submitButton')
const output = document.getElementById('outputResponse')
const input = document.getElementById('input')
const modelSelect = document.getElementById('models')

// Current selected Model
const currentModel = 0

// Event Listners
button.addEventListener('click', submitButton)

input.addEventListener('keydown', function (e) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    submitButton()
  }
})

modelSelect.addEventListener('change', event => {
  const model = event.target.value
  if (model == 'TheBloke/Llama-2-7B-Chat-GGUF') {
    currentModel = 0
  } else if (model == 'jncraton/LaMini-Flan-T5-783M-ct2-int8') {
    currentModel = 1
  } else if (model == 'TheBloke/Llama-2-7B-Chat-GGML') {
    currentModel = 2
  } else if (model == 'TheBloke/Nous-Capybara-7B-v1.9-GGUF') {
    currentModel = 3
  } else if (model == 'TheBloke/TinyLlama-1.1B-1T-OpenOrca-GGUF') {
    currentModel = 4
  } else if (model == 'marella/gpt-2-ggml') {
    currentModel = 5
  }
})

// Function calls fetch API upon promptSubmition
function submitButton() {
  output.innerText = 'Loading...'

  fetch(
    '/api?' + new URLSearchParams({ input: input.value, model: currentModel }),
  )
    .then(response => {
      const textStream = response.body.getReader()
      let accumulatedData = '' // To accumulate the data
      const decoder = new TextDecoder()
      function readAndDisplay() {
        textStream.read().then(({ done, value }) => {
          if (done) {
            return // All tokens have been received
          }
          accumulatedData += decoder.decode(value) // Accumulate the received text
          output.innerText = accumulatedData

          readAndDisplay() // Continue reading and displaying
        })
      }

      readAndDisplay() // Start the process
    })
    .catch(err => console.error(err))
}
