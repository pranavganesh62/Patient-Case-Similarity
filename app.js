
function submitForm(event) {
    event.preventDefault();
    console.log("called here")
    let name = document.forms["registrationForm"]["name"].value;
    let id = document.forms["registrationForm"]["id"].value;
    let phone = document.forms["registrationForm"]["phone"].value;
    let age = document.forms["registrationForm"]["age"].value;
    let sex = document.forms["registrationForm"]["sex"].value;
    let cigsPerDay = document.forms["registrationForm"]["cigsPerDay"].value;
    let BPMeds = document.forms["registrationForm"]["BPMeds"].value;
    let prevalentStroke = document.forms["registrationForm"]["prevalentStroke"].value;
    let prevalentHyp = document.forms["registrationForm"]["prevalentHyp"].value;
    let diabetes = document.forms["registrationForm"]["diabetes"].value;
    let totChol = document.forms["registrationForm"]["totChol"].value;
    let sysBP = document.forms["registrationForm"]["sysBP"].value;
    let diaBP = document.forms["registrationForm"]["diaBP"].value;
    let BMI = document.forms["registrationForm"]["BMI"].value;
    let heartRate = document.forms["registrationForm"]["heartRate"].value;
    let glucose = document.forms["registrationForm"]["glucose"].value;


    if (name == "" || id == "" || phone == "" || age == "" || sex == "" ||
        cigsPerDay == "" || BPMeds == "" || prevalentStroke == "" ||
        prevalentHyp == "" || diabetes == "" || totChol == "" ||
        sysBP == "" || diaBP == "" || BMI == "" || heartRate == "" || glucose == "") {
        alert("All fields must be filled out.");
        return false;
    }

    if (isNaN(id) || isNaN(phone) || isNaN(age)) {
        alert("Patient ID, Phone, and Age must be numbers.");
        return false;
    }

    let patientData = {
        name: name,
        id: id,
        phone: phone,
        age: age,
        sex: sex,
        cigsPerDay: cigsPerDay,
        BPMeds: BPMeds,
        prevalentStroke: prevalentStroke,
        prevalentHyp: prevalentHyp,
        diabetes: diabetes,
        totChol: totChol,
        sysBP: sysBP,
        diaBP: diaBP,
        BMI: BMI,
        heartRate: heartRate,
        glucose: glucose
    };

    fetch('http://127.0.0.1:5000/predict', {
        method: 'POST',
        mode:'cors',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(patientData)
    })
    .then(response => response.json())
    .then(data => {
        let resultDiv = document.createElement('div');
        resultDiv.style.padding = "20px";
        resultDiv.style.backgroundColor = "#444";
        resultDiv.style.marginTop = "20px";
        resultDiv.style.color = "white";
        resultDiv.innerHTML = "<h3>Most Similar Patients:</h3>";

        let similarPatients = data;
        for (let patientId in similarPatients) {
            resultDiv.innerHTML += `<p>Patient ID: ${patientId}, Similarity: ${similarPatients[patientId]}</p>`;
        }
        document.body.appendChild(resultDiv);
    })
    .catch(error => {
        console.error("Error:", error);
        alert("Error ");
    });
}

document.addEventListener('DOMContentLoaded', () => {
});
