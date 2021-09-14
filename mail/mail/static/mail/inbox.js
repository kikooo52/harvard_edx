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
  document.querySelector(".helpBlock").style.display = 'none';
}

function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
      let table = document.createElement('table');
      table.className = 'table table-hover';
      emails.forEach(email => {

        let tr = document.createElement('tr');
        if (!email.read) {
          tr.className = 'mailRead';
        }

        let td1 = document.createElement('td');
        td1.style.width = '35%';

        let td2 = document.createElement('td');
        td2.style.width = '45%';

        let td3 = document.createElement('td');
        td3.style.width = '20%';
        
        let text1 = document.createTextNode(mailbox != "sent" ? email.sender : email.recipients);
        let text2 = document.createTextNode(email.subject);
        let text3 = document.createTextNode(email.timestamp);
    
        td1.appendChild(text1);
        td2.appendChild(text2);
        td3.appendChild(text3);
        tr.appendChild(td1);
        tr.appendChild(td2);
        tr.appendChild(td3);
    
        tr.addEventListener("click", () => get_email(email.id, mailbox));
        table.appendChild(tr);

        
      });
      document.querySelector('#emails-view').appendChild(table);
      console.log(emails);
    })
    .catch((error) => console.error(error));
}


function send() {
  event.preventDefault();      
  fetch("/emails", {
    method: "POST",
    body: JSON.stringify({
        recipients: document.querySelector("#compose-recipients").value,
        subject: document.querySelector("#compose-subject").value,
        body: document.querySelector("#compose-body").value,
      }),
    })
    .then((response) => response.json())
    .then((result) => {
      console.log(result);
      if (result.error) {
        document.querySelector(".helpBlock").innerHTML = result.error;
        document.querySelector(".helpBlock").style.display = 'inline-block';
        document.querySelector("#compose-recipients").scrollIntoView();
      }
      else {
        load_mailbox('sent')
      }          
    })
    .catch((error) => console.error(error));
}

function get_email(email_id, mailbox) {
  fetch(`emails/${email_id}`)
  .then(response => response.json())
  .then(email => {
    let table = document.createElement('table');
    document.querySelector("#emails-view").innerHTML = "";
    let fields = [
      "sender",
      "recipients",
      "subject",
      "timestamp",
      "body"
    ];

    for (let i=0, a=fields, l=a.length; i<l; i++) {
      if (email.hasOwnProperty(a[i])) {
        let tr = document.createElement('tr');
        let td = document.createElement('td');
        if (a[i] == "body") {

          // Reply mail button
          let reply = document.createElement('button');
          reply.className = 'btn btn-sm btn-outline-primary';
          reply.textContent = "Reply";
          reply.addEventListener("click", () => reply_mail(email, mailbox));
          td.appendChild(reply);

          if (mailbox != "sent") {
            // Archive mail button
            let archive = document.createElement('button');
            archive.className = 'btn btn-sm btn-outline-primary archiveButton';
            email.archived ? archive.textContent = "Unarchive" : archive.textContent = "Aarchive";
            archive.addEventListener("click", () => archive_mail(email_id, !email.archived));
            td.appendChild(archive);
          }

          // Mail body 
          let div = document.createElement("div");
          div.className = 'mailBody';
          div.innerHTML = email[a[i]];
          td.appendChild(div);
          tr.appendChild(td);
        } else {
          // Title
          let title = a[i].replace(/\b[a-z]/g, (x) => x.toUpperCase())
          let bold = document.createElement("b");
          bold.innerHTML = title;
          td.appendChild(bold);
          // Value
          let text = document.createTextNode(": " + email[a[i]]);
          td.appendChild(text);
          tr.appendChild(td);
        }

        table.appendChild(tr);
      }
    }
    document.querySelector('#emails-view').appendChild(table);

    // Update to read mail 
    if (!email.read) {
      fetch(`/emails/${email_id}`, {
        method: 'PUT',
        body: JSON.stringify({
          read: true
        })
      })
    }

    console.log(email);
  })
  .catch((error) => console.error(error));
}

function reply_mail(email, mailbox) {
  compose_email();

  let sender =  mailbox != "sent" ? email.sender : email.recipients;
  let subject = email.subject.search("Re") ? email.subject : `Re: ${email.subject}`;
  document.querySelector('#compose-recipients').value = sender;
  document.querySelector('#compose-subject').value = subject;
  document.querySelector('#compose-body').value = `On ${email.timestamp} ${sender} wrote:\n${email.body}\n\n`;
  document.querySelector('#compose-body').focus();
}

function archive_mail(email_id, archive) {
  fetch(`/emails/${email_id}`, {
    method: "PUT",
    body: JSON.stringify({
      archived: archive,
    }),
  })
  .then(() => load_mailbox("inbox"));
}
