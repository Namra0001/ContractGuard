document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const fileInfo = document.getElementById('file-info');
    const fileName = document.getElementById('file-name');
    const uploadBtn = document.getElementById('upload-btn');
    const uploadForm = document.getElementById('upload-form');

    if (!dropZone) return;

    let selectedFile = null;

    dropZone.addEventListener('click', () => {
        fileInput.click();
    });

    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.style.backgroundColor = '#e0e7ff';
    });

    dropZone.addEventListener('dragleave', (e) => {
        e.preventDefault();
        dropZone.style.backgroundColor = '#eef2ff';
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.style.backgroundColor = '#eef2ff';
        if (e.dataTransfer.files.length > 0) {
            handleFile(e.dataTransfer.files[0]);
        }
    });

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFile(e.target.files[0]);
        }
    });

    function handleFile(file) {
        selectedFile = file;
        fileName.textContent = file.name;
        fileInfo.style.display = 'block';
        uploadBtn.disabled = false;
    }

    uploadForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        if (!selectedFile) return;

        uploadBtn.disabled = true;
        uploadBtn.textContent = 'Uploading...';

        try {
            // const formData = new FormData();
            // formData.append('contract', selectedFile);
            // await api.post('/upload', formData);
            
            // Mock upload
            setTimeout(() => {
                alert('Upload successful! Proceeding to analysis.');
                window.location.href = 'analysis.html';
            }, 1000);
            
        } catch (err) {
            alert(err.message);
            uploadBtn.disabled = false;
            uploadBtn.textContent = 'Upload and Analyze';
        }
    });
});
