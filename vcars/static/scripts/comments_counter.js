document.addEventListener('htmx:afterSwap', function(event) {
    if (event.target.id === 'comments-body') {
        const countElement = document.querySelector('#comments-count');
        if (countElement) {
            const currentCount = parseInt(countElement.textContent) || 0;
            countElement.textContent = currentCount + 1 + ' comments';
        }
    }
});