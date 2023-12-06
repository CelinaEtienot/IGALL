const URL = "https://celinaetienot.pythonanywhere.com/";

const app = Vue.createApp({
    data() {
        return {
            documentos: []
        }
    },
    methods: {
        obtenerDocumentos() {
            fetch(URL + 'documentos')
                .then(response => {
                    if (response.ok) {
                        return response.json();
                    } else {
                        throw new Error('Error al obtener los documentos.');
                    }
                })
                .then(data => {
                    this.documentos = data;
                })
                .catch(error => {
                    alert('Error al obtener los documentos.');
                    console.error('Error:', error);
                });
        },
        eliminarDocumento(No) {
            if (confirm('Are you sure you want to delete this document?')) {
                fetch(URL + `documentos/`+ No, { method: 'DELETE' })
                    .then(response => {
                        if (response.ok) {
                            this.documentos = this.documentos.filter(documento => documento.No !== No);
                            alert('Document deleted successfully.');
                        } else {
                            throw new Error('Error deleting document');
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        alert(error.message);
                    });
            }
        }
    },
    mounted() {
        this.obtenerDocumentos();
    }
});

app.mount('#app');
