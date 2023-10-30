// Get elements from HTML
const button = document.getElementById('submitButton')
const output = document.getElementById('outputResponse')
const input = document.getElementById('input')

// Event listener on the button element
// ... Your existing code ...

button.onclick = function () {
  fetch('/api?' + new URLSearchParams({ input: input.value }))
    .then(response => {
      const textStream = response.body.getReader();
      let accumulatedData = ''; // To accumulate the JSON data

      function readAndDisplay() {
        textStream.read().then(({ done, value }) => {
          if (done) {
            return; // All tokens have been received
          }

          accumulatedData += value; // Accumulate the received text

          try {
            const token = JSON.parse(accumulatedData);
            output.innerText += token.data + ' '; // Display each token with a space
          } catch (error) {
            console.error(error);
          }

          readAndDisplay(); // Continue reading and displaying
        });
      }

      readAndDisplay(); // Start the process
    })
    .catch(err => console.error(err))
}

// ... Your existing code ...

