// Save Bearer token to localStorage on change
window.addEventListener('DOMContentLoaded', function() {
    const key = 'swagger_access_token';
    // Restore token from localStorage
    const stored = localStorage.getItem(key);
    if (stored) {
        const input = document.querySelector('input[placeholder="api_key"]');
        if (input) {
            input.value = stored;
            input.dispatchEvent(new Event('input', { bubbles: true }));
        }
    }
    // Listen for changes
    document.body.addEventListener('input', function(e) {
        if (e.target && e.target.placeholder === 'api_key') {
            localStorage.setItem(key, e.target.value);
        }
    });
});
