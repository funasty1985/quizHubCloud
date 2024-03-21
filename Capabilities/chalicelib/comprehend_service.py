# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 18:27:16 2024

@author: 8778t
"""

import boto3

class ComprehendService:
    def __init__(self):
        self.comprehend = boto3.client(service_name='comprehend')

    def extract_key_phrases(self, text):
        response = self.comprehend.detect_key_phrases(Text=text, LanguageCode='en')
        
        key_phrases = [phrase['Text'] for phrase in response['KeyPhrases']]
        return key_phrases
