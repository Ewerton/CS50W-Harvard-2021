# Anotações

unittest é uma library pra testes unitários
Permite escrever teste  para automatizar test runners.

No Django vc pode:
- Criar um arquivo chamado, tests.py, por exemplo
- Criar uma classe que herda de TestCase e implementa uma função setUp para ela
- Cria seus testes
- Vc inicializa os testes chamando python "manage.py test"

## Testando a interação com o browser
Tem que instalar o webdriver do browser que vc quer usar e configrar, por exemplo:
driver = webdriver.Edge('D:/Webdrivers/msedgedriver.exe')
#river = webdriver.Chrome('D:/Webdrivers/chromedriver.exe')


## Continuous Integration (docker and compose)
- Crie um dockefile para sua aplicação
- crie um docker-compose para aplicação e banco de dados
- docker-compose up para rodar o compose (ou então "docker compose up")

Se quiser "interagir" com o container:
- docker ps para pegar o ID do container
- docker exec -it <id do container> <comando que quer rodar>  (-ite quer dizer interactivo)
    - Exemplo docker exec -it d6djr67 bash -l # a partir dadqui vc dá comandos dentro do container
    - Desta forma vc pode executar o python manage.py createsuperuser dentro do container
- para recriar a stack (docker-compose up --build --force-recreate --no-deps)

# Docker
Pra criar um container a partir de um dockerfile
docker build -f [docker_file_name] . (don't miss the dot at the end)
if the name of your file is "dockerfile" (lower case) then you don't need the -f and the filename




