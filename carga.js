const URL = "http://127.0.0.1:5000/"

document.getElementById('form').addEventListener('submit', function(event) {
    event.preventDefault(); // Evitamos que se envíe el formulario

    var formData = new FormData();
    formData.append('No', document.getElementById('No').value);
    formData.append('Title', document.getElementById('Title').value);
    formData.append('Area', document.getElementById('Area').value);
    formData.append('Archivo', document.getElementById('Archivo').files[0]);
    formData.append('Last_valid_version', document.getElementById('Last_valid_version').value);
    formData.append('Igall_owner', document.getElementById('Igall_owner').value);

    // Realizamos la solicitud POST al servidor
    fetch(URL + 'documentos', {
        method: 'POST',
        body: formData // Aquí enviamos formData en lugar de JSON
    })
    // Después de realizar la solicitud POST, se utiliza el método then() para manejar la respuesta del servidor.
    .then(function (response) {
        if (response.ok) { 
            return response.json(); 
        } else {
            // Si hubo un error, lanzar explícitamente una excepción
            // para ser "catcheada" más adelante
            throw new Error('Error al agregar el documento.');
        }
    })
    // Respuesta OK
    .then(function () {
        // En caso de éxito
        alert('Documento agregado correctamente.');
    })
    .catch(function (error) {
        // En caso de error
        alert('Error al agregar el documento.');
        console.error('Error:', error);
    });
});