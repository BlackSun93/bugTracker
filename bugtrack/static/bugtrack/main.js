document.addEventListener('DOMContentLoaded', function() {
    console.log('loaded');
    document.getElementById('bugReportForm').onsubmit = createBug; 
    try {
      if (document.getElementById('header').dataset.header == 'finishedBugs') {
      document.getElementById('bugReport').style.display = 'none';
    }
    }
    catch {
      console.log('You are on the normal index page and not finished bugs page');
    }
    
   
});

function createBug() {
  const newBugTitle = document.getElementById('bugTitle').value;
  const newBugLocation = document.getElementById('bugLocation').value;
  const newBugDesc = document.getElementById('bugDesc').value;
  const newBugPriority = document.getElementById('bugPriority').value;
  alert(newBugTitle + newBugLocation + newBugDesc + newBugPriority);

  fetch('/createBug/' , {
      method: 'POST',
      body: JSON.stringify({title: newBugTitle, location: newBugLocation, description: newBugDesc, priority: newBugPriority })
  })
  .then(response => response.json(console.log()))
  
  alert('Bug made Successfully!'); //needs this for post to send
}


  function hello() {
      alert('hello');
  }