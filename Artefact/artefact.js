/* Employment Graph Variables */
let EmploymentElement;
let EmploymentSector;
let EmploymentSectorToggle;
let EmploymentMinYear;
let EmploymentMaxYear;

/* Weekly Earnings Graph Variables */
let WeeklyEarningsElement;
let WeeklyEarningsSector;
let WeeklyEarningsSectorToggle;
let WeeklyEarningsMinYear;
let WeeklyEarningsMaxYear;

/* Occupations Graph Variables */
let OccupationsElement;
let OccupationsYear;

/* User Survey Variables */
let SurveyGender;
let SurveyAge;
let SurveySector;
let SurveyCounty;
let SurveyIncome;
let SurveySatisfaction;

/*
    Runs all required functions for the page to run,
    including finding elements and running other initalisers.
    No returns.
*/
async function initialise() {
    EmploymentElement = document.getElementById("EmployementLevels");
    WeeklyEarningsElement = document.getElementById("WeeklyEarnings");
    OccupationsElement = document.getElementById("Occupations");

    /* 
        Dropdowns must be initialised before displays are updated
        so there are no race conditions, and there is data to
        read from elements.
    */
    await initialiseDropdowns();
    await updateEmploymentDisplay();
    await updateWeeklyEarningsDisplay();
    await updateOccupationsDisplay();
    await initialiseConsumerPrices();
    await initialiseUserData();
    await initialiseFormData();
}

async function initialiseDropdowns() {
    EmploymentSector = document.getElementById("EmploymentSector");
    EmploymentSector.addEventListener("change", updateEmploymentDisplay);

    WeeklyEarningsSector = document.getElementById("WeeklyEarningsSector");
    WeeklyEarningsSector.addEventListener("change", updateWeeklyEarningsDisplay);

    EmploymentMinYear = document.getElementById("EmploymentMinYear");
    EmploymentMaxYear = document.getElementById("EmploymentMaxYear");

    WeeklyEarningsMinYear = document.getElementById("WeeklyEarningsMinYear");
    WeeklyEarningsMaxYear = document.getElementById("WeeklyEarningsMaxYear");

    OccupationsYear = document.getElementById("OccupationsYear");

    removeOptions(EmploymentSector);
    removeOptions(WeeklyEarningsSector);
    
    await populateDropdown(WeeklyEarningsSector, "api/data_sectors?key=AvgWeeklyEarnings");
    await populateDropdown(EmploymentSector, "api/data_sectors?key=Employment");
    
    removeOptions(EmploymentMinYear);
    removeOptions(EmploymentMaxYear);
    removeOptions(WeeklyEarningsMinYear);
    removeOptions(WeeklyEarningsMaxYear);
    removeOptions(OccupationsYear);
    
    let years = await fetchData("api/data_years?key=AvgWeeklyEarnings");
    populateYearDropdowns(WeeklyEarningsMinYear, WeeklyEarningsMaxYear, years);

    years = await fetchData("api/data_years?key=Employment");
    populateYearDropdowns(EmploymentMinYear, EmploymentMaxYear, years);

    years = await fetchData("api/data_years?key=EmploymentLevelsAndOccupations");
    await populateDropdown(OccupationsYear, "api/data_years?key=EmploymentLevelsAndOccupations");
    OccupationsYear.value = years[years.length - 1];

    WeeklyEarningsMinYear.addEventListener("change", updateWeeklyEarningsDisplay);
    WeeklyEarningsMaxYear.addEventListener("change", updateWeeklyEarningsDisplay);
    EmploymentMinYear.addEventListener("change", updateEmploymentDisplay);
    EmploymentMaxYear.addEventListener("change", updateEmploymentDisplay);
    OccupationsYear.addEventListener("change", updateOccupationsDisplay);
}

async function fetchData(url) {
    let response = await fetch(url);
    return await response.json();
}

async function populateDropdown(element, url) {
    let data = await fetchData(url);
    data.forEach(item => {
        let option = document.createElement("option");
        option.value = item;
        option.textContent = item;
        element.appendChild(option);
    });
}

/*
    Populates two dropdown elements with year options.

    minYearElement - The dropdown element for the minimum year.
    maxYearElement - The dropdown element for the maximum year.
    years - An array of years to populate the dropdowns with.

    No returns.
*/
function populateYearDropdowns(minYearElement, maxYearElement, years) {
    years.forEach(year => {
        let minYearOption = document.createElement("option");
        let maxYearOption = document.createElement("option");

        minYearOption.value = year;
        minYearOption.textContent = year;
        maxYearOption.value = year;
        maxYearOption.textContent = year;

        minYearElement.appendChild(minYearOption);
        maxYearElement.appendChild(maxYearOption);
    });

    // Set the default selected values for the dropdowns
    minYearElement.value = years[0];
    maxYearElement.value = years[years.length - 1];
}

/*
    Updates the display element by setting its source based on the provided parameters and fetches data if necessary.

    element - The HTML element whose source will be updated.
    sectorElement - The input element containing the sector value.
    minYearElement - The input element containing the minimum year value.
    maxYearElement - The input element containing the maximum year value.
    apiEndpoint - The API endpoint to fetch data from.
    dataKey - The key used to fetch data years.
    No returns.
*/
async function updateDisplay(element, sectorElement, minYearElement, maxYearElement, apiEndpoint, dataKey) {
    let sector = sectorElement.value;
    let minYear = minYearElement.value;
    let maxYear = maxYearElement.value;

    element.src = `api/${apiEndpoint}?sector=${sector}&min=${minYear}&max=${maxYear}`;

    if (minYear > maxYear) {
        let DataYears = await fetchData(`api/data_years?key=${dataKey}`);

        if (maxYear - 1 < DataYears[0]) {
            minYearElement.value = DataYears[0];
        } else {
            minYearElement.value = maxYear - 1;
        }
        updateDisplay(element, sectorElement, minYearElement, maxYearElement, apiEndpoint, dataKey);
    }
}

async function updateEmploymentDisplay() {
    await updateDisplay(EmploymentElement, EmploymentSector, EmploymentMinYear, EmploymentMaxYear, "graph_employment_trend", "Employment");
}

async function updateWeeklyEarningsDisplay() {
    await updateDisplay(WeeklyEarningsElement, WeeklyEarningsSector, WeeklyEarningsMinYear, WeeklyEarningsMaxYear, "graph_weekly_earnings_trend", "AvgWeeklyEarnings");
}

async function updateOccupationsDisplay() {
    OccupationsElement.src = `api/graph_occupations?year=${OccupationsYear.value}`;
}

function removeOptions(element) {
    let i, L = element.options.length - 1;
    for (i = L; i >= 0; i--) {
        element.remove(i);
    }
}

async function initialiseConsumerPrices() {
    document.getElementById("Expenditure").src = `api/graph_consumer_prices`;
}

async function initialiseUserData() {
    document.getElementById("usrGender").src = "/api/user_data_graph?key=Gender";
    document.getElementById("usrAge").src = "/api/user_data_graph?key=Age";
    document.getElementById("usrJobSector").src = "/api/user_data_graph?key=JobSector";
    document.getElementById("usrCounty").src = "/api/user_data_graph?key=County";
    document.getElementById("usrAnnualIncome").src = "/api/user_data_graph?key=AnnualIncome";
}

async function initialiseFormData() {
    SurveyGender = document.getElementById("surveyGender");
    SurveyAge = document.getElementById("surveyAge");
    SurveySector = document.getElementById("surveyJobSector");
    SurveyCounty = document.getElementById("surveyCounty");
    SurveyIncome = document.getElementById("surveyAnnualIncome");
    SurveySatisfaction = document.getElementById("surveySatisfaction");

    document.getElementById("formSubmit").addEventListener("click", formSubmitPressed);

    let userFormOptions = await fetchData("/api/form_options");

    Object.keys(userFormOptions).forEach(formKey => {
        if (formKey == "Age" || formKey == "AnnualIncome") 
            return;

        let ele = document.getElementById(`survey${formKey}`);
        removeOptions(ele);

        userFormOptions[formKey].forEach(option => {
            let surveySelectionOption = document.createElement("option");
            surveySelectionOption.value = option;
            surveySelectionOption.textContent = option;
            ele.append(surveySelectionOption);
        })
    })

    // Setting defaults
    SurveyAge.value = "25";
    SurveyIncome.value = "€45,000";
    SurveyCounty.value = "Dublin";
    SurveySatisfaction.value = "Neutral";
}

async function formSubmitPressed() {
    let submitButton = document.getElementById("formSubmit");
    submitButton.disabled = true;

    let userFormOptions = await fetchData("/api/form_options");

    if (SurveyAge.value == "") { 
        alert("Entered invalid age. Please only use numbers.");
        submitButton.disabled = false;
        return;
    }

    let ageValue = parseInt(SurveyAge.value);

    if (ageValue > 130) {
        alert("Please enter a realistic age.");
        submitButton.disabled = false;
        return;
    }
    else if (ageValue < 18) {
        alert("You must be over 18 to enter this survey.");
        submitButton.disabled = false;
        return;
    }

    let ageRange = "";
    if (ageValue >= 65) {
        ageRange = "65+";
    }
    else {
        for (let i = userFormOptions['Age'].length - 2; i > -1; i--) {
            let valueRange = userFormOptions['Age'][i];
            let valueSplit = valueRange.split("-");
            
            if (ageValue < parseInt(valueSplit[0])) continue; // eg. 17 < 18-25
            if (ageValue > parseInt(valueSplit[1])) continue; // eg. 65 > 18-25

            ageRange = valueRange;
            break;
        }
    }

    if (SurveyIncome.value == "" || isNaN(parseInt(SurveyIncome.value))) { 
        alert("Entered invalid annual salary. Please only use numbers (You can use commas).");
        submitButton.disabled = false;
        return;
    }

    let annualValue = SurveyIncome.value.replace(/\D/g, "");
    SurveyIncome.value = annualValue;

    let annualRange = "";
    if (annualValue >= 120000) {
        annualRange = "120,000+";
    }
    else {
        for (let i = userFormOptions['AnnualIncome'].length - 2; i > -1; i--) {
            let valueRange = userFormOptions['AnnualIncome'][i];
            let valueSplit = valueRange.split("-");
            
            if (annualValue < parseInt(valueSplit[0].replace(",",""))) continue; // eg. 17 < 18-25
            if (annualValue > parseInt(valueSplit[1].replace(",",""))) continue; // eg. 65 > 18-25

            annualRange = valueRange;
            break;
        }
    }

    console.log(`/api/user_form_entry?
        gender=${SurveyGender.value}&
        age=${ageRange}&
        sector=${SurveySector.value}&
        county=${SurveyCounty.value}&
        annualincome=${annualRange}&
        satisfaction=${SurveySatisfaction.value}
    `)

    let user_submit_response = await fetch(`/api/user_form_entry?gender=${SurveyGender.value}&age=${ageRange}&sector=${SurveySector.value}&county=${SurveyCounty.value}&annualincome=${annualRange}&satisfaction=${SurveySatisfaction.value}`);

    if (user_submit_response.status == 200) {
        alert("Thank you for participating!");
        submitButton.textContent = "✔️";
    }
    else {
        alert("There was an issue sending your answers. Please try again.");
        submitButton.disabled = false;
    }
}