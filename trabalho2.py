#!/usr/bin/python
# coding: utf-8

import sys
from trabalho1 import *

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
    return [linhasArquivo[0],linhasArquivo[1],linhasArquivo[2:]] #Matriz[0] = coordenadas, Matriz[1]=problema em forma de matriz
#####

#####
"""
Funcao: condicaoParadaFirstPhase
Entrada: matriz com o problema, vetor de variaveis artificiais
Saida: booleano
"""
def condicaoParadaFirstPhase(problema,artificiais):
    mask=[0 for x in problema[0]]
    for x in range(0,len(mask)):
        if(x in artificiais):
            mask[x]=-1;
    return map(lambda x: int(x),problema[0])==mask;
#####
#####
"""
Funcao: simplexFirstPhase
Entrada: matriz com o problema
Saida: matriz com bae artificial
"""
def simplexFirstPhase(matriz,debug):
    coordenadas=matriz[0]
    problema=matriz[1]

    for i in range(0,len(problema[0])):
        if(problema[0][i] != 0):
            problema[0][i]=-1*(problema[0][i])


    artificiais = [x for x in range(int(coordenadas[1])) if problema[0][x] != 0]
    artificialObjectiveFunctionPivoting(problema,getLineArtificial(problema,artificiais))
    naoBasicas=[x for x in range(0,int(coordenadas[1])-1) if not(verificaBase(x,problema))]
    basicas=[x for x in range(0, int(coordenadas[1])-1) if verificaBase(x,problema)]
    aux = 0

    while(not(condicaoParadaFirstPhase(problema,artificiais))):
        printTabela(problema)
        aux=aux+1
        candidato=maximoZ(problema[0],naoBasicas)
        saindo=minimoBase(candidato,basicas,problema[1:])
        saindo[0] = saindo[0] +1
        variavelSaindo=saindo[1]
        saindo=saindo[0]
        print saindo
        print variavelSaindo
        print candidato
        naoBasicas.remove(candidato)
        naoBasicas.append(variavelSaindo)
        basicas.remove(variavelSaindo)
        basicas.append(candidato)
        pivoteamento(problema,saindo,candidato)
    printTabela(problema)
    coordenadas[0] -= 1
    coordenadas[1] -= len(artificiais)
    problema = problema[1:]
    for linha in range(0,len(problema)):
        for artificial in artificiais:
            problema[linha].pop(artificiais[0])
    return [coordenadas,problema]

#####

def getLineArtificial(problema,artificiais):
    lines = []
    for line in range(1,len(problema)):
        for column in artificiais:
            if problema[line][column] != 0 :
                lines.append(line)
    return lines

def artificialObjectiveFunctionPivoting(problema,artificiais):
    for artificial in artificiais:
        for pos in range(0,len(problema[0])):
            problema[0][pos] += problema[artificial][pos]

#####
def main():
    matriz=geraMatriz(leArquivo(sys.argv));
    if (matriz[0][0] == 1):
        matriz = simplexFirstPhase(matriz[1:],False);
        simplex(matriz,False);
    else:
        simplex(matriz[1:],False);
#####

main()
