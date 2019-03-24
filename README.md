# SmartHire
##### A project for TechTogetherBoston2019 ##

### Motivation
As students, we are going to be a part of this selection process, we wanted to make the system fair for everybody.

### What is SmartHire
SmartHire is an automated recruitment platform that uses the power of AI to help hiring managers make fair, unbiased hiring decisions. It screens and analyzes hiring documents to make recommendations about the top candidates to consider from a pool of applicants.

We attempt to make recommendations about the suitable applicants for a job automatically and unbiasedly. To achieve such goal, we develop a web application that can read and extract contents from resumes and job description and then use Word2Vec model to evaluate the "distance" between the candidate's qualifications and the job's requirements. We will then rank and score candidates and recommend the top candidates to recruiters.

### How does it work
We advertise the software by making the webpage informative. They sign up with their organization. They are enabled to use our software once they are authenticated. They would be taken to the interface which currently includes resume screening and would be brought to a screen where they can specify what they are looking for in the candidates and where they can upload the resumes.

### Tools
We developed front-end in HTML, CSS, JavaScript, and Bootstrap. For back-end, we coded primarily in Python. We used IBM's Natural Language Understanding API, Word2Vec model in gensim API, Flask framework and Sqlchemy ORM.

### Struggles....(things we hope to further develop in the future)
Implementing communication between Front-end and Back-end
Implementing data pipeline
Using IBM AIF360 library for making the result less biased
The trouble with GitHub and Wi-Fi

