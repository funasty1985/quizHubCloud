document.addEventListener('DOMContentLoaded', function () {

    const generateButton = document.getElementById('generateButton');
    generateButton.addEventListener('click', uploadAndExtractText);

    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    const fileInfo = document.getElementById('fileInfo'); 

    dropZone.addEventListener('click', () => fileInput.click());

    fileInput.addEventListener('change', function() { 
        displayFileInfo();
    });

    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });

    dropZone.addEventListener('dragleave', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        
        const files = e.dataTransfer.files;
        if (files.length) {
            fileInput.files = files;
            displayFileInfo(); 
        }
    });

    function displayFileInfo() { 
        const file = fileInput.files[0];
        if (file) {
            fileInfo.textContent = `${file.name}`;
        } else {
            fileInfo.textContent = ''; 
        }
    }

    async function uploadAndExtractText() {
        fileInfo.textContent = ''; 
        const file = fileInput.files[0];
        if (!file) {
            console.log("No file selected.");
            fileInfo.textContent = 'Please select a file';
            return;
        }
    
        fileInfo.textContent = 'Processing...'; 
    
        const base64String = await new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.readAsDataURL(file);
            reader.onload = () => resolve(reader.result.split('base64,')[1]);
            reader.onerror = error => reject(error);
        });
    
        fetch("http://127.0.0.1:8000/upload", {
            method: "POST",
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                filename: file.name,
                filebytes: base64String,
            }),
        })
        .then(response => response.ok ? response.json() : Promise.reject(response))
        .then(data => {
            console.log("Upload successful:", data);
            return fetch("http://127.0.0.1:8000/extract-paragraph", {
                method: "POST",
                headers: {
                    Accept: "application/json",
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ filename: file.name }),
            });
        })
        .then(response => response.ok ? response.json() : Promise.reject(response))
        .then(extractionData => {
            console.log("Text Extraction successful:", extractionData);
            fileInfo.textContent = 'Completed!'; 
        })
        .catch(error => {
            console.error("Error during upload or text extraction:", error);
            fileInfo.textContent = 'Error! Check console for details.';
        });
    
        fileInput.value = ""; 
    }
});
