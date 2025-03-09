let WeeklyEarningsElement;
let WeeklyEarningsSector;
let WeeklyEarningsMinYear;
let WeeklyEarningsMaxYear;

async function initialise() {
    WeeklyEarningsElement = document.getElementById("WeeklyEarnings");

    await initialiseWeeklyEarningsDropdowns();
    updateWeeklyEarningsDisplay();
}

async function initialiseWeeklyEarningsDropdowns() {
    WeeklyEarningsSector = document.getElementById("WeeklyEarningsSector");
    WeeklyEarningsSector.addEventListener("change", updateWeeklyEarningsDisplay);

    WeeklyEarningsMinYear = document.getElementById("WeeklyEarningsMinYear");
    WeeklyEarningsMaxYear = document.getElementById("WeeklyEarningsMaxYear");

    removeOptions(WeeklyEarningsSector);
    let Sectors = await (await fetch("api/data_sectors?key=AvgWeeklyEarnings")).json(); 
    Sectors.forEach(sector => {
        let sectorOption = document.createElement("option");
        sectorOption.value = sector;
        sectorOption.textContent = sector;
        WeeklyEarningsSector.appendChild(sectorOption);
    })

    removeOptions(WeeklyEarningsMinYear);
    removeOptions(WeeklyEarningsMaxYear);

    let Years = await (await fetch("api/data_years?key=AvgWeeklyEarnings")).json();
    Years.forEach(year => {
        let minYearOption = document.createElement("option");
        let maxYearOption = document.createElement("option");

        minYearOption.value = year;
        minYearOption.textContent = year;
        maxYearOption.value = year;
        maxYearOption.textContent = year;

        WeeklyEarningsMinYear.appendChild(minYearOption);
        WeeklyEarningsMaxYear.appendChild(maxYearOption);
    });

    WeeklyEarningsMinYear.value = Years[0];
    WeeklyEarningsMaxYear.value = Years[Years.length - 1];

    WeeklyEarningsMinYear.addEventListener("change", updateWeeklyEarningsDisplay);
    WeeklyEarningsMaxYear.addEventListener("change", updateWeeklyEarningsDisplay);
}

async function updateWeeklyEarningsDisplay() {
    let sector = WeeklyEarningsSector.value;
    let minYear = WeeklyEarningsMinYear.value;
    let maxYear = WeeklyEarningsMaxYear.value;

    WeeklyEarningsElement.src = `api/graph_weekly_earnings_trend?sector=${sector}&min=${minYear}&max=${maxYear}`;

    if (minYear > maxYear) {
        let DataYears = await (await fetch("api/data_years?key=AvgWeeklyEarnings")).json();
        
        if (maxYear - 1 < DataYears[0]) {
            WeeklyEarningsMinYear.value = DataYears[0];    
        }
        else {
            WeeklyEarningsMinYear.value = maxYear - 1;
        }
        updateWeeklyEarningsDisplay();
    }
}

function removeOptions(element) {
    let i, L = element.options.length - 1;
    for (i = L; i >= 0; i--) {
        element.remove(i);
    }
}