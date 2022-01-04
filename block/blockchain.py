import datetime
import hashlib
import json
from flask import Flask, jsonify


#block genesis
class blockchain:
    def __init__(self):
        self.chain =[]
        self.criar_bloco(prova = 1, hash_anterior='0')

    #criando bloco 
    def criar_bloco(self,prova, hash_anterior): 
        bloco ={'index': len(self.chain)+1, 
                'timestamp': str(datetime.datetime.now()),
                'prova': prova,
                'hash_anterior':hash_anterior}

        self.chain.append(bloco)
        return bloco

        #funcao pra retornar o bloco anterior
    def get_bloco_anterior(self):
        return self.chain[-1]

    #proof of work
    def prova_de_trabalho(self,prova_anterior):
        nova_prova = 1
        checar_prova = False

        while checar_prova is False:
            operacao_hash = hashlib.sha256(str(nova_prova**2 - prova_anterior**2).encode()).hexdigest()
            if operacao_hash[:4] == '0000':
                checar_prova = True
            else:
                 nova_prova +=1
        return nova_prova

    def hash(sef,bloco):
        encoded_boco = json.dumps(bloco,sort_keys=True).encode()
        return hashlib.sha256(encoded_boco).hexdigest()

    #valiadacao do bloco
    def chain_valida(self,chain):
        bloco_anterior = chain[0]
        bloco_index = 1
        while bloco_anterior < len (chain):
            block = chain[bloco_index]
            if block['bloco_anterior'] != self.hash(bloco_anterior):     #1 validacao
                return False
            prova_anterior = prova_anterior ['prova']
            prova = block['prova']
            operacao_hash = hashlib.sha256(str(prova**2 - prova_anterior**2).encode()).hexdigest()
            if operacao_hash[:4] != '0000':                 #2 avalidacao
                return False
            prova_anterior = block
            bloco_index = +1
        return True


app = Flask(__name__)

blockchain = blockchain()

@app.route('/mineracao_de_bloco', methods =['GET'] )
def mineracao_de_bloco():
    bloco_anterior = blockchain.get_bloco_anterior()
    prova_anterior = bloco_anterior['prova']
    prova = blockchain.prova_de_trabalho(prova_anterior)
    hash_anterior = blockchain.hash(bloco_anterior)
    block = blockchain.criar_bloco(prova, prova_anterior)
    response = {'mensagem':' mineracao concluida',
                'index':block ['index'],
                'timestamp':block ['timestamp'],
                'prova':block ['prova'],
                'hash_anteriror':block ['hash_anterior'] }
    return jsonify(response), 200 

@app.route('/get_chain', methods =['GET'] )
def get_chain():
    response = {'chain': blockchain.chain,
                'lenght': 0}
    return jsonify(response),200

app.run(host = '0.0.0.0', port=5000)
