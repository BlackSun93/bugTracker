document.addEventListener('DOMContentLoaded', function() {
    //may shift logic about which html divs to show to js side
    //divs to show/hide:
    //finishedDiv, solverButtonDiv, solutionDiv (with notSolvedForm), updateForm
    
    bugElement = document.getElementById('bugObjectDiv');
    bugInfo = bugElement.dataset.bug;
    currentUser = bugElement.dataset.user;
    solver = bugElement.dataset.solver;
    console.log(bugJson);
    console.log(bugInfo);
    console.log(currentUser + "  " + solver);
    console.log(bugJson.poster);
    document.getElementById('updateForm').style.display = 'none';
    //document.getElementById('updateForm').style.display = 'block';
    visibilityChecks();

    /*var updateStyle = document.querySelectorAll('updateClass');

    for (var i = 0; i < updateStyle.length; i++) {
        update = updateStyle[i];
        update.style.border = "solid"
    } */
  
    /*
    if (currentUser == solver) {
        document.getElementById('updateForm').style.display = 'block';
    }
    else {
        document.getElementById('updateForm').style.display = 'none';
    }
    if (bugJson.status == 'unclaimed') {
        document.getElementById('solverButtonDiv').style.display = 'block';
    }
    else {
        document.getElementById('solverButtonDiv').style.display = 'none';
    }
    if ((bugJson.status == 'solved') && (bugJson.poster == currentUser) ) {
       document.getElementById('solutionDiv').style.display == 'block';
    } */
    
    try {
        document.getElementById('notSolvedDiv').style.display = 'none';
    }
    catch {
        console.log('unsolved div is not here'); //stops the error if the update form isn't going to be generated
    }
    
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
    try {
        document.getElementById('notSolvedForm').onsubmit = notSolutionForm;
    }
    catch {
        console.log("notSolvedForm isn't displayed");
    }
    

    
});
function visibilityChecks() {
    document.getElementById('updateForm').style.display = 'none';
    if(currentUser == solver) {
       
        document.getElementById('updateForm').style.display = 'block';
    }
    if (bugJson.status == 'unclaimed') { //this causes an issue if for some reason bug is processing wih no solver
        
        solverButton(currentUser);
    }
    else {
       
        document.getElementById('solveThisBugBtn') == 'none';
    }
    if ((bugJson.status == 'solved') && (bugJson.poster == currentUser) ) {
        
        document.getElementById('ifNotFixedDiv').style.display = 'block';
        document.getElementById('updateForm').style.display = 'none';
    }
    else {
        document.getElementById('ifNotFixedDiv').style.display = 'none';
    }
   
}
function hello() {
    alert('hello');
}

function solverButton(userId){ //should standardise whether or not to make elements in JS or in html really
    buttonDiv = document.getElementById('solverButtonDiv');
    button = document.createElement('button');
    button.setAttribute('id', 'solveThisBugBtn');
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
        document.getElementById('statusDivText').innerHTML = 'claimed';
        document.getElementById('solverButtonDiv').style.display= 'none';
        document.getElementById('updateDiv').style.display = 'block'; 
        document.getElementById('updateForm').style.display = 'block';
    })
    buttonDiv.append(button);
}

function createUpdate() {
    alert("A");
    newUpdate = document.getElementById('updateText').value;
    newStatus = document.getElementById('updateStatus').value;
    bugId = bugJson.id;
    alert(newUpdate);
    alert(newStatus);
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
        
        document.getElementById('ifNotFixedDiv').style.display = 'none';
        document.getElementById('updateForm').style.display = 'none';
        document.getElementById('statusDivText').innerHTML = `fixed by ${bugJson.solver}`;
        
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