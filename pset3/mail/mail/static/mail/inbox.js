document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');

  // Add event listener on each email div
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  // event listener for form
  document.querySelector('#compose-form').onsubmit = () => send_email();
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  const emails_div = document.querySelector("#emails-view")

  // Fetch the mailbox requested 
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    // console.log (emails)
    // iterate through each email
    for (email in emails) {
      console.log('email', emails[email]);
      // Create card div
      const card = document.createElement('div');
      card.classList.add('card');
      card.classList.add('flex-row');
      card.classList.add('d-flex');
      card.classList.add('bd-highlight'); 
      card.classList.add('justify-content-start'); 
      
      // If the email has been read, it should appear with a gray background.
      if (emails[email]['read']) {
        card.classList.add('bg-secondary');
        // card.classList.add('text-white');
      }
      
      // Create div for our subject
      const subject = document.createElement('div');
      subject.classList.add('p-2');
      subject.classList.add('flex-grow-1');
      subject.classList.add('bd-highlight');
      subject.innerHTML = emails[email]['subject'];

      // Create div for our sender
      const sender = document.createElement('div');
      sender.classList.add('p-2');
      sender.classList.add('bd-highlight');
      const strongsender = document.createElement('strong');
      strongsender.innerHTML = emails[email]['sender'];
      sender.append(strongsender);

      // Create div for our timestamp
      const timestamp = document.createElement('div');
      timestamp.classList.add('p-2');
      timestamp.classList.add('bd-highlight');
      timestamp.classList.add('ml-auto');
      timestamp.innerHTML = emails[email]['timestamp'];

      // Add all elements to the card
      card.append(sender);
      card.append(subject);
      card.append(timestamp);

      // Add emails to the emails-view div 
      emails_div.append(card);

      // add event listener to email div
      card.addEventListener('click', function() {
        fetch(`/emails/${emails[email]['id']}`)
        .then(response => response.json())
        .then(email => {
            console.log(email);

            // Update the email to read = true
            if (email['read'] === false) {
              fetch(`/emails/${email['id']}`, {
                method: 'PUT',
                body: JSON.stringify({
                    read: true
                })
              })
            }
            // console.log('read? ', email);

            // clear our emails view
            document.querySelector('#emails-view').innerHTML = '';
            
            // show the email’s sender, recipients, subject, timestamp, and body.
            const div = document.createElement('div');

            // Email Sender
            const email_sender = document.createElement('p');
            const email_from = document.createElement('strong');
            email_from.innerHTML = 'From: ';
            email_sender.append(email_from);
            email_sender.append(email['sender']);
            email_sender.classList.add('m-0');

            // Email Recipients
            const email_recipients = document.createElement('p');
            const email_to = document.createElement('strong');
            email_to.innerHTML = 'To: ';
            email_recipients.append(email_to);
            email_recipients.append(email['recipients']);
            email_recipients.classList.add('m-0');

            // Email Subject
            const email_subject_info = document.createElement('p');
            const email_subject= document.createElement('strong');
            email_subject.innerHTML = 'Subject: ';
            email_subject_info.append(email_subject);
            email_subject_info.append(email['subject']);
            email_subject_info.classList.add('m-0');

            // Email Timestamp
            const email_timestamp_info = document.createElement('p');
            const email_timestamp= document.createElement('strong');
            email_timestamp.innerHTML = 'Timestamp: ';
            email_timestamp_info.append(email_timestamp);
            email_timestamp_info.append(email['timestamp']);
            email_timestamp_info.classList.add('m-0');

            // Add an <hr>
            const hr = document.createElement('hr');

            // Email Body
            const body = document.createElement('div');
            body.innerHTML = email['body'];


            // Reply form and button

            //create a form
            const btn = document.createElement('button');
            btn.classList.add('btn');
            btn.classList.add('btn-sm');
            btn.classList.add('btn-outline-primary');
            btn.innerHTML = 'Reply';

            // Example from https://stackoverflow.com/questions/3297143/dynamically-create-a-html-form-with-javascript
            // var f = document.createElement("form");
            // f.setAttribute('method',"post");
            // f.setAttribute('action',"submit.php");

            // //create input element
            // var i = document.createElement("input");
            // i.type = "text";
            // i.name = "user_name";
            // i.id = "user_name1";

            // //create a checkbox
            // var c = document.createElement("input");
            // c.type = "checkbox";
            // c.id = "checkbox1";
            // c.name = "check1";

            // //create a button
            // var s = document.createElement("input");
            // s.type = "submit";
            // s.value = "Submit";

            // // add all elements to the form
            // f.appendChild(i);
            // f.appendChild(c);
            // f.appendChild(s);

            // // add the form inside the body
            // $("body").append(f);   //using jQuery or
            // document.getElementsByTagName('body')[0].appendChild(f); //pure javascript

            // Append elements to the new div
            div.append(email_sender);
            div.append(email_recipients);
            div.append(email_subject_info);
            div.append(email_timestamp_info);
            div.append(btn);
            div.append(hr);
            div.append(body);
            emails_div.append(div);
      });
      });
    }
  });
}

function send_email() {
  console.log('fetching data')
  // Prepare data to submit via POST method
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: document.querySelector('#compose-recipients').value,
        subject: document.querySelector('#compose-subject').value,
        body: document.querySelector('#compose-body').value
    })
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      console.log(result);
      if (result[message] === "Email sent successfully") {
        // Show the mailbox and hide other views
        document.querySelector('#sent-view').style.display = 'block';
        document.querySelector('#compose-view').style.display = 'none';
      }
  });

  // Stop form from submitting
  return false;
}