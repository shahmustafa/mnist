# MNIST Classification Flask MySQL Docker Kubernetes

## MNIST CLassification FLASK MySQL Docker
    `sudo docker compose up -d --build`
- prerequisites: `Docker version 24.0.7`
- Above docker command make a docker images of Classification Api(mnist-app) and MySQL Server (mysql)
- MNIST Classification will be live on localhost [http://localhost:5000/predict](http://localhost:5000/predict)
- Basic authentication is used 
  - `username: dam`
  - `passowrd: damp`
- Basic html page opens to browse(test images are in [./test_data](./test_data)) and upload the image
![Upload page](https://github.com/shahmustafa/mnist/blob/master/readme_imgs/Screenshot%20from%202023-12-11%2000-19-45.png)
- Click upload to classifiy the image
- Classification result will be displayed
![Result page](https://github.com/shahmustafa/mnist/blob/master/readme_imgs/Screenshot%20from%202023-12-10%2022-45-10.png)
- Requested image and prediction result will be stored in MySQL databse\
`-------id-----------------------image------------------------prediction`\
`--------1----------------(Image binary formate)-----------------7------`\
`--------2----------------(Image binary formate)-----------------3------`\
- MySQL Server credentials to the acces the database from host machine. [/misc.](./misc.)
  - `user: root`
  - `password: root`
  - `host: db`
  - `port: 3200`
  - `database: digit`
  - `table: classification_data`