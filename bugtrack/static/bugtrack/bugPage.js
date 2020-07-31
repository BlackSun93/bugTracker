document.addEventListener('DOMContentLoaded', function() {
    console.log('loaded'); 
    bugElement = document.getElementById('bugObjectDiv');
    bugInfo = bugElement.dataset.bug;
    //bugJson = JSON.parse(bugJson);
    console.log(bugJson);
    try {
        document.getElementById('updateForm').onsubmit = createUpdate;
    }
    catch {
        console.log('update form is not here');
    }
    
    
});

function hello() {
    alert('hello');
}

function solverButton(userId){ //should standardise whether or not to make elements in JS or in html really
    buttonDiv = document.getElementById('solverButtonDiv');
    button = document.createElement('button');
    button.setAttribute('class', 'btn btn-success');
    button.innerHTML = 'Solve this bug!';
    button.addEventListener('click', function() {
        alert(bugJson);
        fetch(`newSolver/`, {
            method : 'POST',
            body: JSON.stringify ({
                userId: userId,
                bugId: bugJson.id
            })
        })
    })
    buttonDiv.append(button);
}

function createUpdate() {
    newUpdate = document.getElementById('updateText').value;
    newStatus = document.getElementById('updateStatus').value;
    bugId = bugJson.id;
    alert(newUpdate);
    fetch('newUpdate/', {
        method: 'POST',
        body: JSON.stringify({
            newUpdate: newUpdate,
            newStatus:  newStatus,
            bugId: bugId
        })
    })
    alert('Update posted!');
}

function solution(bugId, userId) {
    solutionDiv = document.getElementById('solutionDiv');
    solutionBtn = document.createElement('button');
    solutionBtn.setAttribute('class', 'btn btn-success');
    solutionBtn.innerHTML = 'This solution worked!';
    solutionBtn.addEventListener('click', function() {
        fetch(`bugSolved/${bugId}`, {
            method: 'POST',
            body: JSON.stringify({ //no need to send any data regarding 'is finished' or anything, can just set 'fixed' to 'true' in views
                userId: userId,
            })
        })
    })
    solutionDiv.append(solutionBtn);
}