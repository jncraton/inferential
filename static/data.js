// Get elements from html
const button = document.getElementById('submitButton')
const output = document.getElementById('outputResponse')
const input = document.getElementById('input')
const modelSelect = document.getElementById('models')

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
  if (model == 'Conversational tasks') {
    // fastchat-t5-3b-v1.0
  } else if (model == 'Coding tasks') {
    // codet5p-220m-py
  } else if (model == 'Creative writing tasks') {
    // LaMini-GPT-124M
  } else if (model == 'Large tasks') {
    // flan-alpaca-gpt4-xl
  } else if (model == 'Summarization and translation tasks') {
    // flan-t5-xl
  }
})

// Function calls fetch API upon promptSubmition
function submitButton() {
  output.innerText = 'Loading...'

  fetch('/api?' + new URLSearchParams({ input: input.value }))
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
