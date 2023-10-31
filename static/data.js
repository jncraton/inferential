// Get elements from html
const button = document.getElementById('submitButton')
const output = document.getElementById('outputResponse')
const input = document.getElementById('input')

// Assign different class to output based on response
function setOutputClass(outputString) {
  if (outputString.length < 80) {
    output.className = 'output-simple'
  } else {
    output.className = 'output'
  }
}

// Event listener for shift-enter
document.addEventListener('DOMContentLoaded', function () {
  const inputElement = document.getElementById('input')
  inputElement.addEventListener('keydown', function (e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      document.querySelector('form').submit()
    }
  })
})

// Event listener on the button element
button.onclick = function () {
  fetch('/api?' + new URLSearchParams({ input: input.value }))
    .then(response => {
      if (response.ok) {
        return response.json()
      } else {
        alert('Something is wrong')
      }
    })
    .then(json => {
      output.innerText = json.data

      setOutputClass(json.data)
    })
    .catch(err => console.error(err))
}
