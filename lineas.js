function obtenerLineas() {
    const form = document.getElementById('lineasForm');
    const formData = new FormData(form);

    // Filter out empty values
    const entriesWithoutEmptyValues = Array.from(formData.entries())
        .filter(([key, value]) => value !== "")
        .reduce((acc, [key, value]) => ({ ...acc, [key]: value }), {});

    const queryString = new URLSearchParams(entriesWithoutEmptyValues).toString();
    const url = `https://celinaetienot.pythonanywhere.com/lineas?${queryString}`;

    fetch(url)
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Error al obtener los datos.');
            }
        })
        .then(data => {
            const resultadoDiv = document.getElementById('resultado');
            resultadoDiv.textContent = JSON.stringify(data, null, 2);
        })
        .catch(error => {
            console.error('Error:', error);
            const resultadoDiv = document.getElementById('resultado');
            resultadoDiv.textContent = 'Error al obtener los datos.';
        });
}