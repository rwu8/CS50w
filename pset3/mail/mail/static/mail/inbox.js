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
    // iterate through each email
    // console.log (emails)
    for (email in emails) {
      console.log('email', emails[email]);
      // Create card div
      const card = document.createElement('div');
      card.classList.add('card');
      card.classList.add('flex-row');
      card.classList.add('d-flex');
      card.classList.add('bd-highlight'); 
      card.classList.add('justify-content-start'); 
      // Create div for our subject
      const subject = document.createElement('div');
      subject.classList.add('p-2')
      // subject.classList.add('flex-fill')
      subject.classList.add('flex-grow-1')
      subject.classList.add('bd-highlight')
      subject.innerHTML = emails[email]['subject'];
 
      // const body = document.createElement('div');
      // body.classList.add('p-2')
      // body.classList.add('flex-fill')
      // body.classList.add('bd-highlight')
      // body.innerHTML = emails[email]['body'];

      // Create div for our sender
      const sender = document.createElement('div');
      sender.classList.add('p-2')
      // sender.classList.add('flex-fill')
      sender.classList.add('bd-highlight')
      const strongsender = document.createElement('strong');
      strongsender.innerHTML = emails[email]['sender'];
      sender.append(strongsender)

      // Create div for our timestamp
      const timestamp = document.createElement('div');
      timestamp.classList.add('p-2')
      // timestamp.classList.add('flex-fill')
      timestamp.classList.add('bd-highlight')
      timestamp.classList.add('ml-auto')
      timestamp.innerHTML = emails[email]['timestamp'];

      // Add all elements to the card
      card.append(sender);
      card.append(subject);
      card.append(timestamp);
      // card.append(body);

      // Add emails to the emails-view div 
      emails_div.append(card);
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