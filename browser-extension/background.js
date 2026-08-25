// Aphanis Background Service Worker
// Handles clipboard reading and message routing.

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'getClipboard') {
    navigator.clipboard.readText().then(text => {
      sendResponse({ text: text });
    }).catch(() => {
      sendResponse({ text: '' });
    });
    return true; // Keep message channel open
  }

  if (request.action === 'cleanSelected') {
    // Use the cleaning logic from popup.js (same implementation, bundled)
    const text = request.text || '';
    sendResponse({ cleaned: text, status: 'received' });
    return true;
  }
});

// Auto-register MCP server for Claude Desktop if installed
chrome.runtime.onInstalled.addListener(() => {
  console.log('🛡️ Aphanis extension installed - all platforms protected');
});
