# Como rodar

## 1. Crie 2 arquivos .env em `./`: dev.env e prod.env;
O arquivo deve ser formatado da seguinte maneira:
TOKEN=`Token do seu Bot`

## 2. Crie 2 arquivos .json em `./database`: DataBaseConfig-dev.json e DataBaseConfig.json;
O arquivo deve possuir as configurações de um banco de dados FireBase. Obtenha elas no site da FireBase.
O arquivo deve ser organizado conforme o arquivo `./database/DataBaseConfig-example.json`

## 3. Crie 2 arquivos .json em `./app`: config-dev.json e config.json;
O arquivo deve ser formatado conforme o arquivo `./app/config-example.json` já presente em `./app`.
`PDFFormNames` deve conter uma lista com o nome dos campos da ficha. A ordem deve ser exatamente a mesma (os indices não podem mudar).

_NOTAS: Você precisa apenas criar os arquivos de desenvolvimento caso não queira usar o aplicativo em produção. Para todo caso, você deve mudar a forma de utilização do aplicativo em `./app/utilities/configreader.py`. Caso queira rodar em desenvolvimento, coloque devMode como True; caso contrário, como False._

## 4. Adicione um arquivo `.zip` contendo o aplicativo no [SquareCloud](https://squarecloud.app/dashboard)