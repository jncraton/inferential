// Get elements from html
const button = document.getElementById('submitButton')
const output = document.getElementById('outputResponse')
const input = document.getElementById('input')

// event listener on the button element
button.onclick = function () {
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
