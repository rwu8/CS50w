document.addEventListener('DOMContentLoaded', function() {
    // const cards = document.querySelectorAll('.edit-link');
    const edit_buttons = document.querySelectorAll('.edit-link');
    const like_buttons = document.querySelectorAll('.like-link');

    edit_buttons.forEach(button => button.addEventListener('click', () => {
        console.log(button['parentElement'])
        createForm(button['parentElement']['parentElement']);
        return false;
        })
    )

    like_buttons.forEach(button => button.addEventListener('click', () => {
        const post_id = button.getAttribute('data-id').split('-')[1];

        // set our CSRF token for AJAX request: https://docs.djangoproject.com/en/dev/ref/csrf/#ajax
        const csrftoken = getCookie('csrftoken');
        const request = new Request(
            `/like/${post_id}`,
            {headers: {'X-CSRFToken': csrftoken}}
        );

        // update our post
        fetch(request, {
            method: 'POST',
            mode: 'same-origin',
            body: JSON.stringify({
                id: post_id,
                }),
        })

        // Fetch the mailbox requested 
        fetch(`/like/${post_id}`)
        .then(response => response.json())
        .then(likes => {
            button['children'][1].innerHTML = likes;
        })
    }))
}) 

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function createForm(parentElem) {
    const body = parentElem['children'][1];
    // console.log(body);
    const post_id = parentElem['id'].split('-')[1];
    const old_body_content = body['children'][1].innerHTML;
    body.innerHTML = '';

    const form = document.createElement('form');
    form.classList.add('mb-3');
    form.setAttribute('data-id', parentElem['id'])
    form.action = `/post/${post_id}`

    const div = document.createElement('div');
    div.classList.add('form-group');

    const label = document.createElement('label');
    label.innerHTML = 'Edit Post';
    label.htmlFor = 'postContent';

    const textarea = document.createElement('textarea');
    textarea.classList.add('form-control');
    textarea.id = 'postContent';
    textarea.name = 'post';
    textarea.rows = 3;
    textarea.value = old_body_content;

    div.append(label);
    div.append(textarea);
    
    const input = document.createElement('input');
    input.classList.add('btn');
    input.classList.add('btn-primary');
    input.value = 'Post';
    input.type = 'submit';
    

    form.append(div);
    form.append(input);
    form.onsubmit = (e) => {
        // get data to update
        const post_id = e['target'].getAttribute('data-id').split('-')[1];
        const updated_post = e['target'][0].value;
        console.log(post_id, updated_post);

        // set our CSRF token for AJAX request: https://docs.djangoproject.com/en/dev/ref/csrf/#ajax
        const csrftoken = getCookie('csrftoken');
        const request = new Request(
            `/post/${post_id}`,
            {headers: {'X-CSRFToken': csrftoken}}
        );

        // update our post
        fetch(request, {
            method: 'PUT',
            mode: 'same-origin',
            body: JSON.stringify({
                id: post_id,
                body: updated_post
                }),
        })
        
        body.innerHTML = '';
        replacePostContent(post_id, body, updated_post);
        
        // Stop form from submitting
        return false;
    }
    
    body.append(form);
}

function replacePostContent(post_id, parent, updated_post) {
    const a = document.createElement('a');
    a.href = "#";
    a.classList.add('text-decoration-none');
    a.classList.add('edit-link');
    a.setAttribute('aria-hidden', 'true');
    a.setAttribute('data-id', `post-${post_id}`);
    a.innerHTML = 'Edit';

    const post_body = document.createElement('pre');
    post_body.classList.add('card-text');
    post_body.style.fontFamily = '-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Oxygen, Ubuntu, Cantarell, Open Sans, Helvetica Neue, sans-serif';
    post_body.innerHTML = updated_post;

    const likes = document.createElement('a');
    likes.classList.add('text-decoration-none');
    likes.classList.add('like-link');
    likes.setAttribute('data-id', `post-${post_id}`);
    const heart_icon = document.createElement('i');
    heart_icon.classList.add('fa');
    heart_icon.classList.add('fa-heart');
    heart_icon.setAttribute('aria-hidden', 'true');
    heart_icon.style.color =  'red';
    const num_likes = document.createElement('span');
    num_likes.id = 'num-likes';
    num_likes.innerHTML = ' 0';
    likes.append(heart_icon);
    likes.append(num_likes);

    const comment = document.createElement('p');
    const comment_link = document.createElement('a');
    comment_link.href = `/comment/${post_id}`;
    comment_link.classList.add('btn');
    comment_link.classList.add('btn-primary');
    comment_link.innerHTML = 'Comment';
    comment.append(comment_link);

    parent.append(a);
    parent.append(post_body);
    parent.append(likes);
    parent.append(comment);
}