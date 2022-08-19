from parser import parse
import unittest
from google.protobuf.json_format import MessageToDict
import data
import json


class TestParser(unittest.TestCase):
    def test_maio2019(self):
        # A extensão das planilhas de contracheques é XLS até maio de 2019
        self.maxDiff = None
        # Json com a saida esperada
        with open('src/output_test/expected/expected_05_2019.json', 'r') as fp:
            expected = json.load(fp)

        files = ['src/output_test/sheets/membros-ativos-contracheques-05-2019.xls']
        dados = data.load(files, '2019', '05', 'src/output_test/sheets')
        result_data = parse(dados, 'mpf/05/2019')
        # Converto o resultado do parser, em dict
        result_to_dict = MessageToDict(result_data)

        self.assertEqual(expected['contraCheque'][0], result_to_dict['contraCheque'][0])

    def test_junho2019(self):
        # A partir de junho de 2019, a extensão adotada foi a ODS.
        self.maxDiff = None
        # Json com a saida esperada
        with open('src/output_test/expected/expected_06_2019.json', 'r') as fp:
            expected = json.load(fp)

        files = ['src/output_test/sheets/membros-ativos-contracheques-06-2019.ods']
        dados = data.load(files, '2019', '06', 'src/output_test/sheets')
        result_data = parse(dados, 'mpf/06/2019')
        # Converto o resultado do parser, em dict
        result_to_dict = MessageToDict(result_data)

        self.assertEqual(expected['contraCheque'][0], result_to_dict['contraCheque'][0]) 
        
    def test_julho2019(self):
        # A publicação de Verbas Indenizatórias e outras Remunerações Temporárias
        # foi iniciada no mês de julho de 2019
        self.maxDiff = None
        # Json com a saida esperada
        with open('src/output_test/expected/expected_07_2019.json', 'r') as fp:
            expected = json.load(fp)

        files = ['src/output_test/sheets/membros-ativos-contracheques-07-2019.ods',
                 'src/output_test/sheets/membros-ativos-indenizacoes-07-2019.ods']
        dados = data.load(files, '2019', '07', 'src/output_test/sheets')
        result_data = parse(dados, 'mpf/07/2019')
        # Converto o resultado do parser, em dict
        result_to_dict = MessageToDict(result_data)

        self.assertEqual(expected['contraCheque'][0], result_to_dict['contraCheque'][0])

    def test_setembro2021(self):
        # As planilhas de indenizacoes seguem um formato de dados diferente a partir de setembro de 2021.
        self.maxDiff = None
        # Json com a saida esperada
        with open('src/output_test/expected/expected_09_2021.json', 'r') as fp:
            expected = json.load(fp)

        files = ['src/output_test/sheets/membros-ativos-contracheques-09-2021.ods',
                 'src/output_test/sheets/membros-ativos-indenizacoes-09-2021.ods']
        dados = data.load(files, '2021', '09', 'src/output_test/sheets')
        result_data = parse(dados, 'mpf/09/2021')
        # Converto o resultado do parser, em dict
        result_to_dict = MessageToDict(result_data)

        self.assertEqual(expected['contraCheque'][0], result_to_dict['contraCheque'][0])


if __name__ == "__main__":
    unittest.main()
