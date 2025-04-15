function uploadFile() {
  const fileInput = document.getElementById('fileInput');
  const file = fileInput.files[0];
  if (!file) {
    alert('Please select a file.');
    return;
  }

  const formData = new FormData();
  formData.append('file', file);

  fetch('/upload', {
    method: 'POST',
    body: formData
  })
  .then(res => res.json())
  .then(data => {
    if (data.error) {
      document.getElementById('output').innerHTML = `<p style="color:red">${data.error}</p>`;
    } else {
      const stats = data.stats;
      document.getElementById('output').innerHTML = `
        <h3>Lead Time Stats</h3>
        <p>Average Lead Time: ${stats.average_lead_time}</p>
        <p>Standard Deviation: ${stats.std_dev_lead_time}</p>
        <p>Max Lead Time: ${stats.max_lead_time}</p>
        <p>Min Lead Time: ${stats.min_lead_time}</p>
      `;
      document.getElementById('chart').innerHTML = data.histogram;
    }
  })
  .catch(err => {
    console.error('Upload failed', err);
  });
}
function downloadReport() {
  window.location.href = '/download_report';
}
