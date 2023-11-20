// Get elements from html
const button = document.getElementById('submitButton')
const output = document.getElementById('outputResponse')
const input = document.getElementById('input')
const modelSelect = document.getElementById('models')

// Event Listners
button.addEventListener('click', submitButton)
modelSelect.addEventListener('change', checkModelType)
input.addEventListener('keydown', function (e) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    submitButton()
  }
})

// Function to check selected model
function checkModelType() {
  let modelNumber = 1
  if (modelSelect.value == 'jncraton/LaMini-Flan-T5-783M-ct2-int8') {
    modelNumber = 0
  } else if (modelSelect.value == 'marella/gpt-2-ggml') {
    modelNumber = 1
  } 
  return modelNumber
}

// Function calls fetch API upon promptSubmition`
function submitButton() {
  output.innerText = 'Loading...'
  const currentModel = checkModelType()
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
