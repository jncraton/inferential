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
      const decode = new TextDecoder()
      function readAndDisplay() {
        textStream.read().then(({ done, value }) => {
          if (done) {
            return; // All tokens have been received
          }
          console.log("Value: " + value)
          accumulatedData += decode.decode(value).replace(/[^a-zA-Z ]/g,"").replace("data",""); // Accumulate the received text
          console.log("Accumulated Data: "+accumulatedData)
          try {
          const token = JSON.stringify(accumulatedData);
          output.innerText = token + " "// Display each token with a space
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

