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

    // Ordenar las claves de los datos según tu preferencia
    const columnOrder = [
        'table_no',
        'igall_no',
        'design', 
        'system',
        'structure_component',
        'critical_location_part',
        'material',
        'environment',
        'ageing_effect',
        'degradation_mechanism',
        'Document'
    ];

    // Iterar sobre los datos y agregar filas a la tabla
    data.forEach(item => {
        const fila = document.createElement('tr');

        // Agregar celdas en el orden especificado
        columnOrder.forEach(column => {
            const celda = document.createElement('td');
            celda.textContent = item[column] || '';  // Manejo de valores nulos o indefinidos
            fila.appendChild(celda);
        });

        tabla.appendChild(fila);
    });
}