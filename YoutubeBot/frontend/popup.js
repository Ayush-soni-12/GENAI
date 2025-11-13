// popup.js
document.getElementById("openYoutube").addEventListener("click", () => {
  chrome.tabs.create({ url: "https://www.youtube.com" });
});

// Add animation to buttons
document.querySelectorAll('button').forEach(button => {
  button.addEventListener('mouseenter', function() {
    this.style.transform = 'translateY(-2px)';
  });
  
  button.addEventListener('mouseleave', function() {
    this.style.transform = 'translateY(0)';
  });
});