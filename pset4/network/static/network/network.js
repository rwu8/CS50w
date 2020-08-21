document.addEventListener('DOMContentLoaded', function() {
    // const cards = document.querySelectorAll('.edit-link');
    const edit_buttons = document.querySelectorAll('.edit-link');
    
    edit_buttons.forEach(button => button.addEventListener('click', () => {
        createForm(button['parentElement']['parentElement']);
        return false;
        })
    )
}) 

function createForm(parentElem) {
    const body = parentElem['children'][1];
    console.log(body);
    const old_body_content = body['children'][1].innerHTML;
    body.innerHTML = '';

    const form = document.createElement('form');
    form.classList.add('mb-3');

    const inputElem = document.createElement('input');
    inputElem.type = 'hidden';
    inputElem.name = 'csrfmiddlewaretoken';
    inputElem.value = CSRF_TOKEN;
    form.appendChild(inputElem);

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
    form.onsubmit = () => {
        console.log('submitted!');
        // TODO need to async update the data


        // Stop form from submitting
        return false;
    }
    
    body.append(form);
}