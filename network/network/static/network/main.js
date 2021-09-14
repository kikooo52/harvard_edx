document.addEventListener('DOMContentLoaded', function() {
    var editPost = document.querySelectorAll(".editPost");
    editPost.forEach((element) => {
        element.addEventListener("click", () => {
        edit_post(element);
        });
    });

    var likePost = document.querySelectorAll(".likePost");
    likePost.forEach((element) => {
        element.addEventListener("click", () => {
        like_post(element);
        });
    });    
});

function edit_post(element) {
    var contentElement = element.parentElement.querySelector('.postConent');
    document.getElementById('editPostContent').value = contentElement.innerText;
    document.getElementById('post_id').value = contentElement.dataset.postId
    document.getElementById('buttonModal').click();
}

function like_post(element) {
    var contentElement = element.parentElement.querySelector('.postConent');
    var postId = contentElement.dataset.postId;
    fetch(`/like_post/${postId}`, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.cookie.match(/csrftoken=([\w-]+)/)[1],
        },
    })
    .then(response => response.json())
    .then(result => {
        if (result.likes >= 1){
            element.classList.remove("noLikes");
            element.classList.add("hasLikes");
        } else {
            element.classList.remove("hasLikes");
            element.classList.add("noLikes");
        }

        element.innerHTML = " " + result.likes;
    })
    .catch(error => console.error(error));    
}
