import unittest

import data


# test_validade_existence é uma validação para ver se a planilha não foi apagada no processo.
# Em todos os casos, o mês é alterado para simular erro.

class TestData(unittest.TestCase):
    def test_validate_existence_maio2019(self):
        # A extensão das planilhas de contracheques é XLS até maio de 2019
        file_names = ['src/output_test/sheets/membros-ativos-contracheques-05-2019.xls']
        STATUS_DATA_UNAVAILABLE = 4
        with self.assertRaises(SystemExit) as cm:
            dados = data.load(file_names, "2019", "04", "src/output_test/sheets")
            dados.validate()
        self.assertEqual(cm.exception.code, STATUS_DATA_UNAVAILABLE)

    def test_validate_existence_julho2019(self):
        # A partir de junho de 2019, a extensão adotada foi a ODS.
        # E a publicação de Verbas Indenizatórias e outras Remunerações Temporárias
        # foi iniciada no mês de julho de 2019
        file_names = ['src/output_test/sheets/membros-ativos-contracheques-07-2019.ods',
                      'src/output_test/sheets/membros-ativos-indenizacoes-07-2019.ods']
        STATUS_DATA_UNAVAILABLE = 4
        with self.assertRaises(SystemExit) as cm:
            dados = data.load(file_names, "2019", "08", "src/output_test/sheets")
            dados.validate()
        self.assertEqual(cm.exception.code, STATUS_DATA_UNAVAILABLE)

    def test_validate_existence_setembro2021(self):
        # As planilhas de indenizacoes seguem um formato de dados diferente a partir de setembro de 2021.
        file_names = ['src/output_test/sheets/membros-ativos-contracheques-09-2021.ods',
                      'src/output_test/sheets/membros-ativos-indenizacoes-09-2021.ods']
        STATUS_DATA_UNAVAILABLE = 4
        with self.assertRaises(SystemExit) as cm:
            dados = data.load(file_names, "2021", "10", "src/output_test/sheets")
            dados.validate()
        self.assertEqual(cm.exception.code, STATUS_DATA_UNAVAILABLE)


if __name__ == "__main__":
    unittest.main()
