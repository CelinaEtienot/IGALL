function obtenerLineas() {
    const formulario = document.getElementById('formulario');
    const formData = new FormData(formulario);

    // Filtrar las entradas eliminando aquellas con valores vacíos
    const entriesWithoutEmptyValues = Array.from(formData.entries())
        .filter(([key, value]) => value !== "")
        .reduce((acc, [key, value]) => ({ ...acc, [key]: value }), {});

    const queryString = new URLSearchParams(entriesWithoutEmptyValues).toString();
    const url = `http://127.0.0.1:5000/lineas?${queryString}`;

    fetch(url)
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Error al obtener los datos.');
            }
        })
        .then(data => {
            mostrarResultadoEnTabla(data);
        })
        .catch(error => {
            console.error('Error:', error);
            mostrarResultadoEnTabla([]);
        });
}

function mostrarResultadoEnTabla(data) {
    const tabla = document.querySelector('#tabla-resultados tbody');

    // Limpiar contenido anterior de la tabla
    tabla.innerHTML = '';

    // Iterar sobre los datos y agregar filas a la tabla
    for (let lineas of data) {
        // Crear una fila de tabla
        let fila = document.createElement('tr');

        // Agregar columnas a la fila
        fila.innerHTML = `<td>${lineas.table_no}</td>
                         <td>${lineas.igall_no}</td>
                         <td>${lineas.design}</td>
                         <td>${lineas.system}</td>
                         <td>${lineas.structure_component}</td>
                         <td>${lineas.critical_location_part}</td>
                         <td>${lineas.material}</td>
                         <td>${lineas.environment}</td>
                         <td>${lineas.ageing_effect}</td>
                         <td>${lineas.degradation_mechanism}</td>
                         <td><a href="static/documentos/${lineas.url}" download>${lineas.Document}</a></td>`;

        // Anexar la fila al cuerpo de la tabla
        tabla.appendChild(fila);
    }
}
