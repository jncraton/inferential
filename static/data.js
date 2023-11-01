// Get elements from html
const button = document.getElementById('submitButton')
const output = document.getElementById('outputResponse')
const input = document.getElementById('input')

// Assign different class to output based on response
function setOutputClass(outputString) {
  //Number of characters before it switches styles is 80, change if needed
  if (outputString.length < 80) {
    output.className = 'output-simple'
  } else {
    output.className = 'output'
  }
}

// Event listener on the button element
button.onclick = function () {
  //Placeholder while fetching API response
  output.innerText = 'Loading...'

  fetch('/api?' + new URLSearchParams({ input: input.value }))
    .then(response => {
    return response.json() 
    })
    .then(json => {
      output.innerText = json.data

      setOutputClass(json.data)
    })
    .catch(err => console.error(err))
}
