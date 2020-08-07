document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  // event listener for reply button
  document.querySelector('#compose-form').onsubmit = () => send_email();  
}

function generate_emails(emails, mailbox) {
  // clear our emails view
  document.querySelector('#emails-view').innerHTML = '';
  const emails_div = document.querySelector("#emails-view")

  // loop through the emails
  for (email in emails) {
    // console.log('email', emails[email]);
    // Create card div
    const card = document.createElement('div');
    card.classList.add('card');
    card.classList.add('flex-row');
    card.classList.add('d-flex');
    card.classList.add('bd-highlight'); 
    card.classList.add('justify-content-start'); 
    card.setAttribute('data-id', emails[email]['id']);
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
  }

  document.querySelectorAll('.card').forEach(email => {
    email.addEventListener('click', mail => {
      get_email(mail['target']['offsetParent'].getAttribute('data-id'), mailbox);
    })
  })
}

function get_email(email_id, mailbox) {
  const emails_div = document.querySelector("#emails-view");

  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {
    console.log('in get_email', email);

    // Update the email to read = true
    if (email['read'] === false) {
      fetch(`/emails/${email_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            read: true
        })
      })
    }

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
    const body_content = document.createElement('pre');
    body_content.innerHTML = email['body'];
    body.append(body_content);

    // create Archive button
    let archive_btn = document.createElement('button');
    archive_btn.classList.add('btn');
    archive_btn.classList.add('btn-sm');
    archive_btn.classList.add('btn-outline-primary');
    archive_btn.id = 'archive-btn';

    if (email['archived'] === false) {
      archive_btn.innerHTML = 'Archive';
    } else {
      archive_btn.innerHTML = 'Unarchive';
    }

    if (mailbox === 'sent') {
      archive_btn.style.display = 'none';
      archive_btn.disabled = 'true';
    } else {
      archive_btn.style.display = 'inline';
      archive_btn.disabled = false;
    }

    // create Reply button
    const reply_btn = document.createElement('button');
    reply_btn.classList.add('btn');
    reply_btn.classList.add('btn-sm');
    reply_btn.classList.add('btn-outline-primary');
    reply_btn.innerHTML = 'Reply';

    // Append elements to the new div
    div.append(email_sender);
    div.append(email_recipients);
    div.append(email_subject_info);
    div.append(email_timestamp_info);
    div.append(reply_btn);
    div.append(archive_btn);
    div.append(hr);
    div.append(body);
    emails_div.append(div);

    // event listeners for archive and reply buttons
    reply_btn.addEventListener('click', () => reply_email(email));
    if (mailbox !== 'sent') {
      document.querySelector('#archive-btn').addEventListener('click', () => toggle_archive(email));
    }
  });
}

function load_mailbox(mailbox) {  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Fetch the mailbox requested 
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    generate_emails(emails, mailbox);
  });
}

function reply_email(email) {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Prepopulate the recipients, subject and body with data from previous email
  document.querySelector('#compose-recipients').value = email['sender'];
  document.querySelector('#compose-subject').value = `RE: ${email['subject']}`;
  const now = new Date(); 
  const datetime = "Last Sync: " + now.getDate() + "/"
                  + (now.getMonth()+1)  + "/" 
                  + now.getFullYear() + " @ "  
                  + now.getHours() + ":"  
                  + now.getMinutes() + ":" 
                  + now.getSeconds();
  document.querySelector('#compose-body').value = `On ${datetime} ${email[`sender`]} wrote:\n${email['body']}\n`;

  // event listener for reply button
  document.querySelector('#compose-form').onsubmit = () => send_email();  
}

function send_email() {
  console.log('sending email')
  // Prepare data to submit via POST method
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: document.querySelector('#compose-recipients').value,
        subject: document.querySelector('#compose-subject').value,
        body: document.querySelector('#compose-body').value,
    })
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      console.log(result);
      if (result['message'] == "Email sent successfully") {
        // load mailbox after archive
        load_mailbox('inbox');
      }
  });

  // load sent mailbox
  load_mailbox('sent');

  // Stop form from submitting
  return false;
}

function toggle_archive(email) {
  console.log('toggling archive', email['id']);
  if (email['archived']) {
    fetch(`/emails/${email['id']}`, {
      method: 'PUT',
      body: JSON.stringify({
          archived: false
      })
    })
  } else {
    fetch(`/emails/${email['id']}`, {
      method: 'PUT',
      body: JSON.stringify({
          archived: true
      })
    })
  }
  
  // load inbox after archive
  setTimeout(load_mailbox('inbox'), 1500);
}