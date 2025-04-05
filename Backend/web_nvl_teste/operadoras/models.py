from django.db import models

class Operadora(models.Model):
    registro_ans = models.CharField(max_length=20, db_column='Registro_ANS', primary_key=True)
    cnpj = models.CharField(max_length=20, db_column='CNPJ')
    razao_social = models.CharField(max_length=255, db_column='Razao_Social')
    nome_fantasia = models.CharField(max_length=255, db_column='Nome_Fantasia')
    modalidade = models.CharField(max_length=100, db_column='Modalidade', null=True, blank=True)
    logradouro = models.CharField(max_length=255, db_column='Logradouro', null=True, blank=True)
    numero = models.CharField(max_length=10, db_column='Numero', null=True, blank=True)
    complemento = models.CharField(max_length=255, db_column='Complemento', null=True, blank=True)
    bairro = models.CharField(max_length=100, db_column='Bairro', null=True, blank=True)
    cidade = models.CharField(max_length=100, db_column='Cidade', null=True, blank=True)
    uf = models.CharField(max_length=2, db_column='UF', null=True, blank=True)
    cep = models.CharField(max_length=10, db_column='CEP', null=True, blank=True)
    ddd = models.CharField(max_length=3, db_column='DDD', null=True, blank=True)
    telefone = models.CharField(max_length=20, db_column='Telefone', null=True, blank=True)
    fax = models.CharField(max_length=20, db_column='Fax', null=True, blank=True)
    endereco_eletronico = models.EmailField(db_column='Endereco_eletronico', null=True, blank=True)
    representante = models.CharField(max_length=255, db_column='Representante', null=True, blank=True)
    cargo_representante = models.CharField(max_length=100, db_column='Cargo_Representante', null=True, blank=True)
    regiao_comercializacao = models.CharField(max_length=255, db_column='Regiao_de_Comercializacao', null=True, blank=True)
    data_registro_ans = models.DateField(db_column='Data_Registro_ANS', null=True, blank=True)


    class Meta:
        managed = False  
        db_table = 'operadoras_ativas'  
        




