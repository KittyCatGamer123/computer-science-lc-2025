/*
    Runs all needed functions when the Body's HTML has loaded.
    Does not return anything.
*/
function Initialise() {
    WordCountSum();
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