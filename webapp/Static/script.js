document.addEventListener('DOMContentLoaded', function () {
    const namespace = '/entrenamiento';
    const socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);

    socket.on('connect', function() {
        console.log('Conectado al servidor');
        // Mostrar el mensaje de cargando inicialmente
        document.getElementById('loading-info').classList.remove('hidden');
    });

    socket.on('update_epoch', function(data) {
        // Si es la primera actualizaci�n, ocultar el mensaje de cargando
        document.getElementById('loading-info').classList.add('hidden');
        document.getElementById('epoch-info').classList.remove('hidden');
        document.getElementById('epoch-info').textContent = `�poca: ${data.current_epoch} de ${data.total_epochs}`;
    });

    socket.on('update_batch', function(data) {
        // Si es la primera actualizaci�n, ocultar el mensaje de cargando
        document.getElementById('loading-info').classList.add('hidden');
        document.getElementById('batch-info').classList.remove('hidden');
        if (data.val_loss) {
            document.getElementById('batch-info').textContent = `Batch: ${data.current_batch} de ${data.total_batches}, P�rdida: ${data.loss}, P�rdida de validaci�n: ${data.val_loss}`;
        } else {
            document.getElementById('batch-info').textContent = `Batch: ${data.current_batch} de ${data.total_batches}, P�rdida: ${data.loss}`;
        }
    });


    socket.on('training_complete', function(data) {
        // Se genera el enlace de descarga cuando el entrenamiento est� completo
        var downloadLink = document.createElement('a');
        downloadLink.href = `/download/${data.file}`;
        downloadLink.textContent = 'Descargar Modelo Entrenado';
        downloadLink.download = data.file; // Esto sugerir� el nombre en el di�logo de guardar como

        var downloadLinkArea = document.getElementById('download-link-area');
        downloadLinkArea.innerHTML = ''; // Limpia cualquier enlace previo
        downloadLinkArea.appendChild(downloadLink);
    });
});


