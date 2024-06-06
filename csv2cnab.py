import csv

def format_number(number, length):
    return str(number).zfill(length)

def format_text(text, length):
    return str(text).ljust(length)[:length]

def generate_cnab400(csv_file, cnab400_file):
    with open(csv_file, 'r') as csvfile, open(cnab400_file, 'w') as cnabfile:
        reader = csv.DictReader(csvfile)
        
        # Registro Header
        for row in reader:
            header = (
                format_text("0", 1) +
                format_text("1", 1) +
                format_text("REMESSA", 7) +
                format_text("01", 2) +
                format_text("COBRANCA", 15) +
                format_text("", 20) +
                format_text(row['empresa_nome'], 30) +
                format_text("077", 3) +
                format_text("Inter", 15) +
                format_text("", 10) +
                format_number(row['sequencial_remessa'], 7) +
                format_text("", 277) +
                format_number(1, 6) +
                "\n"
            )
            cnabfile.write(header)
            break
        
        csvfile.seek(0)
        next(reader)

        # Registro de Transação Tipo 1
        sequencial_registro = 2
        for row in reader:
            transacao = (
                format_text("1", 1) +
                format_text("", 19) +
                format_text(f"{row['carteira']}{row['agencia']}{row['conta'].zfill(10)}", 17) +
                format_text(row['controle'], 25) +
                format_text("", 3) +
                format_text("0", 1) +
                format_number(0, 13) +
                format_number(0, 4) +
                format_text("000000", 6) +
                format_text("00000000000", 11) +
                format_text("", 8) +
                format_text("01", 2) +
                format_text(row['numero_documento'], 10) +
                format_text(row['data_vencimento'], 6) +
                format_number(row['valor_titulo'].replace('.', ''), 13) +
                format_text("0", 2) +
                format_text("", 6) +
                format_text("01", 2) +
                format_text("N", 1) +
                format_text("", 6) +
                format_text("", 3) +
                format_text("0", 1) +
                format_number(0, 13) +
                format_number(0, 4) +
                format_text("000000", 6) +
                format_text("", 13) +
                format_text(row['pagador_tipo_inscricao'], 2) +
                format_number(row['pagador_numero_inscricao'], 14) +
                format_text(row['pagador_nome'], 40) +
                format_text(row['pagador_endereco'], 40) +
                format_number(row['pagador_cep'], 5) +
                format_number(row['pagador_cep_sufixo'], 3) +
                format_text("", 70) +
                format_number(sequencial_registro, 6) +
                "\n"
            )
            cnabfile.write(transacao)
            sequencial_registro += 1
        
        # Registro Trailer
        trailer = (
            format_text("9", 1) +
            format_number(sequencial_registro - 2, 6) +
            format_text("", 387) +
            format_number(sequencial_registro, 6) +
            "\n"
        )
        cnabfile.write(trailer)

# Uso do script
generate_cnab400('modelo.csv', 'saida.cnab')
