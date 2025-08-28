
# API da DCTF Web

API da DCTF Web com três endpoints principais, que permitem:
- Emitir o DARF da DCTF Web.
- Gerar o recibo da declaração da DCTF Web.
- Realizar a declaração do MIT, utilizando um arquivo JSON no formato oficial emitido pelo Governo.




## Ferramentas relacionadas

- ![Google Apps Script](https://img.shields.io/badge/Google%20Apps%20Script-4285F4?style=for-the-badge&logo=google&logoColor=white)
- ![HTML](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
- ![CSS](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
- ![Pico.css](https://img.shields.io/badge/Pico.css-22B8CF?style=for-the-badge&logo=css3&logoColor=white)
- ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)


*Nota: parte do Google Apps Script (com HTML, CSS e PICO.CSS) se encontra na própria plataforma.*



## Documentação da API

Demonstração simples de como utilizar os endpoints fornecidos pela API. 
As requisições devem ser feitas para:  
**https://dctf-web-api.onrender.com/**

#### Apenas para validação do funcionamento

```http
  GET /
```
**Exemplo de resposta esperada:**
```json
{
  "mensagem": "API para assistir na DCTFWeb - Rafael Costrov",
}
```


#### Geração do DARF 
```http
  POST /darf
```

| Parâmetro   |Descrição                                   |
| :--------- | :------------------------------------------ |
| `senha`      | A senha para conseguir utilizar a API. |
| `codigo`      | O codigo da empresa para qual está sendo feita a requisição. |
| `empresa`      | A empresa para qual está sendo feita a requisição. |
| `cnpj`      | O CNPJ para qual está sendo feita a requisição. |
| `competencia`      | Competência da declaração no formato `yyyy-MM`. |

**Exemplo de resposta esperada:**
```json
{
  "mensagem": "Guia DCTFWeb gerada com sucesso.",
  "fileId": {
    "id": "1a2b3c4d5e6f7g8h9i"
  }
}
```
 `mensagem`: Confirmação da geração da Guia.\
 `fileId.id`: ID do PDF da Guia no Google Drive.

#### Geração do DARF em Andamento
```http
  POST /darf-andamento
```

| Parâmetro   |Descrição                                   |
| :--------- | :------------------------------------------ |
| `senha`      | A senha para conseguir utilizar a API. |
| `codigo`      | O codigo da empresa para qual está sendo feita a requisição. |
| `empresa`      | A empresa para qual está sendo feita a requisição. |
| `cnpj`      | O CNPJ para qual está sendo feita a requisição. |
| `competencia`      | Competência da declaração no formato `yyyy-MM`. |

**Exemplo de resposta esperada:**
```json
{
  "mensagem": "Guia DCTFWeb em andamento gerada com sucesso.",
  "fileId": {
    "id": "1a2b3c4d5e6f7g8h9i"
  }
}
```
 `mensagem`: Confirmação da geração da Guia.\
 `fileId.id`: ID do PDF da Guia no Google Drive.

 #### Geração do Recibo 
```http
  POST /recibo
```

| Parâmetro   |Descrição                                   |
| :--------- | :------------------------------------------ |
| `senha`      | A senha para conseguir utilizar a API. |
| `codigo`      | O codigo da empresa para qual está sendo feita a requisição. |
| `empresa`      | A empresa para qual está sendo feita a requisição. |
| `cnpj`      | O CNPJ para qual está sendo feita a requisição. |
| `competencia`      | Competência da declaração no formato `yyyy-MM`. |

**Exemplo de resposta esperada:**
```json
{
  "mensagem": "Recibo DCTFWeb gerado com sucesso.",
  "fileId": {
    "id": "1a2b3c4d5e6f7g8h9i"
  }
}
```
- `mensagem`: Confirmação da geração do recibo.
- `fileId.id`: ID do PDF do recibo no Google Drive.

#### Declaração do MIT 
```http
  POST /mit
```

| Parâmetro   |Descrição                                   |
| :--------- | :------------------------------------------ |
| `senha`      | A senha para conseguir utilizar a API. |
| `empresa`      | A empresa para qual está sendo feita a requisição. |
| `cnpj`      | O CNPJ para qual está sendo feita a requisição. |
| `id`      | ID do arquivo JSON salvo no Google Drive. |

**Exemplo de resposta esperada:**
```json
{
  "mensagem": "MIT gerado com sucesso.",
  "arquivo": "1a2b3c4d5e6f7g8h9i"
}
```
- `mensagem`: Confirmação da entrega do MIT.
- `arquivo`: ID do JSON usado na declaração no Google Drive.






## Autor

- [@RafaelCostrov](https://github.com/RafaelCostrov)
