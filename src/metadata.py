from coleta import coleta_pb2 as Coleta

# A extensão das planilhas de contracheques é XLS até maio de 2019
# Após isso, a extensão adotada foi a ODS.

# A publicação dos relatórios de Verbas Indenizatórias e outras Remunerações Temporárias
# foi iniciada no mês de julho de 2019, em função do início da vigência da Resolução CNMP Nº 200

# As planilhas de contracheque até junho de 2019 não possuem matrícula.

# As planilhas de indenizacoes seguem um formato de dados diferente a partir de setembro de 2021.

# A planilha de indenizações de 07/2020 também possui um formato diferente, similar ao adotado em 2021. 

def get(month, year):
    if year < 2019 or (year == 2019 and month < 7):
        metadata = Coleta.Metadados()
        metadata.acesso = Coleta.Metadados.FormaDeAcesso.ACESSO_DIRETO
        if year == 2019 and month == 6:
            metadata.extensao = Coleta.Metadados.Extensao.ODS
        else:
            metadata.extensao = Coleta.Metadados.Extensao.XLS
        metadata.estritamente_tabular = True
        metadata.tem_matricula = False
        metadata.tem_lotacao = True
        metadata.tem_cargo = True
        metadata.receita_base = Coleta.Metadados.OpcoesDetalhamento.DETALHADO
        metadata.despesas = Coleta.Metadados.OpcoesDetalhamento.DETALHADO
        metadata.outras_receitas = Coleta.Metadados.OpcoesDetalhamento.AUSENCIA
        if year == 2019 and (month == 6 or month == 7):
            metadata.formato_consistente = False
        else:
            metadata.formato_consistente = True
    else:
        metadata = Coleta.Metadados()
        metadata.nao_requer_login = True
        metadata.nao_requer_captcha = True
        metadata.acesso = Coleta.Metadados.FormaDeAcesso.ACESSO_DIRETO
        metadata.extensao = Coleta.Metadados.Extensao.ODS
        metadata.estritamente_tabular = False
        metadata.tem_matricula = True
        metadata.tem_lotacao = True
        metadata.tem_cargo = True
        metadata.receita_base = Coleta.Metadados.OpcoesDetalhamento.DETALHADO
        metadata.despesas = Coleta.Metadados.OpcoesDetalhamento.DETALHADO
        metadata.outras_receitas = Coleta.Metadados.OpcoesDetalhamento.DETALHADO
        if (year == 2021 and month == 9) or (year == 2023 and month == 2) or (int(year) == 2020 and int(month) == 7) or (year == 2024 and month == 1):
            metadata.formato_consistente = False
        else:
            metadata.formato_consistente = True
    return metadata
