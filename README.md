# SmartHire
##### A project for TechTogetherBoston2019 ##

### Motivation
Women and people of color are more likely to see discrimination in the hiring process. There is a lack of diversity in the senior leadership of many companies. AI systems used to automate recruiting can also contain AI bias if the system is trained on bad data that contains implicit biases and excludes certain groups of people, making the AI's decisions untrustworthy. As such, we wanted to make an automated system that is unbiased and fair for everybody.

### What is SmartHire
SmartHire is an automated recruitment platform that uses the power of AI to help hiring managers make fair, unbiased hiring decisions. It screens and analyzes hiring documents (resumes, cover letters etc.) to make recommendations about the top candidates to consider from a pool of applicants, thus saving hiring managers' time and resources.

Our goal is to make recommendations about the suitable applicants for a job automatically and unbiasedly. To achieve this, we developed a web application that can read and extract content from resumes/cover letters and job descriptions and then use the Word2Vec open-source model to evaluate the "distance" between the candidate's qualifications and the job's requirements. The system then scores and ranks candidates to recommend the top candidates to recruiters.

### How does it work
We advertised the software by making an informative webpage where recruiters can create an account with their organization. They are able to use our software once they are authenticated. They would be taken to the interface which currently includes resume screening and would be brought to a screen where they can specify what they are looking for in job candidates and where they can upload the resumes they receive for the opening.

### How to evaluate resumes
We used three measures using the IBM Cloud platform:</br>
- how close the keywords used in the resume are to the words used in the job description</br>
- how close categorically close the resume and the job description are (i.e. taking into account the context of written work)</br>
- how close the concepts in the resume are to the concepts in the job description (i.e. taking into account underlying ideas in the writing)</br>

1 and 3 return binary values and 2 returns numerical(0 to 1). We scaled those numbers and took the average of them. We assumed the final number we got was a biased value. This is because individuals' resume writing skills can be affected by their economic/educational/racial background. Hence, we decided to remove this bias that is outside one's control. As we already had biased numbers, we tried to implement a post-processing method using IBM's AIF360 library. The issue we faced here was we did not have truly right results after removing bias that were necessary for implementing this method. Hence, we used another solution. When the ratio of the privileged group was significantly different in the whole candidate group and in the top candidate group, we considered the candidates who were slightly outside the threshold of the top candidate and in the less privileged group as a part of the top candidate pool. Then we remeasured the percentage of the ratio of the privileged group in both groups, and if the number got improved (the difference in those two groups got smaller), we could show that we somewhat improved the bias.</br>

### Tools
We developed front-end in HTML, CSS, JavaScript, and Bootstrap. For back-end, we coded primarily in Python. We used IBM's Natural Language Understanding APIs, Word2Vec model in gensim API, Flask framework and Sqlchemy ORM.

### Struggles....(things we hope to further develop in the future)
Implementing better communication between Front-end and Back-end
Implementing data pipeline
Using IBM AIF360 library for making the result less biased
Initial struggles with GitHub and Wi-Fi

