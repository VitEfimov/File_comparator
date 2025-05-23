document.getElementById("uploadForm").addEventListener("submit", async function (e) {
  e.preventDefault();

  const formData = new FormData();
  const zip1 = document.getElementById("zip1").files[0];
  const zip2 = document.getElementById("zip2").files[0];
  formData.append("zip1", zip1);
  formData.append("zip2", zip2);

  const resultEl = document.getElementById("result");
  resultEl.textContent = "Comparing...";

  try {
    const response = await fetch("/compare", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      const errorData = await response.json();
      resultEl.textContent = `Error: ${errorData.error}`;
      return;
    }

    const data = await response.json();
    resultEl.textContent = data.result;
  } catch (error) {
    resultEl.textContent = "Error: " + error.message;
  }
});



// const dropArea = document.getElementById('drop-area');
// const output = document.getElementById('output');

// // Drag events
// ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
//   dropArea.addEventListener(eventName, preventDefaults, false);
// });
// function preventDefaults(e) {
//   e.preventDefault();
//   e.stopPropagation();
// }

// dropArea.addEventListener('drop', handleDrop, false);

// function handleDrop(e) {
//   let dt = e.dataTransfer;
//   let files = dt.files;
//   handleFiles(files);
// }

// function handleFiles(files) {
//   if (files.length > 0 && files[0].name.endsWith('.zip')) {
//     uploadFile(files[0]);
//   } else {
//     output.textContent = 'Please upload a .zip file.';
//   }
// }

// function uploadFile(file) {
//   let formData = new FormData();
//   formData.append('file', file);

//   fetch('/upload-zip', {
//     method: 'POST',
//     body: formData
//   })
//   .then(res => res.json())
//   .then(data => {
//     output.textContent = JSON.stringify(data, null, 2);
//   })
//   .catch(err => {
//     output.textContent = 'Upload failed.';
//     console.error(err);
//   });
// }
