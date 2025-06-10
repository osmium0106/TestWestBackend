// Dynamically show/hide option fields in the bulk upload form based on question_type
(function() {
    document.addEventListener('DOMContentLoaded', function() {
        // Only run if the form is present
        var form = document.querySelector('form');
        if (!form) return;
        // This is a bulk upload, so only the file field is present, but this is a placeholder for future per-row UI
        // If you add per-row UI, you can use this script to show/hide option fields based on question_type
    });
})();
