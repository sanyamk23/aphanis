// Untrace AI Content Script
// Detects AI-generated text in web page textareas and offers a floating clean button.

(function() {
  'use strict';

  // Create floating action button
  let fab;

  function createButton() {
    fab = document.createElement('button');
    fab.id = 'untrace-fab';
    fab.textContent = '🛡️';
    fab.title = 'Untrace AI - Remove AI watermarks from this text';
    fab.style.cssText = `
      position: fixed;
      bottom: 20px;
      right: 20px;
      width: 56px;
      height: 56px;
      border-radius: 50%;
      border: none;
      background: #6366f1;
      color: white;
      font-size: 24px;
      cursor: pointer;
      z-index: 999999;
      box-shadow: 0 4px 12px rgba(0,0,0,0.3);
      transition: transform 0.2s;
    `;
    fab.addEventListener('click', () => {
      const activeEl = document.activeElement;
      if (activeEl && (activeEl.tagName === 'TEXTAREA' || activeEl.tagName === 'INPUT' || activeEl.isContentEditable)) {
        // Send to background for processing
        chrome.runtime.sendMessage({
          action: 'cleanSelected',
          text: activeEl.value || activeEl.textContent
        }, (response) => {
          if (response && response.cleaned) {
            if (activeEl.tagName === 'TEXTAREA' || activeEl.tagName === 'INPUT') {
              activeEl.value = response.cleaned;
            } else {
              activeEl.textContent = response.cleaned;
            }
          }
        });
      } else {
        // Try to clean the visible text content
        const text = window.getSelection().toString() || document.body.innerText;
        chrome.runtime.sendMessage({
          action: 'cleanSelected',
          text: text
        }, (response) => {
          if (response && response.cleaned) {
            navigator.clipboard.writeText(response.cleaned).then(() => {
              alert('✅ Cleaned text copied to clipboard!');
            });
          }
        });
      }
    });
    document.body.appendChild(fab);
  }

  // Create button after page loads
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', createButton);
  } else {
    createButton();
  }

  // Hover effect
  if (fab) {
    fab.addEventListener('mouseenter', () => fab.style.transform = 'scale(1.1)');
    fab.addEventListener('mouseleave', () => fab.style.transform = 'scale(1)');
  }
})();
