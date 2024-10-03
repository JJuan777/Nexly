    // Función para previsualizar la imagen
    function previewImage(event) {
        const file = event.target.files[0];
        const reader = new FileReader();
        const imagePreviewContainer = document.getElementById('imagePreviewContainer');
        const imagePreview = document.getElementById('imagePreview');

        if (file) {
            reader.onload = function(e) {
                imagePreview.src = e.target.result;
                imagePreviewContainer.classList.remove('d-none');
            };
            reader.readAsDataURL(file);
        } else {
            imagePreview.src = '';
            imagePreviewContainer.classList.add('d-none');
        }
    }

    // Función para eliminar la imagen cargada
    function removeImage() {
        const imagePreview = document.getElementById('imagePreview');
        const imagePreviewContainer = document.getElementById('imagePreviewContainer');
        const imageUpload = document.getElementById('imageUpload');

        // Limpiar el valor del input
        imageUpload.value = '';

        // Ocultar la vista previa
        imagePreview.src = '';
        imagePreviewContainer.classList.add('d-none');
    }

    // Función para previsualizar el video
    function previewVideo(event) {
        const file = event.target.files[0];
        const videoPreviewContainer = document.getElementById('videoPreviewContainer');
        const videoSource = document.getElementById('videoSource');
        const videoPreview = document.getElementById('videoPreview');

        if (file) {
            const fileURL = URL.createObjectURL(file);
            videoSource.src = fileURL;
            videoPreview.load();
            videoPreviewContainer.classList.remove('d-none');
        } else {
            videoSource.src = '';
            videoPreviewContainer.classList.add('d-none');
        }
    }

    // Función para eliminar el video cargado
    function removeVideo() {
        const videoPreviewContainer = document.getElementById('videoPreviewContainer');
        const videoSource = document.getElementById('videoSource');
        const videoUpload = document.getElementById('videoUpload');

        // Limpiar el valor del input
        videoUpload.value = '';

        // Ocultar la vista previa
        videoSource.src = '';
        videoPreviewContainer.classList.add('d-none');
    }

