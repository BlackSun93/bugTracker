document.addEventListener('DOMContentLoaded', function () {
//current solved, posted?, solving

document.querySelector('#current').addEventListener('click', () => showCurrent());
document.querySelector('#awaiting').addEventListener('click', () => showAwaiting());
document.querySelector('#solved').addEventListener('click', () => showSolved());
document.querySelector('#posted').addEventListener('click', showPosted);
document.getElementById ('bugsCurrentlySolving').style.display = 'none';
document.getElementById ('bugsUserPostedDiv').style.display = 'none';
document.getElementById ('bugsUserSolvedDiv').style.display = 'none';
document.getElementById ('awaitingBugsDiv').style.display = 'none';

})

function showAwaiting() {
    
    document.getElementById ('bugsCurrentlySolving').style.display = 'none';
    document.getElementById ('bugsUserPostedDiv').style.display = 'none';
    document.getElementById ('bugsUserSolvedDiv').style.display = 'none';
    document.getElementById ('awaitingBugsDiv').style.display = 'block';
}
function showCurrent() {
    document.getElementById ('bugsCurrentlySolving').style.display = 'block';
document.getElementById ('bugsUserPostedDiv').style.display = 'none';
document.getElementById ('bugsUserSolvedDiv').style.display = 'none';
document.getElementById ('awaitingBugsDiv').style.display = 'none';
}
function showSolved() {
    document.getElementById ('bugsCurrentlySolving').style.display = 'none';
document.getElementById ('bugsUserPostedDiv').style.display = 'none';
document.getElementById ('bugsUserSolvedDiv').style.display = 'block';
document.getElementById ('awaitingBugsDiv').style.display = 'none';
}
function showPosted() {
    document.getElementById ('bugsCurrentlySolving').style.display = 'none';
document.getElementById ('bugsUserPostedDiv').style.display = 'block';
document.getElementById ('bugsUserSolvedDiv').style.display = 'none';
document.getElementById ('awaitingBugsDiv').style.display = 'none';
}