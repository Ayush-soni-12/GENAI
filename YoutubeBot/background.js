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

        const res = await fetch(
          `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${apiKey}`,
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              contents: [{ 
                parts: [{ 
                  text: `You are a helpful YouTube assistant. Please provide clear, concise, and helpful responses about YouTube videos. 
                  
User's question: ${question}

Please respond in a friendly, informative tone. Focus on being helpful and accurate.` 
                }] 
              }],
              generationConfig: {
                temperature: 0.7,
                topK: 40,
                topP: 0.95,
                maxOutputTokens: 1024,
              }
            }),
          }
        );

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
        const answer = responseData?.candidates?.[0]?.content?.parts?.[0]?.text || 
                      "I couldn't generate a response. Please try again.";

        sendResponse({ answer });
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