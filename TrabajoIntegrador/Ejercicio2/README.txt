Codigos importantes:

Crear la imagen del docker (incluido el punto): 
docker build -t ciberseguridad-tools .

Correr el contenedor:docker run -it --rm -v ${PWD}/webapp:/app/webapp ciberseguridad-tools
