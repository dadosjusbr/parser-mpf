from parser import parse
import unittest
from google.protobuf.json_format import MessageToDict
import data


class TestParser(unittest.TestCase):
    def test_maio2019(self):
        # A extensão das planilhas de contracheques é XLS até maio de 2019
        self.maxDiff = None

        files = ['src/output_test/sheets/membros-ativos-contracheques-05-2019.xls']

        try:
            dados = data.load(files, '2019', '05', 'src/output_test/sheets/')
            result_data = parse(dados, 'mpf/05/2019')
        except:
            assert False

    def test_junho2019(self):
        # A partir de junho de 2019, a extensão adotada foi a ODS.
        self.maxDiff = None

        files = ['src/output_test/sheets/membros-ativos-contracheques-06-2019.ods']

        try:
            dados = data.load(files, '2019', '06', 'src/output_test/sheets/')
            result_data = parse(dados, 'mpf/06/2019')
        except:
            assert False

    def test_julho2019(self):
        # A publicação de Verbas Indenizatórias e outras Remunerações Temporárias
        # foi iniciada no mês de julho de 2019
        self.maxDiff = None

        files = ['src/output_test/sheets/membros-ativos-contracheques-07-2019.ods',
                 'src/output_test/sheets/membros-ativos-indenizacoes-07-2019.ods']

        try:
            dados = data.load(files, '2019', '07', 'src/output_test/sheets/')
            result_data = parse(dados, 'mpf/07/2019')
        except:
            assert False

    def test_setembro2021(self):
        # As planilhas de indenizacoes seguem um formato de dados diferente a partir de setembro de 2021.
        self.maxDiff = None

        files = ['src/output_test/sheets/membros-ativos-contracheques-09-2021.ods',
                 'src/output_test/sheets/membros-ativos-indenizacoes-09-2021.ods']

        try:
            dados = data.load(files, '2021', '09', 'src/output_test/sheets/')
            result_data = parse(dados, 'mpf/09/2021')
        except:
            assert False


if __name__ == "__main__":
    unittest.main()
