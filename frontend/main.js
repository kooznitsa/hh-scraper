let jobsUrl = "http://127.0.0.1:8000/api";

let getJobs = () => {
    fetch(jobsUrl, {
            method: "GET",
            headers: {
                "X-Requested-With": "XMLHttpRequest",
            }
        })
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
                        <p class="card-text"><strong>ЗАРПЛАТА:</strong> от ${job.salary_from} тыс. руб. до ${job.salary_to} тыс. руб.</p>
                        <p class="card-text"><strong>ОПЫТ РАБОТЫ:</strong> ${job.experience}</p>
                        <p class="card-text"><strong>РАБОТОДАТЕЛЬ:</strong> ${job.employer}</p>
                        <p class="card-text"><strong>ГОРОД:</strong> ${job.city}</p>
                        <p class="card-text"><strong>АДРЕС:</strong> ${job.address}</p>
                        <p class="card-text"><strong>РЕЖИМЫ РАБОТЫ:</strong>
        `;

        for (let j in job.employment_modes) {
            jobCard += `
                        ${job.employment_modes[j].employment_mode},
            `;
        }

        jobCard += `
                        </p>
                        <p class="card-text"><strong>НАВЫКИ:</strong> 
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