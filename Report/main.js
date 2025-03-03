/*
    Runs all needed functions when the Body's HTML has loaded.
    Does not return anything.
*/
function Initialise() {
    GetWordCounts();
    WordCountSum();
    CreateCollapsibles();
}

function GetWordCounts() {
    let result = 0;

    for (let element of document.getElementsByClassName("createSection")) {
        element.textContent.split("\n").forEach(n => {
            let nClean = n.trim()
            if (nClean == "") return;

            result += nClean.split(" ").length;
        })
    }

    document.getElementById("CreateSectionSum").textContent = result.toString();
}

/*
    Gets all of the word counts from each section
    of the word count table, and sets it as the total value.
    Does not return anything.
*/
function WordCountSum() {
    let Sum = 0;
    const TableItems = document.getElementById("WordCounts").children[0];

    // Start at 1 to skip the header items
    // Skip the sum items
    for (let i = 1; i < TableItems.children.length - 1; i++) {
        let items = TableItems.children[i]
        Sum += parseInt(items.children[1].textContent);
    }

    document.getElementById("WordCountSum").innerHTML = `<b>${Sum.toString()}</b>`;
}

/*
    Gets all elements of the "collapsible" class, and adds Event Listeners to them
    so their content can be toggled on and off.
    Does not return anything.
*/
function CreateCollapsibles() {
    let Colls = document.getElementsByClassName("collapsible");
    
    for (let i = 0; i < Colls.length; i++) {
        Colls[i].addEventListener("click", function() {
            let content = this.nextElementSibling;
            content.style.display = (content.style.display === "block") ? "none" : "block";
        })
    }
}