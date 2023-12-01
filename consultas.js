const URL = "http://127.0.0.1:5000/";

function listDocuments() {
    const documentNo = document.getElementById("documentNo").value;

    fetch(URL + 'documentos', {
        method: 'GET',
        body: formData // Aquí enviamos formData en lugar de JSON
    })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Error retrieving document.');
            }
        })
        .then(data => {
            displayResult(data);
        })
        .catch(error => {
            displayResult({ error: true, message: error.message });
        });
}

function displayResult(data) {
    const resultContainer = document.getElementById("result");
    resultContainer.innerHTML = "";

    if (data.error) {
        resultContainer.innerHTML = `<p class="error">${data.message}</p>`;
    } else {
        resultContainer.innerHTML = `
            <p><strong>Document Number:</strong> ${data.No}</p>
            <p><strong>Title:</strong> ${data.Title}</p>
            <p><strong>Area:</strong> ${data.Area}</p>
            <p><strong>URL:</strong> ${data.url}</p>
            <p><strong>Last Valid Version:</strong> ${data.Last_valid_version}</p>
            <p><strong>Owner:</strong> ${data.Igall_owner}</p>
        `;
    }
}
