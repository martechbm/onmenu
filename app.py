from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import qrcode
import io
import base64

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cardapio.db'
db = SQLAlchemy(app)

# Modelos
class Lojista(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    preco = db.Column(db.Float, nullable=False)
    lojista_id = db.Column(db.Integer, db.ForeignKey('lojista.id'), nullable=False)

# Rotas
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro_lojista():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        
        novo_lojista = Lojista(nome=nome, email=email, senha=senha)
        db.session.add(novo_lojista)
        db.session.commit()
        
        return jsonify({'message': 'Lojista cadastrado com sucesso!'})
    
    return render_template('cadastro.html')

@app.route('/catalogo/<int:lojista_id>', methods=['GET', 'POST'])
def gerenciar_catalogo(lojista_id):
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        preco = float(request.form['preco'])
        
        novo_produto = Produto(nome=nome, descricao=descricao, preco=preco, lojista_id=lojista_id)
        db.session.add(novo_produto)
        db.session.commit()
        
        return jsonify({'message': 'Produto adicionado com sucesso!'})
    
    produtos = Produto.query.filter_by(lojista_id=lojista_id).all()
    return render_template('catalogo.html', produtos=produtos)

@app.route('/gerar_qrcode/<int:lojista_id>')
def gerar_qrcode(lojista_id):
    url = f"http://seudominio.com/cardapio/{lojista_id}"
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    return f'<img src="data:image/png;base64,{img_str}">'

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)