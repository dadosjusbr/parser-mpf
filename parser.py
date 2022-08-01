import number

from coleta import coleta_pb2 as Coleta

from headers_keys import (HEADERS, REMUNERACAOBASICA,
                          EVENTUALTEMP, OBRIGATORIOS)


def parse_employees(file_name, colect_key):
    employees = {}
    counter = 1
    for row in file_name:
        registration = str(row[0])
        name = row[1]
        function = row[2]
        location = row[3]
        if not number.is_nan(registration) and registration != "Matrícula":
            member = Coleta.ContraCheque()
            member.id_contra_cheque = colect_key + "/" + str(counter)
            member.chave_coleta = colect_key
            member.matricula = registration
            member.nome = name
            member.funcao = function
            member.local_trabalho = location
            member.tipo = Coleta.ContraCheque.Tipo.Value("MEMBRO")
            member.ativo = True

            member.remuneracoes.CopyFrom(
                create_remuneration(row)
            )

            employees[registration] = member
            counter += 1

    return employees


def remunerations(file_indenizatorias):
    dict_remuneracoes = {}
    for row in file_indenizatorias:
        if number.is_nan not in row:
            mat = str(row[0])
            remuneracoes = dict_remuneracoes.get(mat, Coleta.Remuneracoes())
            # Verbas indenizatórias
            if row[4] != "N/C":
                rem = Coleta.Remuneracao()
                rem.natureza = Coleta.Remuneracao.Natureza.Value("R")
                rem.categoria = "Verbas indenizatórias"
                rem.item = str(row[4])
                rem.valor = float(number.format_value(row[5]))
                rem.tipo_receita = Coleta.Remuneracao.TipoReceita.Value("O")
                remuneracoes.remuneracao.append(rem)
            # Outras remunerações temporárias
            if row[6] != "N/C":
                rem = Coleta.Remuneracao()
                rem.natureza = Coleta.Remuneracao.Natureza.Value("R")
                rem.categoria = "Outras remunerações temporárias"
                rem.item = str(row[6])
                rem.valor = float(number.format_value(row[7]))
                rem.tipo_receita = Coleta.Remuneracao.TipoReceita.Value("O")
                remuneracoes.remuneracao.append(rem)
                dict_remuneracoes[mat] = remuneracoes
    return dict_remuneracoes


def create_indenizacoes(employee, remuneracoes):
    if employee in remuneracoes.keys():
        return remuneracoes[employee]


def create_remuneration(row):
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
    for key, value in HEADERS[OBRIGATORIOS].items():
        remuneration = Coleta.Remuneracao()
        remuneration.natureza = Coleta.Remuneracao.Natureza.Value("D")
        remuneration.categoria = OBRIGATORIOS
        remuneration.item = key
        remuneration.valor = float(number.format_value(row[value])) * (-1)
        remuneration_array.remuneracao.append(remuneration)

    return remuneration_array


def update_employees(file_indenizatorias, employees):
    remuneracoes = remunerations(file_indenizatorias)
    for employee in employees:
        emp = employees[employee]
        remu = create_indenizacoes(employee, remuneracoes)
        emp.remuneracoes.MergeFrom(remu)
        employees[employee] = emp
    return employees


def parse(data, colect_key):
    employees = {}
    payroll = Coleta.FolhaDePagamento()

    employees.update(parse_employees(data.contracheque, colect_key))
    update_employees(data.indenizatorias, employees)

    for i in employees.values():
        payroll.contra_cheque.append(i)

    return payroll
