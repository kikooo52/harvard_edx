document.addEventListener('DOMContentLoaded', function() {
    var bookmarkNews = document.querySelectorAll(".bookmarkNews");
    bookmarkNews.forEach((element) => {
        element.addEventListener("click", () => {
        bookmark_news(element);
        });
    });    
});

function bookmark_news(element) {
    var contentElement = element.parentElement.querySelector('.bookmarkNews');
    var newsId = contentElement.dataset.newsId;
    fetch(`/bookmark_news/${newsId}`, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.cookie.match(/csrftoken=([\w-]+)/)[1],
        },
    })
    .then(response => response.json())
    .then(result => {
        debugger
        if (result.bookmarked){
            element.classList.remove("fa-bookmark-o");
            element.classList.add("fa-bookmark");
        } else {
            element.classList.remove("fa-bookmark");
            element.classList.add("fa-bookmark-o");
        }
    })
    .catch(error => console.error(error));    
}
