"""
Model Factory module for AI Behavioral Guidelines
Provides DecisionTree and RandomForest model implementations
"""

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score, recall_score
import pickle
from typing import Tuple, Dict
import numpy as np


class ModelBase:
    """Base class for all models"""
    
    def __init__(self):
        self.model = None
        self.model_name = "BaseModel"
    
    def train(self, X_train: np.ndarray, y_train: np.ndarray):
        """Train the model"""
        if self.model is None:
            raise ValueError("Model not initialized")
        self.model.fit(X_train, y_train)
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Make predictions"""
        if self.model is None:
            raise ValueError("Model not trained")
        return self.model.predict(X)
    
    def evaluate(self, X_test: np.ndarray, y_test: np.ndarray) -> Dict[str, float]:
        """Evaluate model performance"""
        y_pred = self.predict(X_test)
        precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
        recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
        
        return {
            'precision': precision,
            'recall': recall,
            'f1_score': 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        }
    
    def save(self, filepath: str):
        """Save model to file"""
        with open(filepath, 'wb') as f:
            pickle.dump(self.model, f)
    
    def load(self, filepath: str):
        """Load model from file"""
        with open(filepath, 'rb') as f:
            self.model = pickle.load(f)


class DecisionTreeModel(ModelBase):
    """Decision Tree model implementation"""
    
    def __init__(self, max_depth: int = 10, random_state: int = 42):
        super().__init__()
        self.model = DecisionTreeClassifier(
            max_depth=max_depth,
            random_state=random_state
        )
        self.model_name = "DecisionTree"


class RandomForestModel(ModelBase):
    """Random Forest model implementation"""
    
    def __init__(self, n_estimators: int = 100, max_depth: int = 10, random_state: int = 42):
        super().__init__()
        self.model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            random_state=random_state
        )
        self.model_name = "RandomForest"


def get_model(model_type: str) -> ModelBase:
    """Factory function to get model instance"""
    models = {
        'decision_tree': DecisionTreeModel,
        'random_forest': RandomForestModel
    }
    
    if model_type not in models:
        raise ValueError(f"Unknown model type: {model_type}. Available: {list(models.keys())}")
    
    return models[model_type]()
