import os


DEBUG = os.environ.get('DEBUG') == "True"
SIDE = os.environ.get('SIDE') or 0.02
VERIFY_URL = 'https://www.google.com/recaptcha/api/siteverify'
contatos = {"Caxias do Sul": {"email": "caxiasdosul@casamilitar.rs.gov.br", "orgao": "Defesa Civil de Caxias do Sul"},
            "Lageado": {"email": "defesacivil-lajeado@casamilitar.rs.gov.br", "orgao": "Defesa Civil de Lageado"},
            "Frederico Westphalen": {"email": "defesacivil-fwestphalen@casamilitar.rs.gov.br", "orgao": "Defesa Civil de Frederico Westphalen"},
            "Uruguaiana": {"email": "luiz-martins@casamilitar.rs.gov.br", "orgao": "Defesa Civil de Uruguaiana"},
            "Santo Ângelo": {"email": "defesacivil-santoangelo@casamilitar.rs.gov.br", "orgao": "Defesa Civil de Santo Ângelo"},
            "Pelotas": {"email": "defesacivil-regionalsul@casamilitar.rs.gov.br", "orgao": "Defesa Civil de Pelotas"},
            "Santa Maria": {"email": "defesacivil-santamaria@cm.rs.gov.br", "orgao": "Defesa Civil de Santa Maria"},
            "Passo Fundo": {"email": "defesacivil-passofundo@casamilitar.rs.gov.br", "orgao": "Defesa Civil de Passo Fundo"},
            "Porto Alegre": {"email": "defesacivil-metropolitana@casamilitar.rs.gov.br", "orgao": "Defesa Civil da Região Metropolitana"},
            "Brasilia": {"email": "alexlopespereira@gmail.com", "orgao": "Defesa Civil da Região Metropolitana"},
            "Canoas": {"email": "defesacivil-metropolitana@casamilitar.rs.gov.br", "orgao": "Defesa Civil da Região Metropolitana"}}
