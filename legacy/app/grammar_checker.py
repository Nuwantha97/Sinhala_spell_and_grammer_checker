from transformers import XLMRobertaTokenizer, XLMRobertaForSequenceClassification, XLMRobertaConfig
import pandas as pd
from datasets import Dataset
import os
import json
import numpy as np
import torch
import evaluate
from typing import Dict, List, Tuple
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix

class SinhalaGrammarChecker:
    def __init__(self):
        self.model_path = "models/model2"
        self.tokenizer = None
        self.model = None
        self.max_length = 512
        self.model_name = 'xlm-roberta-base'

    def preprocess_text(self, text: str) -> str:
        return text.strip()

    def tokenize_sentence(self, text: str) -> List[str]:
        return text.strip().split()

    def align_words(self, incorrect: str, correct: str) -> List[Tuple[str, str]]:
        incorrect_words = self.tokenize_sentence(incorrect)
        correct_words = self.tokenize_sentence(correct)
        return list(zip(incorrect_words, correct_words))

    def create_dataset(self, texts: List[str], labels: List[int]) -> Dataset:
        return Dataset.from_dict({
            'text': [self.preprocess_text(str(text)) for text in texts],
            'label': labels
        })

    def prepare_training_data(self, file_path: str) -> Tuple[Dataset, Dataset]:
        df = pd.read_csv(file_path)

        texts = []
        labels = []

        texts.extend(df['incorrect_sentence'].tolist())
        labels.extend([1] * len(df['incorrect_sentence']))

        texts.extend(df['correct_sentence'].tolist())
        labels.extend([0] * len(df['correct_sentence']))

        combined = list(zip(texts, labels))
        np.random.shuffle(combined)
        texts, labels = zip(*combined)

        split_idx = int(0.9 * len(texts))
        return (
            self.create_dataset(texts[:split_idx], labels[:split_idx]),
            self.create_dataset(texts[split_idx:], labels[split_idx:])
        )

    def tokenize_function(self, examples: Dict) -> Dict:
        tokenized = self.tokenizer(
            examples['text'],
            truncation=True,
            max_length=self.max_length,
            padding='max_length'
        )
        tokenized['labels'] = examples['label']
        return tokenized

    def compute_metrics(self, eval_pred: Tuple) -> Dict:
        predictions, labels = eval_pred
        predictions = np.argmax(predictions, axis=1)

        metrics = {}
        accuracy = evaluate.load("accuracy")
        metrics.update(accuracy.compute(predictions=predictions, references=labels))

        metrics['precision'] = float(precision_score(labels, predictions, average='binary'))
        metrics['recall'] = float(recall_score(labels, predictions, average='binary'))
        metrics['f1'] = float(f1_score(labels, predictions, average='binary'))

        return metrics

    def initialize_model_and_tokenizer(self):
        # Initialize tokenizer
        self.tokenizer = XLMRobertaTokenizer.from_pretrained(
            self.model_name,
            model_max_length=self.max_length
        )

        # Initialize config with explicit values to ensure consistency
        config = XLMRobertaConfig(
            num_labels=2,
            vocab_size=self.tokenizer.vocab_size,  # Use tokenizer's vocab size
            max_position_embeddings=self.max_length + 2, # Accommodate special tokens
            type_vocab_size=1  # Ensure consistency
        )

        # Initialize model with config
        self.model = XLMRobertaForSequenceClassification.from_pretrained(
            self.model_name,
            config=config,
            ignore_mismatched_sizes=True
        )

    def load_model(self, load_path: str = None) -> None:
        load_path = load_path or self.model_path
        if not os.path.exists(load_path):
            raise ValueError(f"Model path {load_path} does not exist")

        # Load configuration
        with open(os.path.join(load_path, 'config.json'), 'r') as f:
            config_dict = json.load(f)

        # Load tokenizer and config, using saved values
        self.tokenizer = XLMRobertaTokenizer.from_pretrained(
            load_path,
            model_max_length=config_dict['max_length']
        )

        config = XLMRobertaConfig.from_pretrained(
            load_path,
            num_labels=config_dict['num_labels'],
            vocab_size=config_dict['vocab_size'],  # Use saved vocab size
            max_position_embeddings=config_dict['max_position_embeddings'],  # Use saved max position embeddings
            type_vocab_size=config_dict['type_vocab_size']  # Use saved token type embeddings size
        )

        # Load model with config
        self.model = XLMRobertaForSequenceClassification.from_pretrained(
            load_path,
            config=config,
            ignore_mismatched_sizes=True
        )

        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model = self.model.to(device)

    def check_grammar(self, text: str, df: pd.DataFrame) -> Dict:
        if not self.model or not self.tokenizer:
            self.load_model()

        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = self.model.to(device)

        text = self.preprocess_text(text)
        words = self.tokenize_sentence(text)

        try:
            inputs = self.tokenizer(
                text,
                return_tensors="pt",
                truncation=True,
                max_length=self.max_length,
                padding='max_length'
            )

            inputs = {k: v.to(device) for k, v in inputs.items()}

            with torch.no_grad():
                outputs = self.model(**inputs)
                predictions = torch.softmax(outputs.logits, dim=1)
                has_error = torch.argmax(predictions).item()
                confidence = predictions[0][has_error].item()

            correction = None
            problematic_words = []

            if has_error == 1:
                correction = self.get_correction(text, df)
                if correction:
                    word_alignments = self.align_words(text, correction)
                    for i, (incorrect, correct) in enumerate(word_alignments):
                        if incorrect != correct:
                            problematic_words.append({
                                'word': incorrect,
                                'position': i,
                                'correction': correct
                            })

            return {
                'text': text,
                'has_error': bool(has_error),
                'confidence': confidence,
                'correction': correction,
                'problematic_words': problematic_words,
                'suggestion': correction if correction else ('Grammatical error detected' if has_error else 'No grammatical errors detected.')
            }

        except Exception as e:
            print(f"Error during grammar checking: {str(e)}")
            return {
                'text': text,
                'has_error': None,
                'confidence': None,
                'error': str(e)
            }

    def get_correction(self, text: str, df: pd.DataFrame) -> str:
        match = df[df['incorrect_sentence'] == text]
        return match.iloc[0]['correct_sentence'] if not match.empty else None


