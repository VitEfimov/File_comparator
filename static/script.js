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


