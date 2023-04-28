import unittest
from flask_testing import TestCase
from main import app
from views import connection
from flask import url_for

class TestApp(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        return app

    def setUp(self):
        with connection.cursor() as cursor:
            cursor.execute("CREATE TEMPORARY TABLE animal AS SELECT * FROM animal;")
            cursor.execute("CREATE TEMPORARY TABLE usuarios AS SELECT * FROM usuarios;")

    def tearDown(self):
        with connection.cursor() as cursor:
            cursor.execute("DROP TABLE animal;")
            cursor.execute("DROP TABLE usuarios;")

    def test_home(self):
        response = self.client.get('/home/ufpe')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'ufpe', response.data)

    def test_login(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'login', response.data)

    def test_singup(self):
        response = self.client.get('/singup')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Cadastrar', response.data)

    def test_fetch_animals(self):
        response = self.client.get('/fetch_animals')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'[', response.data)

    def test_remove_animal(self):
        # Adicione um animal de teste ao banco de dados
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO animal (nome, especie, raca, idade, descricao, imagem, local_circulacao) VALUES ('Test', 'Dog', 'Bulldog', 2, 'Test Dog', 'images/test.jpg', 'Test Center');")
            cursor.execute("SELECT id FROM animal WHERE nome = 'Test' AND especie = 'Dog';")
            animal_id = cursor.fetchone()[0]

        response = self.client.post('/remove_animal', json={"id": animal_id})
        self.assertEqual(response.status_code, 302)

    def test_get_animal(self):
        # Adicione um animal de teste ao banco de dados
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO animal (nome, especie, raca, idade, descricao, imagem, local_circulacao) VALUES ('Test', 'Dog', 'Bulldog', 2, 'Test Dog', 'images/test.jpg', 'Test Center');")
            cursor.execute("SELECT id FROM animal WHERE nome = 'Test' AND especie = 'Dog';")
            animal_id = cursor.fetchone()[0]

        response = self.client.get(f'/animal/{animal_id}')
        self.assertEqual(response.status_code, 200)
        response_data = response.get_json()
        self.assertEqual(response_data["nome"], "Test")


if __name__ == '__main__':
    unittest.main()