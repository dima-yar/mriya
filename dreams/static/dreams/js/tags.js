        const tagButtons = document.querySelectorAll('.hashtag-button');

        console.log(tagButtons);
        tagButtons.forEach(button => {
            button.addEventListener('click', function() {
                const tagId = this.textContent;
                const url = new URL(window.location.href);
                const params = url.searchParams;
                

                if (!params.getAll('tags').includes(tagId)) {
                    params.append('tags', tagId);
                }
                
                // Оновлюємо URL запиту
                window.location.href = `${url.pathname}?${params.toString()}`;
            });
        });
