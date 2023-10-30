// Get elements from html
const button = document.getElementById('submitButton')
const output = document.getElementById('outputResponse')
const input = document.getElementById('input')

// event listener on the button element
button.onclick = function () {
  fetch('/api?' + new URLSearchParams({ input: input.value }))
    .then(response => {
      if (responsçe.ok) {
        return response.json()
      } else {
        alert('something is wrong')
      }
    })
    .then(json => {
      output.innerText = json.data
    })
    .catch(err => console.error(err))
}
