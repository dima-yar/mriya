tinymce.init({
    selector: 'textarea#id_content',  // Замініть на ваш селектор
    plugins: 'autolink lists link image preview anchor visualblocks fullscreen media table help wordcount',
    toolbar: 'undo redo | blocks | formatselect | bold italic backcolor | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | removeformat | image media code',
    images_upload_url: "/upload_image/",
    automatic_uploads: true,
    file_picker_types: "image",
    file_picker_callback: function(callback, value, meta) {
        if (meta.filetype === 'image') {
            var input = document.createElement('input');
            input.setAttribute('type', 'file');
            input.setAttribute('accept', 'image/*');
            input.onchange = function() {
                var file = this.files[0];
                var formData = new FormData();
                formData.append('file', file);

                fetch("/upload_image/", {
                    method: 'POST',
                    body: formData
                })
                .then(response => response.json())
                .then(data => {
                    if (data.location) {
                        callback(data.location);  // Передаємо URL зображення
                    } else {
                        console.error('Image upload failed. No location returned');
                    }
                })
                .catch(error => {
                    console.error('Error uploading image:', error);
                });
            };
            input.click();
        }
    }
});
