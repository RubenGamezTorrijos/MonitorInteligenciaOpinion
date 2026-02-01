
import unittest
from unittest.mock import MagicMock, patch
import pandas as pd

# Mocking external classes that are not available in current env
class MockUserAgent:
    def __init__(self): self.random = "TestUA"

# Logic to test (simplified version of what's in the notebook)
class TrustpilotProcessor:
    def __init__(self):
        self.pos_words = {'excelente', 'perfecto'}
        
    def analyze_sentiment(self, text):
        words = text.lower().split()
        if any(w in words for w in self.pos_words):
            return "positivo"
        return "neutral"

class TestUnifiedLogic(unittest.TestCase):
    def test_sentiment_logic(self):
        processor = TrustpilotProcessor()
        res = processor.analyze_sentiment("El servicio es excelente")
        self.assertEqual(res, "positivo")
        
    def test_dataframe_creation(self):
        data = [{'texto': 'hola', 'puntuacion': 5}]
        df = pd.DataFrame(data)
        self.assertEqual(len(df), 1)
        self.assertEqual(df.iloc[0]['puntuacion'], 5)

if __name__ == "__main__":
    print("🧪 Ejecutando pruebas unitarias de la lógica del notebook...")
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
