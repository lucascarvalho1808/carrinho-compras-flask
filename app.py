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

# Rota para adicionar produto ao carrinho
@app.route('/adicionar/<int:produto_id>', methods=['POST'])
def adicionar_ao_carrinho(produto_id):
    produtos = app.config['PRODUTOS']
    
    # Recuperar carrinho da sessão (ou criar lista vazia)
    carrinho = session.get('carrinho', [])
    
    # Adicionar produto ao carrinho
    carrinho.append(produtos[produto_id])
    
    # Salvar carrinho na sessão
    session['carrinho'] = carrinho
    
    # Mensagem de feedback
    flash('Produto adicionado ao carrinho!')
    
    return redirect(url_for('index'))

# Rota para visualizar o carrinho
@app.route('/carrinho')
def carrinho():
    carrinho = session.get('carrinho', [])
    
    # Calcular total
    total = sum(item['preco'] for item in carrinho)
    
    return render_template('carrinho.html', carrinho=carrinho, total=total)

# Rota para remover produto do carrinho
@app.route('/remover/<int:produto_id>', methods=['POST'])
def remover_do_carrinho(produto_id):
    carrinho = session.get('carrinho', [])
    
    # Procurar e remover produto
    for produto in carrinho:
        if produto['id'] == produto_id:
            carrinho.remove(produto)
            session['carrinho'] = carrinho
            flash('Produto removido do carrinho!')
            break
    else:
        flash('Produto não encontrado no carrinho.')
    
    return redirect(url_for('carrinho'))

# Executar aplicação
if __name__ == '__main__':
    app.run(debug=True)