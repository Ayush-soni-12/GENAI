// options.js
document.addEventListener("DOMContentLoaded", () => {
  chrome.storage.sync.get(["apiKey"], (data) => {
    if (data.apiKey) {
      document.getElementById("apiKey").value = data.apiKey;
    }
  });
});

document.getElementById("save").addEventListener("click", () => {
  const apiKey = document.getElementById("apiKey").value.trim();
  const status = document.getElementById("status");

  if (!apiKey) {
    showStatus("Please enter an API key!", "error");
    return;
  }

  if (!apiKey.startsWith("AIza")) {
    showStatus("Please enter a valid Gemini API key!", "error");
    return;
  }

  chrome.storage.sync.set({ apiKey }, () => {
    showStatus("API Key saved successfully!", "success");
    
    setTimeout(() => {
      status.classList.add("status-hidden");
    }, 3000);
  });
});

function showStatus(message, type) {
  const status = document.getElementById("status");
  status.textContent = message;
  status.className = type === "success" ? "status-success" : "status-error";
  status.classList.remove("status-hidden");
}

// Add input animation
document.getElementById("apiKey").addEventListener("focus", function() {
  this.parentElement.style.transform = "scale(1.02)";
});

document.getElementById("apiKey").addEventListener("blur", function() {
  this.parentElement.style.transform = "scale(1)";
});