// Get elements from HTML
const button = document.getElementById('submitButton')
const output = document.getElementById('outputResponse')
const input = document.getElementById('input')

// Event Listners
button.addEventListener('click', submitButton)

input.addEventListener('keydown', function (e) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    submitButton()
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
