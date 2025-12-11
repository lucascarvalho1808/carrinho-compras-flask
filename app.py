from flask import Flask, render_template, request, redirect, url_for, session, flash

# Criar a aplicação Flask
app = Flask(__name__)

# Chave secreta para sessões (em produção, use uma chave mais segura)
app.secret_key = '01a20eb3f73e21ff9a4e7e3520380fb2570f0b056811ad1ac84481a63c9299b5'

# Configuração dos produtos (simulando um banco de dados)
app.config['PRODUTOS'] = {
    1: {
        'id': 1, 
        'nome': 'Smartphone Galaxy', 
        'preco': 1200.00, 
        'imagem_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/14/Product_sample_icon_picture.png/640px-Product_sample_icon_picture.png'
    },
    2: {
        'id': 2, 
        'nome': 'Notebook Dell', 
        'preco': 3500.00, 
        'imagem_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/14/Product_sample_icon_picture.png/640px-Product_sample_icon_picture.png'
    },
    3: {
        'id': 3, 
        'nome': 'Fone de Ouvido Bluetooth', 
        'preco': 150.00, 
        'imagem_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/14/Product_sample_icon_picture.png/640px-Product_sample_icon_picture.png'
    },
    4: {
        'id': 4, 
        'nome': 'Monitor 24 Polegadas', 
        'preco': 899.90, 
        'imagem_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/14/Product_sample_icon_picture.png/640px-Product_sample_icon_picture.png'
    },
    5: {
        'id': 5, 
        'nome': 'Teclado Mecânico', 
        'preco': 250.50, 
        'imagem_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/14/Product_sample_icon_picture.png/640px-Product_sample_icon_picture.png'
    },
    6: {
        'id': 6, 
        'nome': 'Mouse Gamer', 
        'preco': 120.00, 
        'imagem_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/14/Product_sample_icon_picture.png/640px-Product_sample_icon_picture.png'
    },
}

# Rota principal - Lista de produtos
@app.route('/')
def index():
    produtos = app.config['PRODUTOS']
    return render_template('index.html', produtos=produtos)

# Rota Sobre a Loja
@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

# Rota para adicionar produto ao carrinho
@app.route('/adicionar/<int:produto_id>', methods=['POST'])
def adicionar_ao_carrinho(produto_id):
    produtos = app.config['PRODUTOS']
    
    # Recuperar carrinho da sessão (ou criar lista vazia)
    carrinho = session.get('carrinho', [])
    
    # Verificar se o produto já está no carrinho
    produto_encontrado = False
    for item in carrinho:
        if item['id'] == produto_id:
            # Se já existe, incrementa a quantidade
            item['quantidade'] = item.get('quantidade', 1) + 1
            produto_encontrado = True
            break
    
    # Se não encontrou, adiciona como novo item com quantidade 1
    if not produto_encontrado:
        novo_item = produtos[produto_id].copy()
        novo_item['quantidade'] = 1
        carrinho.append(novo_item)
    
    # Salvar carrinho na sessão
    session['carrinho'] = carrinho
    
    # Mensagem de feedback
    flash('Produto adicionado ao carrinho!')
    
    return redirect(url_for('index'))

# Rota para visualizar o carrinho
@app.route('/carrinho')
def carrinho():
    carrinho = session.get('carrinho', [])
    
    # Calcular total considerando a quantidade
    total = sum(item['preco'] * item.get('quantidade', 1) for item in carrinho)
    
    return render_template('carrinho.html', carrinho=carrinho, total=total)

# Rota para remover produto do carrinho
@app.route('/remover/<int:produto_id>', methods=['POST'])
def remover_do_carrinho(produto_id):
    carrinho = session.get('carrinho', [])
    
    # Recriar a lista mantendo apenas os itens que NÃO têm o ID informado
    carrinho = [item for item in carrinho if item['id'] != produto_id]
    
    session['carrinho'] = carrinho
    flash('Produto removido do carrinho!')
    
    return redirect(url_for('carrinho'))

# Rota para limpar todo o carrinho
@app.route('/limpar', methods=['POST'])
def limpar_carrinho():
    session.pop('carrinho', None)

# Executar aplicação
if __name__ == '__main__':
    app.run(debug=True)