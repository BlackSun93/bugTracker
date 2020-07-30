document.addEventListener('DOMContentLoaded', function() {
    console.log('loaded'); 
    bugElement = document.getElementById('bugObjectDiv');
    bugInfo = bugElement.dataset.bug;
    //bugJson = JSON.parse(bugJson);
    console.log(bugJson);
    document.getElementById('updateForm').onsubmit = createUpdate;
    
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
    alert(newUpdate);
    fetch('newUpdate/', {
        method: 'POST',
        body: JSON.stringify({
            newUpdate: newUpdate,
            newStatus:  newStatus
        })
    })
    alert('Update posted!');
}