// background.js
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "askGemini") {
    const { question, videoId } = message;

    (async () => {
      try {
        const data = await new Promise((resolve) => {
          chrome.storage.sync.get(["apiKey"], resolve);
        });

        const apiKey = data.apiKey;
        if (!apiKey) {
          sendResponse({
            error: "API key not found. Please set it in extension options."
          });
          return;
        }

       const res = await fetch("http://localhost:8000/ask", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            question,
            videoId
          }),
        });
         
        console.log("Gemini API Response Status:", res);

        if (!res.ok) {
          const errorData = await res.json();
          console.error("Gemini API Error:", errorData);
          
          let errorMessage = `API Error: ${res.status}`;
          if (res.status === 401) {
            errorMessage = "Invalid API key. Please check your Gemini API key in settings.";
          } else if (res.status === 429) {
            errorMessage = "Rate limit exceeded. Please try again later.";
          } else if (errorData?.error?.message) {
            errorMessage = errorData.error.message;
          }
          
          sendResponse({ error: errorMessage });
          return;
        }

        const responseData = await res.json();
        console.log("Gemini Response Data:", responseData);
        sendResponse({ answer: responseData.answer });
      } catch (err) {
        console.error("Error in askGemini:", err);
        sendResponse({ 
          error: err.message || "Network error. Please check your connection." 
        });
      }
    })();

    return true; // Keep message channel open
  }
});

// Add installation handler
chrome.runtime.onInstalled.addListener((details) => {
  if (details.reason === "install") {
    chrome.tabs.create({
      url: chrome.runtime.getURL("options.html")
    });
  }
});