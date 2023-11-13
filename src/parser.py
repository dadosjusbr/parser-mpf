import re
import number

from coleta import coleta_pb2 as Coleta

from headers_keys import (HEADERS, INDENIZACOES_ANTES, OBRIGATORIOS_ANTES, REMTEMP_ANTES, REMUNERACAOBASICA,
                          EVENTUALTEMP, OBRIGATORIOS)


def parse_employees_after(file_name, colect_key, month, year):
    employees = {}
    counter = 1
    for row in file_name:
        if str(row[0]) == "TOTAL GERAL":
            break
        if not number.is_nan(row[0]) and str(row[0]) != "Matrícula":
            # As planilhas do MPF possui células vazias (NaN) entre os dados,
            # aqui removemos essas células e deixamos apenas as informações dos membros
            new_row = [x for x in row if not number.is_nan(x)]
            member = Coleta.ContraCheque()
            member.id_contra_cheque = colect_key + "/" + str(counter)
            member.chave_coleta = colect_key
            member.matricula = str(new_row[0])
            member.nome = new_row[1]
            member.funcao = new_row[2]
            member.local_trabalho = new_row[3]
            member.tipo = Coleta.ContraCheque.Tipo.Value("MEMBRO")
            member.ativo = True
            member.remuneracoes.CopyFrom(
                create_remuneration(new_row, month, year)
            )

            employees[str(new_row[0])] = member
            counter += 1

    return employees


def parse_employees_before(file_name, colect_key, month, year):
    employees = {}
    counter = 1
    for row in file_name:
        if str(row[0]) == "TOTAL GERAL":
            break
        if not number.is_nan(row[0]) and str(row[0]) != "Nome ou Matrícula":
            new_row = [x for x in row if not number.is_nan(x)]
            member = Coleta.ContraCheque()
            member.id_contra_cheque = colect_key + "/" + str(counter)
            member.chave_coleta = colect_key
            member.nome = new_row[0]
            member.funcao = new_row[1]
            member.local_trabalho = new_row[3]
            member.tipo = Coleta.ContraCheque.Tipo.Value("MEMBRO")
            member.ativo = True
            member.remuneracoes.CopyFrom(
                create_remuneration(new_row, month, year)
            )

            employees[str(new_row[0])] = member
            counter += 1

    return employees


def remunerations_after(file_indenizatorias):
    dict_remuneracoes = {}
    for row in file_indenizatorias:
        if 'Data' in str(row):
            break
        if not number.is_nan(row[0]) and str(row[0]) != "Matrícula":
            # As planilhas do MPF possui células vazias (NaN) entre os dados,
            # aqui removemos essas células e deixamos apenas as informações dos membros
            new_row = [x for x in row if not number.is_nan(x)]
            mat = str(new_row[0])
            remuneracoes = dict_remuneracoes.get(mat, Coleta.Remuneracoes())
            # Verbas indenizatórias
            # O MPF não possui formato estritamente tabular, sendo necessário apagarmos células vazias, deixando apenas os dados (new_row[8]).
            # Quando o membro não possui verba indenizatória, 2 campos ficam vazios. Assim, new_row possui 6 campos.
            # Quando o membro não possui outras remunerações temporárias, o órgão adiciona um campo "N/C" e o outro é vazio.
            # Assim, new_row possui 7 campos.
            # Quando o membro possui as duas verbas, new_row contém a descrição e valor de ambos, ficando com 8 campos
            if new_row[4] != "N/C" and len(new_row) in [8, 7]:
                rem = Coleta.Remuneracao()
                rem.natureza = Coleta.Remuneracao.Natureza.Value("R")
                rem.categoria = "Verbas indenizatórias"
                rem.item = str(new_row[4])
                rem.valor = float(number.format_value(str(new_row[5]).replace('R$','')))
                rem.tipo_receita = Coleta.Remuneracao.TipoReceita.Value("O")
                remuneracoes.remuneracao.append(rem)
            # Outras remunerações temporárias
            if new_row[len(new_row)-2] != "N/C" and len(new_row) in [8, 6]:
                rem = Coleta.Remuneracao()
                rem.natureza = Coleta.Remuneracao.Natureza.Value("R")
                rem.categoria = "Outras remunerações temporárias"
                rem.item = str(new_row[len(new_row)-2])
                rem.valor = float(number.format_value(str(new_row[len(new_row)-1]).replace('R$','')))
                rem.tipo_receita = Coleta.Remuneracao.TipoReceita.Value("O")
                remuneracoes.remuneracao.append(rem)
            dict_remuneracoes[mat] = remuneracoes
    return dict_remuneracoes


def remunerations_before(row):
    remuneration_array = Coleta.Remuneracoes()
    # VERBAS INDENIZATÓRIAS
    for key, value in HEADERS[INDENIZACOES_ANTES].items():
        remuneration = Coleta.Remuneracao()
        remuneration.natureza = Coleta.Remuneracao.Natureza.Value("R")
        remuneration.categoria = INDENIZACOES_ANTES
        remuneration.item = key
        remuneration.valor = float(number.format_value(row[value]))
        remuneration.tipo_receita = Coleta.Remuneracao.TipoReceita.Value("O")
        remuneration_array.remuneracao.append(remuneration)
    # OUTRAS REMUNERAÇÕES TEMPORÁRIAS
    for key, value in HEADERS[REMTEMP_ANTES].items():
        remuneration = Coleta.Remuneracao()
        remuneration.natureza = Coleta.Remuneracao.Natureza.Value("R")
        remuneration.categoria = REMTEMP_ANTES
        remuneration.item = key
        remuneration.valor = float(number.format_value(row[value]))
        remuneration.tipo_receita = Coleta.Remuneracao.TipoReceita.Value("O")
        remuneration_array.remuneracao.append(remuneration)
    return remuneration_array


def create_remuneration(row, month, year):
    remuneration_array = Coleta.Remuneracoes()
    # REMUNERAÇÃO BÁSICA
    for key, value in HEADERS[REMUNERACAOBASICA].items():
        remuneration = Coleta.Remuneracao()
        remuneration.natureza = Coleta.Remuneracao.Natureza.Value("R")
        remuneration.categoria = REMUNERACAOBASICA
        remuneration.item = key
        remuneration.valor = float(number.format_value(row[value]))
        remuneration.tipo_receita = Coleta.Remuneracao.TipoReceita.Value("B")
        remuneration_array.remuneracao.append(remuneration)
    # REMUNERAÇÃO EVENTUAL OU TEMPORÁRIA
    for key, value in HEADERS[EVENTUALTEMP].items():
        remuneration = Coleta.Remuneracao()
        remuneration.natureza = Coleta.Remuneracao.Natureza.Value("R")
        remuneration.categoria = EVENTUALTEMP
        remuneration.item = key
        remuneration.valor = float(number.format_value(row[value]))
        remuneration.tipo_receita = Coleta.Remuneracao.TipoReceita.Value("B")
        remuneration_array.remuneracao.append(remuneration)
    # OBRIGATÓRIOS/LEGAIS
    if int(year) > 2019 or (int(year) == 2019 and int(month) >= 7):
        for key, value in HEADERS[OBRIGATORIOS].items():
            remuneration = Coleta.Remuneracao()
            remuneration.natureza = Coleta.Remuneracao.Natureza.Value("D")
            remuneration.categoria = OBRIGATORIOS
            remuneration.item = key
            remuneration.valor = abs(
                float(number.format_value(row[value]))) * (-1)
            remuneration_array.remuneracao.append(remuneration)
    else:
        for key, value in HEADERS[OBRIGATORIOS_ANTES].items():
            remuneration = Coleta.Remuneracao()
            remuneration.natureza = Coleta.Remuneracao.Natureza.Value("D")
            remuneration.categoria = OBRIGATORIOS
            remuneration.item = key
            remuneration.valor = abs(
                float(number.format_value(row[value]))) * (-1)
            remuneration_array.remuneracao.append(remuneration)
    return remuneration_array


def update_employees_after(file_indenizacoes, employees):
    remuneracoes = remunerations_after(file_indenizacoes)
    for employee in employees:
        emp = employees[employee]
        if employee in remuneracoes.keys():
            remu = remuneracoes[employee]
            emp.remuneracoes.MergeFrom(remu)
        employees[employee] = emp
    return employees


def update_employees_before(file_indenizacoes, employees):
    for row in file_indenizacoes:
        registration = str(row[0])
        if registration in employees.keys():
            new_row = [x for x in row if not number.is_nan(x)]
            emp = employees[registration]
            remu = remunerations_before(new_row)
            emp.remuneracoes.MergeFrom(remu)
            employees[registration] = emp
    return employees


def parse(data, colect_key):
    employees = {}
    payroll = Coleta.FolhaDePagamento()
    # As planilhas de contracheque até junho de 2019 não possuem matrícula e seguem uma ordem diferente de dados.
    # As planilhas de indenizações somente passam a ser disponibilizadas em julho de 2019.
    if int(data.year) > 2019 or (int(data.year) == 2019 and int(data.month) >= 7):
        employees.update(parse_employees_after(
            data.contracheque, colect_key, data.month, data.year))
        # As planilhas de indenizacoes seguem um formato de dados diferente a partir de setembro de 2021. 
        # 07/2020 também segue esse formato, sendo uma exceção em 2020.
        if int(data.year) > 2021 or (int(data.year) == 2021 and int(data.month) >= 9) or (int(data.year) == 2020 and int(data.month) == 7):
            update_employees_after(data.indenizatorias, employees)
        else:
            update_employees_before(data.indenizatorias, employees)
    else:
        employees.update(parse_employees_before(
            data.contracheque, colect_key, data.month, data.year))

    for i in employees.values():
        payroll.contra_cheque.append(i)

    return payroll
