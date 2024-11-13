const likeContainer = document.getElementById('like-container');
const likesCountElem = document.getElementById('like-count');
const likeButton = document.getElementById('like-button');

const dreamId = likeContainer ? likeContainer.getAttribute('data-dream-id') : null;
console.log("dreamId:", dreamId);

let isLiked;

const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
const ws = new WebSocket(`${protocol}://${window.location.host}/ws/like/dream/${dreamId}/`);



ws.onmessage = (event) => {
    console.log("Отримані дані:", event.data); // Перевірка цілісності даних
    const data = JSON.parse(event.data);
    console.log("Дані після парсингу:", data);
    console.log("action:", data.action);

    if (data.action === 'initial_like_status') {
        isLiked = data.is_liked;
        likesCountElem.textContent = data.likes_count;

    } else if (data.action === 'like_update') {
        likesCountElem.textContent = data.likes_count;
    }
};

likeButton.onclick = () => {

    if (!isLiked) {
        ws.send(JSON.stringify({ 'action': 'like' }));
        isLiked = true;
    } else {
        ws.send(JSON.stringify({ 'action': 'unlike' }));
        isLiked = false;
    }
};
