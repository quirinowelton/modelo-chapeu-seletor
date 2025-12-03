import pandas as pd
import random
from faker import Faker

# Inicializa o Faker para gerar nomes (britânicos, para o tema)
fake = Faker('en_GB')

# --- Definição das Colunas ---
categorical_cols = [
    'nome', 'genero', 'blood_status', 'profissao', 'casa', 
    'patrono', 'elemento_preferido', 'animal_preferido', 'cor'
]

numerical_cols = [
    'coragem', 'ambicao', 'inteligencia', 'lealdade', 'determinacao', 'justica', 
    'criatividade', 'coragem_moral', 'cautela', 'lealdade_a_amigos', 
    'competitividade', 'individualismo', 'cooperacao', 'fama_reconhecimento', 
    'pertencimento_comunidade', 'pensamento_analitico', 'intuicao', 'estrategia', 
    'impulsividade', 'autocontrole', 'empatia', 'etica', 'pragmatismo', 
    'lideranca', 'leitura_de_pessoas', 'persistencia', 'humildade', 'orgulho', 
    'busca_por_proposito_pessoal', 'identidade_forte'
]

# --- Definição dos Perfis de Atributos (Onde a mágica acontece) ---
# Cada atributo terá um range (min, max) de 1 a 10, enviesado pela casa.

# Função auxiliar para gerar um valor dentro do range
def get_stat(min_val, max_val):
    return random.randint(min_val, max_val)

# Define os "perfis" de personalidade para cada casa (range de 1-10)
# (Default é (1, 10) se não for especificado)
profiles = {
    'Gryffindor': {
        'coragem': (7, 10), 'coragem_moral': (7, 10), 'lealdade_a_amigos': (6, 10),
        'impulsividade': (6, 10), 'lideranca': (5, 9), 'determinacao': (5, 9),
        'cautela': (1, 4), 'estrategia': (2, 6), 'pragmatismo': (1, 5), 
        'competitividade': (4, 8), 'ambicao': (3, 7), 'inteligencia': (4, 8)
    },
    'Slytherin': {
        'ambicao': (8, 10), 'determinacao': (7, 10), 'estrategia': (7, 10),
        'lideranca': (6, 10), 'autocontrole': (6, 10), 'orgulho': (7, 10),
        'individualismo': (7, 10), 'competitividade': (8, 10), 'pragmatismo': (6, 10),
        'empatia': (1, 4), 'humildade': (1, 3), 'justica': (2, 5), 
        'cooperacao': (2, 6), 'lealdade': (3, 7) # Lealdade seletiva
    },
    'Ravenclaw': {
        'inteligencia': (8, 10), 'criatividade': (7, 10), 'pensamento_analitico': (8, 10),
        'intuicao': (6, 10), 'busca_por_proposito_pessoal': (7, 10), 'individualismo': (6, 9),
        'leitura_de_pessoas': (5, 9), 'cautela': (5, 9), 'estrategia': (5, 9),
        'impulsividade': (1, 5), 'cooperacao': (3, 7), 'pertencimento_comunidade': (2, 6),
        'coragem': (3, 7)
    },
    'Hufflepuff': {
        'lealdade': (8, 10), 'lealdade_a_amigos': (8, 10), 'justica': (7, 10),
        'cooperacao': (7, 10), 'pertencimento_comunidade': (7, 10), 'empatia': (8, 10),
        'etica': (7, 10), 'persistencia': (6, 10), 'humildade': (6, 10),
        'ambicao': (1, 5), 'competitividade': (1, 5), 'individualismo': (2, 6),
        'orgulho': (2, 6), 'lideranca': (3, 7), 'estrategia': (3, 7)
    }
}

# --- Listas de Opções Categóricas (ATUALIZADAS) ---
generos = ['Masculino', 'Feminino', 'Não-Binário']
blood_statuses = ['Puro-Sangue', 'Mestiço', 'Nascido-Trouxa']

# LISTA DE PROFISSÕES ATUALIZADA
profissoes = [
    'Estudante', 'Auror', 'Professor(a)', 'Funcionário(a) do Ministério', 
    'Medibruxo(a)', 'Curandeiro(a)', 'Lojista', 'Jornalista', 'Jogador(a) de Quadribol', 
    'Desempregado(a)', 'Tratador(a) de Criaturas Mágicas', 'Inominável', 
    'Fabricante de Varinhas', 'Pocionista', 'Pesquisador(a)', 'Membro da Suprema Corte',
    'Herbologista'
]

patronos = [
    'Cervo', 'Lontra', 'Cão', 'Gato', 'Cavalo', 'Fênix', 'Lebre', 'Doninha', 
    'Cisne', 'Raposa', 'Lobo', 'Urso', 'Águia', 'Salmão', 'Texugo', 'Serpente', 'Indeterminado'
]

# LISTA DE ANIMAIS ATUALIZADA
animais = [
    'Coruja', 'Gato', 'Sapo', 'Rato', 'Furão', 'Cachorro', 'Pomo', # Originais
    'Serpente', 'Mini-pufe', 'Hipogrifo', 'Aranha', 'Testrálio', 'Fênix',
    'Amasso (Kneazle)', 'Dragão (miniatura)'
]

elementos = ['Fogo', 'Água', 'Terra', 'Ar']
cores = [
    'Vermelho', 'Verde', 'Azul', 'Amarelo', 'Preto', 'Branco', 'Prata', 
    'Dourado', 'Bronze', 'Roxo'
]
casas = ['Gryffindor', 'Slytherin', 'Ravenclaw', 'Hufflepuff']

# --- Geração dos Dados ---
data = []
total_rows = 5000

print(f"Gerando {total_rows} registros...")

for _ in range(total_rows):
    row = {}
    
    # 1. Escolher a Casa (base para os stats)
    casa = random.choice(casas)
    row['casa'] = casa
    
    # 2. Gerar Dados Categóricos
    row['nome'] = fake.name()
    row['genero'] = random.choice(generos)
    row['blood_status'] = random.choices(blood_statuses, weights=[0.3, 0.4, 0.3], k=1)[0]
    row['profissao'] = random.choice(profissoes)
    row['patrono'] = random.choice(patronos)
    row['animal_preferido'] = random.choice(animais)
    
    # Correlacionar elemento e cor com a casa (para ficar mais realista)
    if casa == 'Gryffindor':
        row['elemento_preferido'] = random.choices(['Fogo', 'Ar'], weights=[0.8, 0.2], k=1)[0]
        row['cor'] = random.choices(['Vermelho', 'Dourado'], weights=[0.7, 0.3], k=1)[0]
    elif casa == 'Slytherin':
        row['elemento_preferido'] = random.choices(['Água', 'Terra'], weights=[0.8, 0.2], k=1)[0]
        row['cor'] = random.choices(['Verde', 'Prata'], weights=[0.7, 0.3], k=1)[0]
    elif casa == 'Ravenclaw':
        row['elemento_preferido'] = random.choices(['Ar', 'Água'], weights=[0.8, 0.2], k=1)[0]
        row['cor'] = random.choices(['Azul', 'Bronze'], weights=[0.7, 0.3], k=1)[0]
    else: # Hufflepuff
        row['elemento_preferido'] = random.choices(['Terra', 'Fogo'], weights=[0.8, 0.2], k=1)[0]
        row['cor'] = random.choices(['Amarelo', 'Preto'], weights=[0.7, 0.3], k=1)[0]

    # 3. Gerar Dados Numéricos (Baseado no Perfil da Casa)
    house_profile = profiles[casa]
    for stat in numerical_cols:
        # Pega o range (min, max) do perfil da casa. Se não estiver lá, usa (1, 10).
        min_val, max_val = house_profile.get(stat, (1, 10))
        row[stat] = get_stat(min_val, max_val)
        
    data.append(row)

# --- Criar DataFrame e Salvar CSV ---
df = pd.DataFrame(data)

# Reordenar colunas para a ordem solicitada
all_cols = categorical_cols + numerical_cols
df = df[all_cols]

# Salvar
output_filename = 'harry_potter_characters.csv'
df.to_csv(output_filename, index=False)

print(f"Base de dados salva com sucesso como '{output_filename}'!")