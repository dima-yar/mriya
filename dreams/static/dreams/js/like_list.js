const likesCountElem = document.getElementById('like-count');

const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
const ws = new WebSocket(`${protocol}://${window.location.host}/ws/like/dream/main_page/`);



ws.onmessage = (event) => {
    console.log("Отримані дані:", event.data); // Перевірка цілісності даних
    const data = JSON.parse(event.data);
    console.log("likes_count:",data.likes_count);
    console.log("action:", likesCountElem.textContent);

    if (data.action === 'initial_like_status') {
        isLiked = data.is_liked;
        likesCountElem.textContent = data.like_count;

    } else if (data.action === 'like_update') {
        likesCountElem.textContent = data.like_count;
    }
};
