#!/usr/bin/python
# coding: utf-8

import sys

#####
"""
Funcao: leArquivo
Entrada: parametros do programa
Saida: lista com linhas do arquivo em formato string
"""
def leArquivo(parametros):

    if(len(parametros)>1):
        arquivo_entrada=open(parametros[1],'r')
    else:
        print('Arquivo nao encontrado');
        exit()

    linhasDoArquivo=arquivo_entrada.readlines()
    arquivo_entrada.close()
    return linhasDoArquivo
#####

#####
"""
Funcao: geraMatriz
Entrada: linhas do arquivo de entrada
Saida: o problema em forma de matriz
"""
def geraMatriz(linhasArquivo):
    for i in range(0,len(linhasArquivo)): #pega cada uma das linhas
        linhasArquivo[i]=linhasArquivo[i].split(" ") #separa os numeros pelo espaco
        for j in range(0,len(linhasArquivo[i])): #pega cada um dos numeros separados ainda como string
            linhasArquivo[i][j]=float(linhasArquivo[i][j]) #transforma um por um em inteiro
    return [linhasArquivo[0],linhasArquivo[1:]] #Matriz[0] = coordenadas, Matriz[1]=problema em forma de matriz
#####

#####
"""
Funcao: maximoZ
Entrada: Linha com os Z-C, variaveis nao basicas
Saida: indice da variavel nao basica com maior valor na lista Z
"""
def maximoZ(linha,vnb):

    candidato=vnb[0]

    for i in vnb[1:]:
        if(linha[i] > linha[candidato]):
            candidato = i

    return candidato
#####

#####
"""
Funcao: paradaOtimo
Entrada: linha dos Z-C
Saida: Verdadeiros se todos forem menores  ou iguais a 0, Falso senao
"""
def paradaOtimo(linhaZc):
    for i in linhaZc:
        if(i>0): return False
    return True
#####

#####
"""
Funcao: printTabela
Entrada: iteracao,problema na forma matricial
Saida:
Descricao: printa a tabela da iteracao
"""
def printTabela(iteracao,problema):
    print("Tabela da iteracao ",iteracao,":");
    for i in problema:
        print(i);
    print();
#####

#####
"""
Funcao: minimoBase
Entrada:candidato a base,variaveis basicas,problema em forma matricial
Saida:quem deve sair da base
"""
def minimoBase(candidato,vb,problema):
    flag=True
    coluna_dosCustos=len(problema[0])-1
    coluna_doCandidato=candidato
    saindo=42

    for i in range(1,len(problema)):
        if(problema[i][coluna_doCandidato] > 0):
            if(flag):
                saindo=i
                flag=False
            elif((problema[i][coluna_dosCustos]/problema[i][coluna_doCandidato]) < (problema[saindo][coluna_dosCustos]/problema[saindo][coluna_doCandidato])): saindo = i;
    colunaSaindo=0;
    for i in vb:
        if(problema[saindo][i]==1):
            colunaSaindo=i;
            break;
    return [saindo,colunaSaindo]
#####

#####
"""
Funcao: verificaDivergencia
Entrada: problema em forma matricial, variaveis nao basicas
Saida: se o problema diverge
"""
def verificaDivergencia(problema,vnb):
    for j in vnb:  ##Pega  cada uma das variaveis nao basicas
        flag=True
        for i in range(1,len(problema)): ##Percorrendo toda a coluna da variavel com excessao da linha Z-C
            if(problema[i][j] > 0): ###Se encontra algum valor maior que 0 ja retorna pra cima
                flag=False
                break;
        if(flag): return True ###Se encontrou uma coluna em que ninguem era maior que 0
    return False;
#####

#####
"""
Funcao: pivoteamento
Entrada: as dimensoes da matriz, o problema em forma matricial, o indice de quem esta entrando na base, o indice de quem esta saindo
Descricao: realiza o pivoteamento ajustando os valores
"""
def pivoteamento(problema,linha,coluna):
    pivo = problema[linha][coluna]
    for i in range(0,len(problema)):
        if(i!=linha):
            fator= problema[i][coluna]/pivo
            for j in range(0,len(problema[i])):
                problema[i][j]=problema[i][j]-(fator)*problema[linha][j]
    for j in range(0,len(problema[linha])):
        problema[linha][j]=problema[linha][j]/pivo
#####

def verificaDegeneracao(problema,vb):
    coluna_dosCustos=len(problema[0])-1
    for i in range(1,len(problema)):
        if(problema[i][coluna_dosCustos] == 0): return 'Degenerada'
    return 'Unica'


#####
"""
Funcao: simplex
Entrada: matriz com o problema
Saida: imprime as tabelas e a solucao caso possivel
"""
def simplex(matriz,debug):
    iteracoes=0;
    coordenadas=matriz[0]
    problema=matriz[1]

    variaveis_naoBasicas=[x for x in range(0,int(coordenadas[1]-coordenadas[0]))]
    variaveis_Basicas=[x for x in range(int(coordenadas[1]-coordenadas[0]),int(coordenadas[1]-1))]
    ## Base inicial = variaveis de folga


    while(not(paradaOtimo(problema[0]))):

        iteracoes=iteracoes+1
        printTabela(iteracoes,problema)

        if(verificaDivergencia(problema,variaveis_naoBasicas)):
           print('Solucao diverge');
           exit()

        candidato=maximoZ(problema[0],variaveis_naoBasicas)
        ###
        if(debug):
            print('variaveis nao basicas: ',variaveis_naoBasicas);
            print('variaveis basicas: ',variaveis_Basicas);
        ###
        if(debug): print('Candidato da iteracao ',iteracoes,': ',candidato);
        saindo=minimoBase(candidato,variaveis_Basicas,problema)
        if(debug): print('Saindo na iteracao ',iteracoes,': ',saindo);
        variavelSaindo=saindo[1]
        saindo=saindo[0]
        variaveis_naoBasicas.remove(candidato)
        variaveis_naoBasicas.append(variavelSaindo)
        variaveis_Basicas.remove(variavelSaindo)
        variaveis_Basicas.append(candidato)

        pivoteamento(problema,saindo,candidato)

    printTabela(iteracoes+1,problema)
    printResultado2(problema)
    print('Solucao ',verificaDegeneracao(problema,variaveis_Basicas),' ',verificaMultiplicidade(problema,variaveis_Basicas));

#####

def printResultado(problema,vb):

    coluna_dosCustos = len(problema[0])-1
    resultado=[0 for x in range(0,len(problema[1]))]
    CustoZ=problema[0][coluna_dosCustos]
    linha_atual=1
    for i in  vb:
        resultado[i]=problema[linha_atual][coluna_dosCustos]
        linha_atual=linha_atual+1

    print('Custo= ',CustoZ);
    for i in range(0,len(resultado)):
        print('x',i,': ',resultado[i],'; ')
    print();

def printResultado2(problema):
    custos = problema[0]
    x = []
    for i in range(0,len(custos)-1):
        if(custos[i] != 0):
            x.append(str(0))
        else:
            for j in range(1,len(problema)):
                if(problema[j][i] != 0):
                    x.append(str(problema[j][len(custos)-1]))
    print 'Custo = ',custos[-1]
    print "x = (",', '.join(x),")"


def verificaMultiplicidade(problema,vnb):
    for i in vnb:
        if(problema[0][i]==0):return 'Multipla'
    return 'Simples'

#####
def main():
    matriz=geraMatriz(leArquivo(sys.argv))
    for i in range(0,len(matriz[1][0])):
        if(matriz[1][0][i] != 0):
            matriz[1][0][i]=-1*(matriz[1][0][i])
    print matriz
    simplex(matriz,False)
#####

main()
