function obtenerLineas() {
    const formulario = document.getElementById('formulario');
    const formData = new FormData(formulario);

    const queryString = new URLSearchParams(formData).toString();
    const url = `http://127.0.0.1:5000/lineas/?${queryString}`;

    fetch(url)
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Error al obtener los datos.');
            }
        })
        .then(data => {
            mostrarResultado(data);
        })
        .catch(error => {
            console.error('Error:', error);
            mostrarResultado('Error al obtener los datos.');
        });
}

function mostrarResultado(data) {
    const resultadoDiv = document.getElementById('resultado');
    resultadoDiv.innerHTML = JSON.stringify(data, null, 2);
}
