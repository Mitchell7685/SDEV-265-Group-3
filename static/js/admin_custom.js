// Debug statement to confirm the script is loading
console.log("TidyTracker Custom Admin JS has loaded!");


document.addEventListener('DOMContentLoaded', function() {
    // Grab every link on the page
    const allLinks = document.querySelectorAll('a');
    
    allLinks.forEach(link => {
        // First check if the link's text is exactly "Change"
        if (link.textContent.trim() === 'Change') {
            
            // Look at the table row this link lives inside
            const row = link.closest('tr');
            
            // If the row contains our specific custom link names
            if (row && (row.textContent.includes('Generate Schedule') || row.textContent.includes('User Dashboard'))) {
                
                // Swap the "Change" text for "Go to Page"
                link.textContent = 'Go to Page';    
            }
        }
    });
});
