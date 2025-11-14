// content.js - UPDATED VERSION
let currentVideoId = null;
let observer = null;

console.log('YouTube AI Assistant: Content script loaded');

// Initialize when page loads
document.addEventListener('DOMContentLoaded', init);
// Also initialize when YouTube updates (SPA navigation)
window.addEventListener('yt-navigate-finish', init);
window.addEventListener('spfrequest}")"', init); // For older YouTube
window.addEventListener('spfdone', init); // For older YouTube

function init() {
    console.log('YouTube AI Assistant: Initializing...');
    setTimeout(() => {
        removeExistingButton();
        initAIButton();
        setupObserver();
    }, 1000);
}

function setupObserver() {
    if (observer) {
        observer.disconnect();
    }

    observer = new MutationObserver((mutations) => {
        for (let mutation of mutations) {
            if (mutation.type === 'childList') {
                for (let node of mutation.addedNodes) {
                    if (node.nodeType === 1) { // Element node
                        if (isVideoPage() && !document.getElementById('ai-assistant-btn')) {
                            console.log('YouTube AI Assistant: DOM changed, reinitializing...');
                            setTimeout(initAIButton, 500);
                            break;
                        }
                    }
                }
            }
        }
    });

    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
}

function isVideoPage() {
    return window.location.href.includes('youtube.com/watch') && getCurrentVideoId();
}

function getCurrentVideoId() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('v');
}

function removeExistingButton() {
    const existingBtn = document.getElementById('ai-assistant-btn');
    const existingBox = document.getElementById('ai-box');
    if (existingBtn) existingBtn.remove();
    if (existingBox) existingBox.remove();
}

function initAIButton() {
    if (!isVideoPage()) {
        console.log('YouTube AI Assistant: Not a video page, skipping');
        return;
    }

    if (document.getElementById('ai-assistant-btn')) {
        console.log('YouTube AI Assistant: Button already exists');
        return;
    }

    console.log('YouTube AI Assistant: Creating button...');

    // Wait for YouTube's UI to be ready
    const maxAttempts = 10;
    let attempts = 0;

    const tryCreateButton = () => {
        attempts++;
        
        // Try different possible containers for YouTube's action buttons
        const possibleContainers = [
            '#actions-inner', // New YouTube layout
            '#top-level-buttons-computed',
            '#menu-container ytd-menu-renderer',
            '#above-the-fold #actions',
            'ytd-watch-flexy #actions',
            '#primary #actions',
            'ytd-watch-metadata #actions',
            '#bottom-row #actions'
        ];

        let container = null;
        
        for (const selector of possibleContainers) {
            container = document.querySelector(selector);
            if (container) {
                console.log('YouTube AI Assistant: Found container:', selector);
                break;
            }
        }

        // If no container found, try to find by text content
        if (!container) {
            const likeButtons = document.querySelectorAll('ytd-toggle-button-renderer, ytd-button-renderer, ytd-menu-renderer');
            for (let element of likeButtons) {
                if (element.textContent.includes('Like') || element.textContent.includes('Dislike') || element.textContent.includes('Share')) {
                    container = element.parentElement;
                    if (container) break;
                }
            }
        }

        if (container) {
            createButtonInContainer(container);
        } else if (attempts < maxAttempts) {
            console.log(`YouTube AI Assistant: Container not found, retrying... (${attempts}/${maxAttempts})`);
            setTimeout(tryCreateButton, 500);
        } else {
            console.log('YouTube AI Assistant: Failed to find container, creating floating button');
            createFloatingButton();
        }
    };

    tryCreateButton();
}

function createButtonInContainer(container) {
    const button = document.createElement('button');
    button.id = 'ai-assistant-btn';
    button.innerHTML = `
        <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" style="margin-right: 8px;">
            <path d="M21 6h-2v9H6v2c0 .55.45 1 1 1h11l4 4V7c0-.55-.45-1-1-1zm-4 6V3c0-.55-.45-1-1-1H3c-.55 0-1 .45-1 1v14l4-4h11c.55 0 1-.45 1-1z"/>
        </svg>
        Ask AI
    `;
    
    // Style for inline placement
    button.style.cssText = `
        display: inline-flex;
        align-items: center;
        background: linear-gradient(135deg, #ff0000, #cc0000);
        color: white;
        border: none;
        padding: 10px 16px;
        border-radius: 18px;
        cursor: pointer;
        font-weight: 500;
        font-size: 14px;
        font-family: 'Roboto', 'Arial', sans-serif;
        margin-left: 8px;
        transition: all 0.3s ease;
        white-space: nowrap;
    `;

    button.addEventListener('mouseenter', () => {
        button.style.transform = 'translateY(-2px)';
        button.style.boxShadow = '0 4px 12px rgba(255, 0, 0, 0.3)';
    });

    button.addEventListener('mouseleave', () => {
        button.style.transform = 'translateY(0)';
        button.style.boxShadow = 'none';
    });

    button.addEventListener('click', showAIBox);

    // Insert after the last button in the container
    const lastButton = container.lastElementChild;
    if (lastButton) {
        lastButton.after(button);
    } else {
        container.appendChild(button);
    }

    console.log('YouTube AI Assistant: Button created successfully in container');
}

function createFloatingButton() {
    const button = document.createElement('button');
    button.id = 'ai-assistant-btn';
    button.innerHTML = `
        <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
            <path d="M21 6h-2v9H6v2c0 .55.45 1 1 1h11l4 4V7c0-.55-.45-1-1-1zm-4 6V3c0-.55-.45-1-1-1H3c-.55 0-1 .45-1 1v14l4-4h11c.55 0 1-.45 1-1z"/>
        </svg>
        Ask AI
    `;
    
    // Style for floating placement
    button.style.cssText = `
        position: fixed;
        bottom: 100px;
        right: 20px;
        background: linear-gradient(135deg, #ff0000, #cc0000);
        color: white;
        border: none;
        padding: 12px 20px;
        border-radius: 25px;
        cursor: pointer;
        z-index: 9999;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        font-weight: 600;
        font-size: 14px;
        display: flex;
        align-items: center;
        gap: 8px;
        transition: all 0.3s ease;
        font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
    `;

    button.addEventListener('mouseenter', () => {
        button.style.transform = 'translateY(-2px) scale(1.05)';
        button.style.boxShadow = '0 6px 20px rgba(255, 0, 0, 0.4)';
    });

    button.addEventListener('mouseleave', () => {
        button.style.transform = 'translateY(0) scale(1)';
    });

    button.addEventListener('click', showAIBox);

    document.body.appendChild(button);
    console.log('YouTube AI Assistant: Floating button created');
}

function showAIBox() {
    console.log('YouTube AI Assistant: Showing AI box');
    
    // Remove existing AI box if any
    const existingBox = document.getElementById('ai-box');
    if (existingBox) {
        existingBox.remove();
        return;
    }

    const aiBox = document.createElement('div');
    aiBox.id = 'ai-box';
    aiBox.innerHTML = `
        <div id="ai-header">
            YouTube AI Assistant
            <span id="close-ai">✖</span>
        </div>
        <div id="ai-input-container">
            <textarea 
                id="ai-input" 
                placeholder="Ask anything about this video... (e.g., What are the main points? Can you summarize this?)"
                maxlength="1000"
            ></textarea>
            <div style="font-size: 12px; color: #666; text-align: right; margin-top: 4px;">
                <span id="char-count">0</span>/1000
            </div>
        </div>
        <div id="ai-controls">
            <button id="ai-send">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/>
                </svg>
                Send
            </button>
            <button id="ai-clear">Clear</button>
        </div>
        <div id="ai-response">
            <div style="text-align: center; color: #666; padding: 20px;">
                <svg width="48" height="48" viewBox="0 0 24 24" fill="#666" style="margin-bottom: 8px;">
                    <path d="M21 6h-2v9H6v2c0 .55.45 1 1 1h11l4 4V7c0-.55-.45-1-1-1zm-4 6V3c0-.55-.45-1-1-1H3c-.55 0-1 .45-1 1v14l4-4h11c.55 0 1-.45 1-1z"/>
                </svg>
                <div>Ask me anything about this video!</div>
            </div>
        </div>
    `;
    
    document.body.appendChild(aiBox);

    // Add event listeners
    document.getElementById('close-ai').onclick = () => aiBox.remove();
    document.getElementById('ai-send').onclick = sendQuestionToAI;
    document.getElementById('ai-clear').onclick = clearChat;
    
    // Character count
    const textarea = document.getElementById('ai-input');
    const charCount = document.getElementById('char-count');
    
    textarea.addEventListener('input', () => {
        charCount.textContent = textarea.value.length;
        updateSendButton();
    });

    // Enter key support (Ctrl+Enter to send)
    textarea.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
            e.preventDefault();
            sendQuestionToAI();
        }
    });

    textarea.focus();
}

function updateSendButton() {
    const input = document.getElementById('ai-input');
    const sendButton = document.getElementById('ai-send');
    const hasText = input.value.trim().length > 0;
    sendButton.disabled = !hasText;
}

function clearChat() {
    const input = document.getElementById('ai-input');
    const response = document.getElementById('ai-response');
    const charCount = document.getElementById('char-count');
    
    input.value = '';
    response.innerHTML = `
        <div style="text-align: center; color: #666; padding: 20px;">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="#666" style="margin-bottom: 8px;">
                <path d="M21 6h-2v9H6v2c0 .55.45 1 1 1h11l4 4V7c0-.55-.45-1-1-1zm-4 6V3c0-.55-.45-1-1-1H3c-.55 0-1 .45-1 1v14l4-4h11c.55 0 1-.45 1-1z"/>
            </svg>
            <div>Ask me anything about this video!</div>
        </div>
    `;
    charCount.textContent = '0';
    updateSendButton();
    input.focus();
}

function sendQuestionToAI() {
    const query = document.getElementById('ai-input').value.trim();
    const responseDiv = document.getElementById('ai-response');
    const sendButton = document.getElementById('ai-send');

    if (!query) return;

    console.log('YouTube AI Assistant: Sending question:', query);

    // Show loading state
    responseDiv.innerHTML = `
        <div style="padding: 20px; text-align: center;">
            <div class="loading-dots" style="display: inline-flex; gap: 4px; margin-bottom: 8px;">
                <span style="width: 8px; height: 8px; border-radius: 50%; background: #1a73e8; animation: bounce 1.4s infinite ease-in-out;"></span>
                <span style="width: 8px; height: 8px; border-radius: 50%; background: #1a73e8; animation: bounce 1.4s infinite ease-in-out; animation-delay: -0.32s;"></span>
                <span style="width: 8px; height: 8px; border-radius: 50%; background: #1a73e8; animation: bounce 1.4s infinite ease-in-out; animation-delay: -0.16s;"></span>
            </div>
            <div style="color: #666;">Thinking...</div>
        </div>
    `;

    sendButton.disabled = true;
    sendButton.innerHTML = `
        <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 4V1L8 5l4 4V6c3.31 0 6 2.69 6 6 0 1.01-.25 1.97-.7 2.8l1.46 1.46C19.54 15.03 20 13.57 20 12c0-4.42-3.58-8-8-8zm0 14c-3.31 0-6-2.69-6-6 0-1.01.25-1.97.7-2.8L5.24 7.74C4.46 8.97 4 10.43 4 12c0 4.42 3.58 8 8 8v3l4-4-4-4v3z"/>
        </svg>
        Processing...
    `;

    // Get video context for better responses
    const videoTitle = document.querySelector('h1.ytd-watch-metadata, ytd-watch-metadata h1, #container h1.title')?.textContent?.trim() || 'this video';
    const enhancedQuery = `About the YouTube video "${videoTitle}": ${query}`;

    chrome.runtime.sendMessage(
        { 
            action: 'askGemini', 
            question: enhancedQuery,
            videoId: getCurrentVideoId()
        },
        (res) => {
            console.log('YouTube AI Assistant: Received response:', res);
            
            sendButton.disabled = false;
            sendButton.innerHTML = `
                <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/>
                </svg>
                Send
            `;

            if (!res) {
                showError('No response received. Please check your connection and try again.');
                return;
            }

            if (res.error) {
                showError(res.error);
            } else if (res.answer) {
                showResponse(res.answer);
            } else {
                showError(res,'Unexpected response format from AI service.');
            }
        }
    );
}

function showResponse(answer) {
    const responseDiv = document.getElementById('ai-response');
    responseDiv.innerHTML = `
        <div style="padding: 16px; background: #e6f4ea; border-radius: 8px; border-left: 4px solid #34a853;">
            <div style="font-size: 14px; line-height: 1.5; color: #137333;">
                ${answer.replace(/\n/g, '<br>')}
            </div>
        </div>
    `;
}

function showError(error) {
    const responseDiv = document.getElementById('ai-response');
    responseDiv.innerHTML = `
        <div style="padding: 16px; background: #fce8e6; border-radius: 8px; border-left: 4px solid #ea4335;">
            <div style="font-size: 14px; line-height: 1.5; color: #c5221f;">
                <strong>Error:</strong> ${error}
            </div>
        </div>
    `;
}

// Add CSS for loading animation
const style = document.createElement('style');
style.textContent = `
    @keyframes bounce {
        0%, 80%, 100% {
            transform: scale(0);
        }
        40% {
            transform: scale(1);
        }
    }
`;
document.head.appendChild(style);

// Initial initialization
setTimeout(init, 2000);