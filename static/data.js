// Get elements from html
const button = document.getElementById('submitButton')
const output = document.getElementById('outputResponse')
const input = document.getElementById('input')
const modelSelect = document.getElementById('models')

// Assign different class to output based on response
function setOutputClass(outputString) {
  //Number of characters before it switches styles is 80, change if needed
  if (outputString.length < 80) {
    output.className = 'output-simple'
  } else {
    output.className = 'output'
  }
}

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

      setOutputClass(json.data)
    })
    .catch(err => console.error(err))
}

modelSelect.addEventListener('change', event => {
  const model = event.target.value
  if(model == "flan-alpaca-base"){
    //update model selection
    console.assert("base model")
  }
  else if(model == "test"){
    console.assert("test model")
  }
})