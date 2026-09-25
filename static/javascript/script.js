function atualizarNomeArquivo(input) {
    var fileName = document.getElementById('fileName');
    if (!fileName) return;
    fileName.textContent = input.files && input.files.length ? input.files[0].name : 'Nenhum arquivo escolhido';
    fileName.title = fileName.textContent;
}

document.addEventListener('DOMContentLoaded', function () {
    var photoInput = document.getElementById('photoInput');
    if (photoInput) {
        atualizarNomeArquivo(photoInput);
        photoInput.addEventListener('change', function () { atualizarNomeArquivo(photoInput); });
    }
});
