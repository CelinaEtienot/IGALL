const URL = "https://celinaetienot.pythonanywhere.com/documentos/";

function eliminarDocumento() {
    const documentNo = document.getElementById("documentNo").value;

    fetch(URL + documentNo, {
        method: 'DELETE',
    })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Error al eliminar el documento. Por favor, verifique el número de documento e inténtelo de nuevo.');
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
    } else if (data.mensaje) {
        resultContainer.innerHTML = `<p>${data.mensaje}</p>`;
    } else {
        resultContainer.innerHTML = `<p>Error desconocido al procesar la solicitud.</p>`;
    }
}
