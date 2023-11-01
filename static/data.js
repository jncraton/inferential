// Get elements from html
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
      return response.json()
    })
    .then(json => {
      output.innerText = json.data
    })
    .catch(err => console.error(err))
}
