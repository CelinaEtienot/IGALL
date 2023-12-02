const URL = "http://127.0.0.1:5000/";

// Realizamos la solicitud GET al servidor para obtener todos los documentos
fetch(URL + 'documentos')
    .then(function (response) {
        if (response.ok) {
            return response.json();
        } else {
            // Si hubo un error, lanzar explícitamente una excepción
            // para ser "catcheada" más adelante
            throw new Error('Error al obtener los documentos.');
        }
    })
    .then(function (data) {
        let tableBody = document.getElementById('tableBody');

        // Iterate over the documents and create rows
        for (let documento of data) {
            // Create a table row
            let row = document.createElement('tr');

            // Add columns to the row
            row.innerHTML = `<td>${documento.No}</td>
                             <td>${documento.Title}</td>
                             <td>${documento.Area}</td>
                             <td>${documento.Last_valid_version}</td>
                             <td>${documento.Igall_owner}</td>
                             <td><a href="static/documentos/${documento.url}" download>Descargar</a></td>`;

            // Append the row to the table body
            tableBody.appendChild(row);
        }
    })
    .catch(function (error) {
        // En caso de error
        alert('Error al obtener los documentos.');
        console.error('Error:', error);
    });