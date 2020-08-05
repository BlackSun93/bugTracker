document.addEventListener('DOMContentLoaded', function() {
    console.log('loaded'); 
    document.getElementById('notSolvedDiv').style.display = 'none';
    bugElement = document.getElementById('bugObjectDiv');
    bugInfo = bugElement.dataset.bug;
    //bugJson = JSON.parse(bugJson);
    console.log(bugJson);
    try {
        document.getElementById('updateForm').onsubmit = createUpdate;
    }
    catch {
        console.log('update form is not here'); //stops the error if the update form isn't going to be generated
    }
    if (bugJson.status == 'finished') {
        console.log('here');
        ifNotFinishedDiv = document.getElementById('ifNotFixedDiv');
        ifNotFinishedDiv.style.display = 'none';
       document.getElementById('updateDiv').style.display = 'none'; 
        //ideally set background to green or some other obvious indicator
    }
    document.getElementById('notSolvedForm').onsubmit = notSolutionForm;

    
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
        fetch(`newSolver/`, {
            method : 'POST',
            body: JSON.stringify ({
                userId: userId,
                bugId: bugJson.id
            })
        })
        alert('a');
        document.getElementById('solverButtonDiv').style.display= 'none';
        document.getElementById('updateDiv').style.display = 'none'; 
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

function notSolution () { //the 'problem not solved' button, on click, should show the form to fill out for why the bug isnt solved
  //  console.log("passed parameters are bugID " + bugId + "and userId " + userId);
    solutionDiv = document.getElementById('solutionDiv');
    notSolutionBtn = document.createElement('button');
    notSolutionBtn.setAttribute('class', 'btn btn-danger');
    notSolutionBtn.innerHTML = 'This solution didnt work!';
    notSolutionBtn.addEventListener('click', function() {
        if (document.getElementById('notSolvedDiv').style.display == 'none') {
            document.getElementById('notSolvedDiv').style.display = 'block';
        }
        else {
            document.getElementById('notSolvedDiv').style.display ='none';
        }
    })
    solutionDiv.append(notSolutionBtn);
}
 function notSolutionForm () {

    nsform = document.getElementById('notSolvedForm');
    bugId = bugJson.id;
        console.log(bugId );
        reasonText = document.getElementById('notSolvedText').value;
        updateStatus = document.getElementById('updateStatus').value;
        
        alert(reasonText);
        //need some kind of feedback form to show up here, why wasnt solution good? what do you want to do? unclaimed, leave with solver etc
        //needs to pass userid, bugid, reason,(could pass as an update yknow) new status (unclaimed, proceesing, given up)
        fetch(`bugNotSolved/${bugId}`, {
            method: 'POST',
            body: JSON.stringify({ //no need to send any data regarding 'is finished' or anything, can just set 'fixed' to 'true' in views
                reasonText: reasonText,
                updateStatus: updateStatus
            })
        })
        alert('of course you wont post unless theres an alert');
   
   
}