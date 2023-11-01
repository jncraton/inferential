// Get elements from html
const button = document.getElementById('submitButton')
const output = document.getElementById('outputResponse')
const input = document.getElementById('input')

// Assign different class to output based on response
function setOutputClass(outputString) {
  if (outputString.length < 80) {
    //Number of characters before it switches styles is 80, change if
    output.className = 'output-simple'
  } else {
    output.className = 'output'
  }
}

// Event listener on the button element
button.onclick = function () {
  output.innerText = 'Loading...'
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
