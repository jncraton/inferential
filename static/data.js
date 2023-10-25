// Get elements from html
const button = document.getElementById('submitButton')
const output = document.getElementById('outputResponse')
const input = document.getElementById('input')

// Create an event listener on the button element
button.onclick = function () {
  // Get the reciever endpoint from Python using fetch
  fetch('/api?' + new URLSearchParams({ input: input.value }))
    .then(response => {
      if (response.ok) {
        return response.json()
      } else {
        alert('something is wrong')
      }
    })
    .then(json => {
      // Log the response data in the console
      output.innerText = json.data
    })
    .catch(err => console.error(err))
}
