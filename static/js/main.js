document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.save-post-btn').forEach(btn => {
        btn.addEventListener('click', event => {
            const postId = event.target.dataset.postId;
            const content = document.querySelector(`#edit-post-content-${postId}`).value;

            fetch(`/edit-post/${postId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': '{{ csrf_token }}',
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: `content=${encodeURIComponent(content)}`
            })
            .then(response => response.json())
            .then(data => {
                if (data.content) {
                    document.querySelector(`#post-content-${postId}`).innerText = data.content;
                    document.querySelector(`#post-content-${postId}`).style.display = 'block';
                    document.querySelector(`#edit-form-${postId}`).style.display = 'none';
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });

    // Actualizar la etiqueta de comentarios al cargar la página
    document.querySelectorAll('.comment-count').forEach(count => {
        const postId = count.dataset.postId;
        const commentsDiv = document.getElementById(`comments-${postId}`);
        if (commentsDiv.style.display === 'block') {
            count.textContent = 'Ocultar comentarios';
        }
    });
});

function showEditForm(event) {
    event.preventDefault();
    const postId = event.target.dataset.postId;
    document.querySelector(`#post-content-${postId}`).style.display = 'none';
    document.querySelector(`#edit-form-${postId}`).style.display = 'block';
}

function toggleComments(postId) {
    const commentsDiv = document.getElementById(`comments-${postId}`);
    const commentCountLabel = document.querySelector(`.comment-count[data-post-id="${postId}"]`);
    if (commentsDiv.style.display === 'none') {
        commentsDiv.style.display = 'block';
        commentCountLabel.textContent = 'Ocultar comentarios';
    } else {
        commentsDiv.style.display = 'none';
        const count = commentCountLabel.dataset.count;
        if (count == 0) {
            commentCountLabel.textContent = '';
        } else if (count == 1) {
            commentCountLabel.textContent = '1 comentario';
        } else {
            commentCountLabel.textContent = `${count} comentarios`;
        }
    }
}

function toggleCommentForm(postId) {
    const commentFormDiv = document.getElementById(`comment-form-${postId}`);
    if (commentFormDiv.style.display === 'none') {
        commentFormDiv.style.display = 'block';
    } else {
        commentFormDiv.style.display = 'none';
    }
}

    document.addEventListener('DOMContentLoaded', () => {
        function timeAgo(date) {
            const now = new Date();
            const seconds = Math.floor((now - date) / 1000);
            const interval = Math.floor(seconds / 31536000); // years
            if (interval > 1) return `hace ${interval} años`;
            else if (interval === 1) return 'hace un año';
    
            const monthInterval = Math.floor(seconds / 2592000); // months
            if (monthInterval > 1) return `hace ${monthInterval} meses`;
            else if (monthInterval === 1) return 'hace un mes';
    
            const weekInterval = Math.floor(seconds / 604800); // weeks
            if (weekInterval > 1) return `hace ${weekInterval} semanas`;
            else if (weekInterval === 1) return 'hace una semana';
    
            const dayInterval = Math.floor(seconds / 86400); // days
            if (dayInterval > 1) return `hace ${dayInterval} días`;
            else if (dayInterval === 1) return 'ayer';
    
            const hourInterval = Math.floor(seconds / 3600); // hours
            if (hourInterval > 1) return `hace ${hourInterval} horas`;
            else if (hourInterval === 1) return 'hace una hora';
    
            const minuteInterval = Math.floor(seconds / 60); // minutes
            if (minuteInterval > 1) return `hace ${minuteInterval} minutos`;
            else if (minuteInterval === 1) return 'hace un minuto';
    
            return 'hace unos segundos';
        }
    
        function updateTimes() {
            document.querySelectorAll('.post-time').forEach(el => {
                const timestamp = new Date(el.dataset.timestamp);
                el.textContent = timeAgo(timestamp);
            });
        }
    
        updateTimes(); // Initial update
    
        setInterval(updateTimes, 60000); // Update every minute
    });