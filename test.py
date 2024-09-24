from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False

    def test_home(self):
        with self.client:
            response = self.client.get('/')
            html = response.get_data(as_text=True)
            
            #test correct rendering and status
            self.assertEqual(response.status_code, 200)
            self.assertIn("<table class=\"board\">", html)
            self.assertIn("Score:", html)
            
            #test that a board has been created and is in session
            self.assertIsNotNone(session['board'])
            #test the presence of the top score and times played in session
            self.assertNotIn('topscore', session)
            self.assertIn('times_played', session)
            
            
    def test_valid_word(self):
        """Test if word is valid by modifying the board in the session."""
        
        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [['C', 'A', 'T', 'T', 'T'],
                                ['C', 'A', 'T', 'T', 'T'],
                                ['C', 'A', 'T', 'T', 'T'],
                                ['C', 'A', 'T', 'T', 'T'],
                                ['C', 'A', 'T', 'T', 'T']]
            resp = self.client.get('/check-word?word=cat')
            self.assertEqual(resp.json['result'], 'ok')
            
            
    def test_invalid_word(self):
        """Test if word is in dictionary"""
        
        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [['C', 'A', 'T', 'T', 'T'],
                                ['C', 'A', 'T', 'T', 'T'],
                                ['C', 'A', 'T', 'T', 'T'],
                                ['C', 'A', 'T', 'T', 'T'],
                                ['C', 'A', 'T', 'T', 'T']]
        resp = self.client.get('/check-word?word=impossible')
        self.assertEqual(resp.json['result'], 'not-on-board')
        
        
    def non_english_word(self):
        """Test if word is on board"""
        self.client.get('/')
        resp = self.client.get('/check-word?word=fsjdakfkldsfjdslkfjdlksf')
        self.assertEqual(resp.json['result'], 'not-word')
            
            
    def test_check_word(self):
        """Test to check the check word route."""
        with self.client as client:
            with client.session_transaction() as change_session:
                change_session['board'] = [
                    ['A', 'B', 'C', 'D', 'E'],
                    ['F', 'G', 'H', 'I', 'J'],
                    ['K', 'L', 'M', 'N', 'O'],
                    ['P', 'Q', 'R', 'S', 'T'],
                    ['U', 'V', 'W', 'X', 'Y']
                ]
        response = self.client.get('/check-word?word=word')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['result'], 'not-on-board')
        response = client.get('/check-word?word=')
        self.assertEqual(response.get_json()['result'], 'not-word')
        
        
    def test_empty_word(self):
        """Check for empty word submit"""
        with self.client as client:
            with client.session_transaction() as change_session:
                change_session['board'] = [
                    ['A', 'B', 'C', 'D', 'E'],
                    ['F', 'G', 'H', 'I', 'J'],
                    ['K', 'L', 'M', 'N', 'O'],
                    ['P', 'Q', 'R', 'S', 'T'],
                    ['U', 'V', 'W', 'X', 'Y']
                    ]
            resp = self.client.get('/check-word?word=')
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.json['result'], 'not-word')
        
        
    def test_submit_score(self):
        """Test to check the submit score route."""
        with self.client as client:
            with client.session_transaction() as session:
                session['topscore'] = 0
            response = self.client.post('/submit-score', json={'score': 5})
            
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['beatHighScore'], True)

    # TODO -- write tests for every view function / feature!

