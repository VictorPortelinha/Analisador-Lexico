# Aluno: Seu Nome (github: usuario)
# Grupo: NomeDoGrupo
# Disciplina: Linguagens Formais e Autômatos
# Professor: Nome do Professor
# Instituicao: Nome da Instituicao

import sys
import json


# ==============================================================================
# ANALISADOR LEXICO - Automato Finito Deterministico (AFD)
# Cada estado e representado por uma funcao
# ==============================================================================

def estadoInicial(char, pos, linha, tokens, token_atual, erro):
    if char == ' ' or char == '\t':
        return estadoEspaco(char, pos, linha, tokens, token_atual, erro)
    elif char == '(':
        return estadoAbreParentese(char, pos, linha, tokens, token_atual, erro)
    elif char == ')':
        return estadoFechaParentese(char, pos, linha, tokens, token_atual, erro)
    elif char in '0123456789':
        return estadoNumero(char, pos, linha, tokens, token_atual, erro)
    elif char == '-':
        return estadoMenosOuNegativo(char, pos, linha, tokens, token_atual, erro)
    elif char in '+*%^':
        return estadoOperador(char, pos, linha, tokens, token_atual, erro)
    elif char == '/':
        return estadoDivisao(char, pos, linha, tokens, token_atual, erro)
    elif char.isupper():
        return estadoPalavra(char, pos, linha, tokens, token_atual, erro)
    elif char == '\n' or char == '\r' or char == '':
        return ('FIM', tokens, token_atual, erro)
    else:
        return ('ERRO', tokens, token_atual, f"Caractere invalido '{char}' na posicao {pos}")


def estadoEspaco(char, pos, linha, tokens, token_atual, erro):
    if token_atual:
        tokens.append(token_atual)
        token_atual = ''
    return ('INICIAL', tokens, token_atual, erro)


def estadoAbreParentese(char, pos, linha, tokens, token_atual, erro):
    if token_atual:
        tokens.append(token_atual)
        token_atual = ''
    tokens.append('(')
    return ('INICIAL', tokens, '', erro)


def estadoFechaParentese(char, pos, linha, tokens, token_atual, erro):
    if token_atual:
        tokens.append(token_atual)
        token_atual = ''
    tokens.append(')')
    return ('INICIAL', tokens, '', erro)


def estadoOperador(char, pos, linha, tokens, token_atual, erro):
    if token_atual:
        tokens.append(token_atual)
        token_atual = ''
    tokens.append(char)
    return ('INICIAL', tokens, '', erro)


def estadoMenosOuNegativo(char, pos, linha, tokens, token_atual, erro):
    prox = pos + 1
    if prox < len(linha) and linha[prox] in '0123456789':
        return ('NUM', tokens, '-', erro)
    else:
        if token_atual:
            tokens.append(token_atual)
            token_atual = ''
        tokens.append('-')
        return ('INICIAL', tokens, '', erro)


def estadoDivisao(char, pos, linha, tokens, token_atual, erro):
    prox = pos + 1
    if prox < len(linha) and linha[prox] == '/':
        if token_atual:
            tokens.append(token_atual)
            token_atual = ''
        return ('DIV_INT', tokens, '//', erro)
    else:
        if token_atual:
            tokens.append(token_atual)
            token_atual = ''
        tokens.append('/')
        return ('INICIAL', tokens, '', erro)


def estadoNumero(char, pos, linha, tokens, token_atual, erro):
    token_atual += char
    return ('NUM', tokens, token_atual, erro)


def estadoNumContinuacao(char, pos, linha, tokens, token_atual, erro):
    if char in '0123456789':
        token_atual += char
        return ('NUM', tokens, token_atual, erro)
    elif char == '.':
        if '.' in token_atual:
            return ('ERRO', tokens, token_atual, f"Numero malformado '{token_atual}.' na posicao {pos}")
        token_atual += char
        return ('NUM_PONTO', tokens, token_atual, erro)
    elif char == ' ' or char == '\t':
        tokens.append(token_atual)
        return ('INICIAL', tokens, '', erro)
    elif char == ')':
        tokens.append(token_atual)
        tokens.append(')')
        return ('INICIAL', tokens, '', erro)
    elif char == '(':
        tokens.append(token_atual)
        tokens.append('(')
        return ('INICIAL', tokens, '', erro)
    elif char == '\n' or char == '\r' or char == '':
        tokens.append(token_atual)
        return ('FIM', tokens, '', erro)
    else:
        return ('ERRO', tokens, token_atual, f"Caractere invalido '{char}' apos numero na posicao {pos}")


def estadoNumPonto(char, pos, linha, tokens, token_atual, erro):
    if char in '0123456789':
        token_atual += char
        return ('NUM_DEC', tokens, token_atual, erro)
    elif char == '.':
        return ('ERRO', tokens, token_atual, f"Numero malformado '{token_atual}.' na posicao {pos}")
    else:
        return ('ERRO', tokens, token_atual, f"Esperado digito apos ponto em '{token_atual}' na posicao {pos}")


def estadoNumDecimal(char, pos, linha, tokens, token_atual, erro):
    if char in '0123456789':
        token_atual += char
        return ('NUM_DEC', tokens, token_atual, erro)
    elif char == '.':
        return ('ERRO', tokens, token_atual, f"Numero malformado '{token_atual}.' na posicao {pos}")
    elif char == ' ' or char == '\t':
        tokens.append(token_atual)
        return ('INICIAL', tokens, '', erro)
    elif char == ')':
        tokens.append(token_atual)
        tokens.append(')')
        return ('INICIAL', tokens, '', erro)
    elif char == '(':
        tokens.append(token_atual)
        tokens.append('(')
        return ('INICIAL', tokens, '', erro)
    elif char == '\n' or char == '\r' or char == '':
        tokens.append(token_atual)
        return ('FIM', tokens, '', erro)
    else:
        return ('ERRO', tokens, token_atual, f"Caractere invalido '{char}' na posicao {pos}")


def estadoPalavra(char, pos, linha, tokens, token_atual, erro):
    token_atual += char
    return ('PALAVRA', tokens, token_atual, erro)


def estadoPalavraContinuacao(char, pos, linha, tokens, token_atual, erro):
    if char.isupper() or char.isdigit():
        token_atual += char
        return ('PALAVRA', tokens, token_atual, erro)
    elif char == ' ' or char == '\t':
        tokens.append(token_atual)
        return ('INICIAL', tokens, '', erro)
    elif char == ')':
        tokens.append(token_atual)
        tokens.append(')')
        return ('INICIAL', tokens, '', erro)
    elif char == '(':
        tokens.append(token_atual)
        tokens.append('(')
        return ('INICIAL', tokens, '', erro)
    elif char == '\n' or char == '\r' or char == '':
        tokens.append(token_atual)
        return ('FIM', tokens, '', erro)
    else:
        return ('ERRO', tokens, token_atual, f"Caractere invalido '{char}' em identificador na posicao {pos}")


def rodarAFD(linha):
    tokens = []
    token_atual = ''
    erro = None
    estado = 'INICIAL'
    i = 0

    linha = linha.strip()

    while i <= len(linha):
        char = linha[i] if i < len(linha) else ''

        if estado == 'INICIAL':
            resultado = estadoInicial(char, i, linha, tokens, token_atual, erro)
        elif estado == 'NUM':
            resultado = estadoNumContinuacao(char, i, linha, tokens, token_atual, erro)
        elif estado == 'NUM_PONTO':
            resultado = estadoNumPonto(char, i, linha, tokens, token_atual, erro)
        elif estado == 'NUM_DEC':
            resultado = estadoNumDecimal(char, i, linha, tokens, token_atual, erro)
        elif estado == 'PALAVRA':
            resultado = estadoPalavraContinuacao(char, i, linha, tokens, token_atual, erro)
        elif estado == 'DIV_INT':
            tokens.append('//')
            token_atual = ''
            estado = 'INICIAL'
            i += 1
            continue
        elif estado == 'FIM':
            break
        elif estado == 'ERRO':
            return None, erro
        else:
            break

        estado, tokens, token_atual, erro = resultado[0], resultado[1], resultado[2], resultado[3]

        if estado == 'FIM':
            break
        if estado == 'ERRO':
            return None, erro

        i += 1

    if token_atual:
        tokens.append(token_atual)

    return tokens, None


def parseExpressao(linha):
    tokens, erro = rodarAFD(linha)
    if erro:
        print(f"  [ERRO LEXICO] {erro}")
        return []
    return tokens if tokens else []


# ==============================================================================
# LEITURA DE ARQUIVO
# ==============================================================================

def lerArquivo(nomeArquivo):
    linhas = []
    try:
        with open(nomeArquivo, 'r', encoding='utf-8') as f:
            for linha in f:
                linha = linha.strip()
                if linha:
                    linhas.append(linha)
    except FileNotFoundError:
        print(f"[ERRO] Arquivo '{nomeArquivo}' nao encontrado.")
        sys.exit(1)
    except IOError as e:
        print(f"[ERRO] Nao foi possivel ler o arquivo: {e}")
        sys.exit(1)
    return linhas


# ==============================================================================
# SALVAR TOKENS EM JSON
# ==============================================================================

def salvarTokens(tokens_por_linha, nomeArquivo):
    base = nomeArquivo.rsplit('.', 1)[0]
    saida = base + '_tokens.json'
    dados = []
    for i, tokens in enumerate(tokens_por_linha):
        dados.append({'linha': i + 1, 'tokens': tokens})
    with open(saida, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)
    print(f"Tokens salvos em: {saida}")
    return saida


    # ==============================================================================
# GERADOR DE ASSEMBLY ARMv7 (CPULATOR DEC1-SOC)
# ==============================================================================

def gerarAssembly(tokens_por_linha, arquivo_saida="programa.s"):

    asm = []

    asm.append(".global _start")
    asm.append("")
    asm.append(".data")
    asm.append("")

    # variáveis de memória
    mem_vars = set()

    for linha in tokens_por_linha:
        for token in linha:
            if token.isalpha() and token not in ["RES"]:
                mem_vars.add(token)

    for var in mem_vars:
        asm.append(f"{var}: .word 0")

    asm.append("")
    asm.append(".text")
    asm.append("_start:")
    asm.append("")

    linha_index = 0
    label_id = 0

    for tokens in tokens_por_linha:

        asm.append(f"    @ Linha {linha_index+1}")

        for token in tokens:

            if token in ["(", ")"]:
                continue

            # número
            elif token.replace('.', '', 1).isdigit():

                valor = int(float(token))  # converte float para inteiro
                asm.append(f"    LDR r0, ={valor}")
                asm.append("    PUSH {r0}")

            # +
            elif token == "+":

                asm.append("    POP {r1}")
                asm.append("    POP {r0}")
                asm.append("    ADD r0, r0, r1")
                asm.append("    PUSH {r0}")

            # -
            elif token == "-":

                asm.append("    POP {r1}")
                asm.append("    POP {r0}")
                asm.append("    SUB r0, r0, r1")
                asm.append("    PUSH {r0}")

            # *
            elif token == "*":

                asm.append("    POP {r1}")
                asm.append("    POP {r0}")
                asm.append("    MUL r0, r0, r1")
                asm.append("    PUSH {r0}")

            # divisão
            elif token == "/" or token == "//":

                div_id = label_id
                label_id += 1

                asm.append("    POP {r1}")
                asm.append("    POP {r0}")
                asm.append("    MOV r2, #0")

                asm.append(f"div_loop_{div_id}:")
                asm.append("    CMP r0, r1")
                asm.append(f"    BLT div_end_{div_id}")
                asm.append("    SUB r0, r0, r1")
                asm.append("    ADD r2, r2, #1")
                asm.append(f"    B div_loop_{div_id}")

                asm.append(f"div_end_{div_id}:")
                asm.append("    MOV r0, r2")
                asm.append("    PUSH {r0}")

            # resto %
            elif token == "%":

                mod_id = label_id
                label_id += 1

                asm.append("    POP {r1}")
                asm.append("    POP {r0}")

                asm.append(f"mod_loop_{mod_id}:")
                asm.append("    CMP r0, r1")
                asm.append(f"    BLT mod_end_{mod_id}")
                asm.append("    SUB r0, r0, r1")
                asm.append(f"    B mod_loop_{mod_id}")

                asm.append(f"mod_end_{mod_id}:")
                asm.append("    PUSH {r0}")

            # potência ^
            elif token == "^":

                pow_id = label_id
                label_id += 1

                asm.append("    POP {r1}")  # expoente
                asm.append("    POP {r0}")  # base
                asm.append("    MOV r2, #1")

                asm.append(f"pow_loop_{pow_id}:")
                asm.append("    CMP r1, #0")
                asm.append(f"    BEQ pow_end_{pow_id}")
                asm.append("    MUL r2, r2, r0")
                asm.append("    SUB r1, r1, #1")
                asm.append(f"    B pow_loop_{pow_id}")

                asm.append(f"pow_end_{pow_id}:")
                asm.append("    PUSH {r2}")

            # RES
            elif token == "RES":

                asm.append("    @ RES - duplica topo da pilha")
                asm.append("    POP {r0}")
                asm.append("    PUSH {r0}")
                asm.append("    PUSH {r0}")

            # variável
            elif token.isalpha():

                asm.append(f"    LDR r0, ={token}")
                asm.append("    LDR r0, [r0]")
                asm.append("    PUSH {r0}")

        linha_index += 1
        asm.append("")

    asm.append("    POP {r0}")

    asm.append("end:")
    asm.append("    B end")

    with open(arquivo_saida, "w") as f:
        for linha in asm:
            f.write(linha + "\n")

    print(f"\nAssembly gerado em: {arquivo_saida}")

    return asm

def testarAFD():
    print("\n" + "="*60)
    print("TESTES DO ANALISADOR LEXICO (AFD)")
    print("="*60)

    casos_validos = [
        ("(3.14 2.0 +)",               ['(', '3.14', '2.0', '+', ')']),
        ("(5 2 -)",                     ['(', '5', '2', '-', ')']),
        ("(10 3 *)",                    ['(', '10', '3', '*', ')']),
        ("(9.0 3.0 /)",                 ['(', '9.0', '3.0', '/', ')']),
        ("(9 3 //)",                    ['(', '9', '3', '//', ')']),
        ("(10 3 %)",                    ['(', '10', '3', '%', ')']),
        ("(2 8 ^)",                     ['(', '2', '8', '^', ')']),
        ("(5 RES)",                     ['(', '5', 'RES', ')']),
        ("(10.5 CONTADOR)",             ['(', '10.5', 'CONTADOR', ')']),
        ("(CONTADOR)",                  ['(', 'CONTADOR', ')']),
        ("((3.0 2.0 *) (4.0 5.0 *) /)", ['(', '(', '3.0', '2.0', '*', ')', '(', '4.0', '5.0', '*', ')', '/', ')']),
    ]

    casos_invalidos = [
        ("(3.14 2.0 &)",  "operador invalido"),
        ("(3.14.5 2.0 +)", "numero malformado"),
        ("(3,45 2.0 +)",  "separador decimal invalido"),
    ]

    print("\n[Entradas Validas]")
    for entrada, esperado in casos_validos:
        tokens = parseExpressao(entrada)
        ok = tokens == esperado
        status = "OK" if ok else "FALHA"
        print(f"  [{status}] '{entrada}'")
        if not ok:
            print(f"       Esperado: {esperado}")
            print(f"       Obtido:   {tokens}")

    print("\n[Entradas Invalidas - devem gerar erro]")
    for entrada, descricao in casos_invalidos:
        tokens = parseExpressao(entrada)
        status = "OK (erro detectado)" if not tokens else "FALHA (deveria ser invalido)"
        print(f"  [{status}] '{entrada}' ({descricao})")


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    if len(sys.argv) < 2:
        print("Uso: python parser.py <arquivo_de_teste.txt>")
        sys.exit(1)

    nomeArquivo = sys.argv[1]

    print(f"Lendo arquivo: {nomeArquivo}")
    linhas = lerArquivo(nomeArquivo)
    print(f"Total de linhas: {len(linhas)}")

    print("\n" + "="*60)
    print("RESULTADO DA ANALISE LEXICA")
    print("="*60)

    tokens_por_linha = []
    for i, linha in enumerate(linhas):
        tokens = parseExpressao(linha)
        tokens_por_linha.append(tokens)
        print(f"\nLinha {i+1}: {linha}")
        if tokens:
            print(f"  Tokens: {tokens}")
        else:
            print(f"  Tokens: [ERRO ou vazio]")

    salvarTokens(tokens_por_linha, nomeArquivo)
    testarAFD()
    print("\nGerando codigo Assembly ARMv7...")
    gerarAssembly(tokens_por_linha)


if __name__ == '__main__':
    main()
