function eliminarLineas() {
    const formulario = document.getElementById('formulario');
    const formData = new FormData(formulario);

    const tableNo = formData.get('table_no');
    const igallNo = formData.get('igall_no');

    const url = `https://celinaetienot.pythonanywhere.com/eliminar_lineas/${tableNo}/${igallNo}`;

    fetch(url, {
        method: 'DELETE'
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('Error al eliminar las líneas.');
        }
    })
    .then(data => {
        mostrarResultado(data);
    })
    .catch(error => {
        console.error('Error:', error);
        mostrarResultado('Error al eliminar las líneas.');
    });
}

function mostrarResultado(data) {
    const resultadoDiv = document.getElementById('resultado');
    resultadoDiv.innerHTML = JSON.stringify(data, null, 2);
}
