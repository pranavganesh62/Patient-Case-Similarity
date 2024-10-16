# Patient-Case-Similarity
We intend to develop a web application for Clinicians and Researchers. There is a central database which contains EHR and on
this EHR, we are applying Machine Learning algorithms to train our model. Patients are clustered based on their medical
conditions. The accuracy of the similarity scores will be checked using RMSE. We are providing two interfaces i.e., one for
Researchers and another for Doctors. A new user needs to register themselves based on their designation and after successful
registrations, he/she has to login. Researchers interface will have options like querying the database from which patient
similarity score matrix between any two sets of individuals will be generated based on trained model. This can be used for
his/her medical research such as patients who have received similar treatments or examine their medical records for exposure
and outcomes. Also, he/she can conduct case-control studies which is a retrospective study in which a group of individuals
that are disease positive is compared with a group of disease negative individuals. Further the application can assist them in
conducting clinical trails. Doctors interface will have functionality to query the database based on new patient’s
symptoms/parameters, first we will classify to which cluster the new patient belongs to and then give similarity scores with
other patients. From this, a doctor can do an observational study based on demographics (age, location, etc.) and history of
most similar case patient. This can assist the doctor in diagnosis and recommend treatment to patient.
