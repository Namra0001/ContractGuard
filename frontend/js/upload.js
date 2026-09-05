document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const fileInfo = document.getElementById('file-info');
    const fileName = document.getElementById('file-name');
    const fileSize = document.getElementById('file-size');
    const removeFileBtn = document.getElementById('remove-file-btn');
    const uploadBtn = document.getElementById('upload-btn');
    const uploadForm = document.getElementById('upload-form');
    
    const uploadProgress = document.getElementById('upload-progress');
    const progressBar = document.getElementById('progress-bar');
    const progressPercent = document.getElementById('progress-percent');
    const progressStatus = document.getElementById('progress-status');

    if (!dropZone) return;

    let selectedFile = null;

    dropZone.addEventListener('click', () => {
        fileInput.click();
    });

    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => {
            dropZone.classList.add('border-brand-500', 'bg-brand-50', 'dark:bg-brand-900/20');
        }, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => {
            dropZone.classList.remove('border-brand-500', 'bg-brand-50', 'dark:bg-brand-900/20');
        }, false);
    });

    dropZone.addEventListener('drop', (e) => {
        if (e.dataTransfer.files.length > 0) {
            handleFile(e.dataTransfer.files[0]);
        }
    });

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFile(e.target.files[0]);
        }
    });

    removeFileBtn.addEventListener('click', () => {
        selectedFile = null;
        fileInput.value = '';
        dropZone.classList.remove('hidden');
        fileInfo.classList.add('hidden');
        uploadBtn.disabled = true;
    });

    function formatBytes(bytes, decimals = 2) {
        if (!+bytes) return '0 Bytes';
        const k = 1024;
        const dm = decimals < 0 ? 0 : decimals;
        const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return `${parseFloat((bytes / Math.pow(k, i)).toFixed(dm))} ${sizes[i]}`;
    }

    function handleFile(file) {
        selectedFile = file;
        fileName.textContent = file.name;
        if (fileSize) fileSize.textContent = formatBytes(file.size);
        
        dropZone.classList.add('hidden');
        fileInfo.classList.remove('hidden');
        uploadBtn.disabled = false;
    }

    uploadForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        if (!selectedFile) return;

        uploadBtn.disabled = true;
        uploadBtn.innerHTML = '<i data-lucide="loader-2" class="h-4 w-4 mr-2 animate-spin"></i> Processing...';
        lucide.createIcons();
        
        fileInfo.classList.add('hidden');
        uploadProgress.classList.remove('hidden');

        try {
            // Mock upload progress visually while waiting for API
            let progress = 0;
            const interval = setInterval(() => {
                progress += Math.random() * 15;
                if (progress > 90) progress = 90; // Hold at 90% until API responds
                
                progressBar.style.width = `${progress}%`;
                progressPercent.textContent = `${Math.floor(progress)}%`;
            }, 300);
            
            // Real API call
            const formData = new FormData();
            formData.append('file', selectedFile); // Assuming 'file' based on standard FastAPI UploadFile
            
            const result = await api.post('/contracts/upload', formData);
            
            clearInterval(interval);
            progressBar.style.width = `100%`;
            progressPercent.textContent = `100%`;
            progressStatus.textContent = 'Processing document...';
            
            setTimeout(() => {
                window.location.href = `analysis.html?id=${result.id || result.contract_id || ''}`;
            }, 800);
            
        } catch (err) {
            alert(err.message);
            uploadBtn.disabled = false;
            uploadBtn.innerHTML = 'Analyze Contract <i data-lucide="arrow-right" class="h-4 w-4 ml-2"></i>';
            lucide.createIcons();
            
            uploadProgress.classList.add('hidden');
            fileInfo.classList.remove('hidden');
        }
    });
});
