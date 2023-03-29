import sys
import os
import pandas as pd
from status import status


def _readODS(file):
    try:
        data = pd.read_excel(file, engine='odf').to_numpy()
    except Exception as excep:
        status.exit_from_error(status.Error(
            status.SystemError, f"Erro lendo as planilhas: {excep}"))
    return data


def _readXLS(file):
    try:
        data = pd.read_excel(file, engine='xlrd').to_numpy()
    except Exception as excep:
        status.exit_from_error(status.Error(
            status.SystemError, f"Erro lendo as planilhas: {excep}"))
    return data


def load(file_names, year, month, output_folder):
    """Carrega os arquivos passados como parâmetros.
       :param file_names: slice contendo os arquivos baixados pelo coletor.
      Os nomes dos arquivos devem seguir uma convenção e começar com
      Membros ativos-contracheque e Membros ativos-Verbas Indenizatorias
       :param year e month: usados para fazer a validação na planilha de controle de dados
       :return um objeto Data() pronto para operar com os arquivos
      """
    # A extensão das planilhas de contracheques é XLS até maio de 2019
    # Após isso, a extensão adotada foi a ODS.
    if int(year) == 2018 or (int(year) == 2019 and int(month) <= 5):
        contracheque = _readXLS(
            [c for c in file_names if "contracheques" in c][0])
    else:
        contracheque = _readODS(
            [c for c in file_names if "contracheques" in c][0])

    # A publicação dos relatórios de Verbas Indenizatórias e outras Remunerações Temporárias
        # foi iniciada no mês de julho de 2019, em função do início da vigência da Resolução CNMP Nº 200
    if int(year) > 2019 or (int(year) == 2019 and int(month) >= 7):
        indenizatorias = _readODS(
            [i for i in file_names if "indenizacoes" in i][0])
        return Data(contracheque, indenizatorias, year, month, output_folder)
    return DataContracheque(contracheque, year, month, output_folder)


class Data:
    def __init__(self, contracheque, indenizatorias, year, month, output_folder):
        self.year = year
        self.month = month
        self.output_folder = output_folder
        self.contracheque = contracheque
        self.indenizatorias = indenizatorias

    def validate(self):
        """
         Validação inicial dos arquivos passados como parâmetros.
        Aborta a execução do script em caso de erro.
         Caso o validade fique pare o script na leitura da planilha 
        de controle de dados dara um erro retornando o codigo de erro 4,
        esse codigo significa que não existe dados para a data pedida.
        """

        if not (
                os.path.isfile(
                    f"{self.output_folder}/membros-ativos-contracheques-{self.month}-{self.year}.ods"
                )
                or os.path.isfile(
                    f"{self.output_folder}/membros-ativos-indenizacoes-{self.month}-{self.year}.ods"
                )
        ):
            status.exit_from_error(status.Error(
                status.DataUnavailable, f"Não existe planilhas para {self.month}/{self.year}."))


class DataContracheque:
    def __init__(self, contracheque, year, month, output_folder):
        self.year = year
        self.month = month
        self.output_folder = output_folder
        self.contracheque = contracheque

    def validate(self):
        """
        Validação inicial dos arquivos passados como parâmetros.
        Aborta a execução do script em caso de erro.
        Caso o validade falhe, o script na leitura da planilha 
        de controle de dados dara um erro retornando o codigo de erro 4,
        esse codigo significa que não existe dados para a data pedida.
        """
        if int(self.year) == 2018 or (int(self.year) == 2019 and int(self.month) <= 5):
            if not os.path.isfile(f"{self.output_folder}/membros-ativos-contracheques-{self.month}-{self.year}.xls"):
                status.exit_from_error(status.Error(
                    status.DataUnavailable, f"Não existe planilhas para {self.month}/{self.year}."))
        elif not os.path.isfile(f"{self.output_folder}/membros-ativos-contracheques-{self.month}-{self.year}.ods"):
            status.exit_from_error(status.Error(
                status.DataUnavailable, f"Não existe planilhas para {self.month}/{self.year}."))
