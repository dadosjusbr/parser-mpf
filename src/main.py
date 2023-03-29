import sys
import os
import metadata
import data

from coleta import coleta_pb2 as Coleta, IDColeta
from google.protobuf.timestamp_pb2 import Timestamp
from google.protobuf import text_format
from parser import parse
from status import status

if "YEAR" in os.environ:
    YEAR = os.environ["YEAR"]
else:
    status.exit_from_error(status.Error(status.InvalidInput, "YEAR environment variable not set\n"))

if "MONTH" in os.environ:
    MONTH = os.environ["MONTH"]
else:
    status.exit_from_error(status.Error(status.InvalidInput, "MONTH environment variable not set\n"))

if "OUTPUT_FOLDER" in os.environ:
    OUTPUT_FOLDER = os.environ["OUTPUT_FOLDER"]
else:
    OUTPUT_FOLDER = "/output"

if "CRAWLER_VERSION" in os.environ:
    CRAWLER_VERSION = os.environ["CRAWLER_VERSION"]
else:
    CRAWLER_VERSION = "unspecified"

if "PARSER_VERSION" in os.environ:
    PARSER_VERSION = os.environ["PARSER_VERSION"]
else:
    PARSER_VERSION = "unspecified"


def parse_execution(data, file_names):
    # Cria objeto com dados da coleta.
    coleta = Coleta.Coleta()
    coleta.chave_coleta = IDColeta("mpf", MONTH, YEAR)
    coleta.orgao = "mpf"
    coleta.mes = int(MONTH)
    coleta.ano = int(YEAR)
    coleta.repositorio_coletor = "https://github.com/dadosjusbr/coletor-mpf"
    coleta.versao_coletor = CRAWLER_VERSION
    coleta.repositorio_parser = "https://github.com/dadosjusbr/parser-mpf"
    coleta.versao_parser = PARSER_VERSION
    coleta.arquivos.extend(file_names)
    timestamp = Timestamp()
    timestamp.GetCurrentTime()
    coleta.timestamp_coleta.CopyFrom(timestamp)

    # Consolida folha de pagamento
    payroll = Coleta.FolhaDePagamento()
    payroll = parse(data, coleta.chave_coleta)

    # Monta resultado da coleta.
    rc = Coleta.ResultadoColeta()
    rc.folha.CopyFrom(payroll)
    rc.coleta.CopyFrom(coleta)

    mt = metadata.get(int(MONTH), int(YEAR))
    rc.metadados.CopyFrom(mt)

    # Imprime a versão textual na saída padrão.
    print(text_format.MessageToString(rc), flush=True, end="")


# Main execution
def main():
    file_names = [f.rstrip() for f in sys.stdin.readlines()]
    dt = data.load(file_names, YEAR, MONTH, OUTPUT_FOLDER)
    dt.validate()
    parse_execution(dt, file_names)


if __name__ == "__main__":
    main()
