const URL = "http://127.0.0.1:5000/";

const app = Vue.createApp({
    data() {
        return {
            No: '',
            Title: '',
            Area: '',
            Last_valid_version: '',
            Igall_owner: '',
            url: '',
            MostrarDocumentos: false,
            documentoSeleccionado: null,
        };
    },
    methods: {
        obtenerDocumento() {
            fetch(URL + 'documentos/' + this.No)
                .then(response => {
                    if (response.ok) {
                        return response.json();
                    } else {
                        throw new Error('Error al obtener los datos del documento.');
                    }
                })
                .then(data => {
                    this.Title = data.Title;
                    this.Area = data.Area;
                    this.Last_valid_version = data.Last_valid_version;
                    this.Igall_owner = data.Igall_owner;
                    this.url = data.url;
                    this.MostrarDocumentos = true;
                })
                .catch(error => {
                    console.log(error);
                    alert('No encontrado.');
                });
        },
        seleccionarDocumento(event) {
            const file = event.target.files[0];
            this.documentoSeleccionado = file;
            this.imagenUrlTemp = URL.createObjectURL(file);
        },
        guardarCambios() {
            const formData = new FormData();
            formData.append('No', this.No);
            formData.append('Title', this.Title);
            formData.append('Area', this.Area);
            formData.append('Last_valid_version', this.Last_valid_version);
            formData.append('Igall_owner', this.Igall_owner);

            if (this.documentoSeleccionado) {
                formData.append('Archivo', this.documentoSeleccionado, this.documentoSeleccionado.name);
            }

            fetch(URL + 'documentos/' + this.No, {
                method: 'PUT',
                body: formData,
            })
                .then(response => {
                    if (response.ok) {
                        return response.json();
                    } else {
                        throw new Error('Error al guardar los cambios del documento.');
                    }
                })
                .then(data => {
                    alert('Documento actualizado correctamente.');
                    this.limpiarFormulario();
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('Error al actualizar el documento.');
                });
        },
        limpiarFormulario() {
            this.No = '';
            this.Title = '';
            this.Area = '';
            this.Last_valid_version = '';
            this.Igall_owner = '';
            this.url = '';
            this.documentoSeleccionado = null;
            this.imagenUrlTemp = null;
            this.MostrarDocumentos = false;
        },
    },
});

app.mount('#app');
