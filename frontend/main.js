let jobsUrl = "http://127.0.0.1:8000/api/";

let getJobs = () => {
    fetch(jobsUrl)
        .then(response => response.json())
        .then(data => {
            console.log(data)
            buildJobs(data);
        })
}

let buildJobs = (jobs) => {
    let jobsWrapper = document.getElementById("jobs-wrapper");
    jobsWrapper.innerHTML = "";

    for (let i in jobs["JOBS"]) {
        let job = jobs["JOBS"][i];

        let jobCard = `
                <div class="card mb-5">
                    <div class="card-body">
                        <a href="http://127.0.0.1:8000/job/${job.id}" target="_blank">
                            <h4 class="card-title">${job.title}</h4>
                        <a/>
                        <p class="card-text">ЗАРПЛАТА: от ${job.salary_from} тыс. руб. до ${job.salary_to} тыс. руб.</p>
                        <p class="card-text">ОПЫТ РАБОТЫ: ${job.experience}</p>
                        <p class="card-text">РАБОТОДАТЕЛЬ: ${job.employer}</p>
                        <p class="card-text">ГОРОД: ${job.city}</p>
                        <p class="card-text">АДРЕС: ${job.address}</p>
                        <p class="card-text">РЕЖИМЫ РАБОТЫ:
        `;

        for (let j in job.employment_modes) {
            jobCard += `
                        ${job.employment_modes[j].employment_mode},
            `;
        }

        jobCard += `
                        </p>
                        <p class="card-text">НАВЫКИ: 
        `;

        for (let k in job.skills) {
            jobCard += `
                        ${job.skills[k].skill},
            `;
        }

        jobCard += `
                        </p>
                    </div>
                </div>
            `;

        jobsWrapper.innerHTML += jobCard;
    }
}


getJobs();