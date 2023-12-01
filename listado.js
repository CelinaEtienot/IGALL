const URL = "http://127.0.0.1:5000/"

// Realizamos la solicitud GET al servidor para obtener todos los documentos

fetch(URL + 'documentos')
    .then(function (response) {
        if (response.ok) {
            return response.json();
    } else {
         // Si hubo un error, lanzar explícitamente una excepción
        // para ser "catcheada" más adelante
            throw new Error('Error al obtener los productos.');
        }
    })
    .then(function (data) {
        let tablaProductos = document.getElementById('tablaProductos');

    // Iteramos sobre los productos y agregamos filas a la tabla
        for (let documento of data) {
            let fila = document.createElement('tr');
            fila.innerHTML = '<td>' + documento.No + '</td>' +
                            '<td>' + documento.Title + '</td>' +
                            '<td align="right">' + producto.cantidad + '</td>' +
                            '<td align="right">' + producto.precio + '</td>' +
    // Mostrar miniatura de la imagen
    '<td><img src=static/img/' + producto.imagen_url +' 
    alt="Imagen del producto" style="width: 100px;"></td>' +
    '<td align="right">' + producto.proveedor + '</td>';
    //Una vez que se crea la fila con el contenido del producto, 
    se agrega a la tabla utilizando el método appendChild del elemento
    tablaProductos.
    tablaProductos.appendChild(fila);
    }
    })
    .catch(function (error) {
    // En caso de error
    alert('Error al agregar el producto.');
    console.error('Error:', error);
    }