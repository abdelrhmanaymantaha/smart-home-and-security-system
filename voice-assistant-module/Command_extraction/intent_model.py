
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

from sklearn.svm import SVC



class SmartHomeIntentModel:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(ngram_range=(1,1))  # Using bigrams
        self.model = LogisticRegression(solver='liblinear', max_iter=5000, class_weight='balanced')
        self.model = SVC(kernel='linear', probability=True)  # Use SVM

    def load_data(self):
        """
        Loads the dataset from a JSON file and returns a DataFrame.
        """
        from TextPreProcessing import text_processing as tp
        import json
        
        try:
            # Construct the full path to dataset.json
            file_path = 'Command_extraction/dataset.json'  # Use forward slashes
            print(f"Loading data from: {file_path}")  # Debugging: Print the file path
            
            # Load the dataset from the JSON file
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            # Convert the data to a DataFrame
            df = pd.DataFrame(data)
            df['text'] = df['text'].apply(tp.text_preprocessor)
            print("Data loaded successfully!")  # Debugging: Confirm data is loaded
            print(df['intent'].value_counts())  # Check class distribution
            return df
        
        except Exception as e:
            print(f"Error loading data: {e}")
            return None

    def train(self, df):
        from sklearn.model_selection import GridSearchCV
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import classification_report


        X_train, X_test, y_train, y_test = train_test_split(df["text"], df["intent"], test_size=0.1, random_state=42, stratify=df["intent"])
        X_train_tfidf = self.vectorizer.fit_transform(X_train)
        X_test_tfidf = self.vectorizer.transform(X_test)

        # Define hyperparameters for tuning
        param_grid = {
            'C': [0.1, 1, 10],  # Regularization strength
            'penalty': ['l1', 'l2'],  # Regularization type
        }
        
        # Perform grid search
        grid_search = GridSearchCV(LogisticRegression(solver='liblinear',max_iter=5000), param_grid, cv=5, scoring='accuracy')
        grid_search.fit(X_train_tfidf, y_train)
        


        # Use the best model
        self.model = grid_search.best_estimator_
        
        # Print best parameters and accuracy
        print("Best Parameters:", grid_search.best_params_)
        print("Best Cross-Validation Accuracy:", grid_search.best_score_)
        
        # Evaluate the model
        y_pred = self.model.predict(X_test_tfidf)
        report = classification_report(y_test, y_pred, output_dict=True)
        print(classification_report(y_test, y_pred))
        # self.extract_feature_importance(X_train_tfidf, y_train)

        return report


    def save_model(self, model_path, vectorizer_path):
        import joblib
        joblib.dump(self.model, model_path)
        joblib.dump(self.vectorizer, vectorizer_path)

    def load_model(self, model_path, vectorizer_path):
        import joblib
        self.model = joblib.load(model_path)
        self.vectorizer = joblib.load(vectorizer_path)

    def predict_intent(self, text, threshold=0.5):
        text_tfidf = self.vectorizer.transform([text])
        probabilities = self.model.predict_proba(text_tfidf)
        max_prob = max(probabilities[0])
        print(f"Probability: {max_prob}")
        # print(f'probabilities: {probabilities}')
        print(f"Predicted Intent: {self.model.predict(text_tfidf)[0]}")
        if max_prob < threshold:
            return "unsupported"
        return self.model.predict(text_tfidf)[0]
    
    

    def extract_feature_importance(self, X_train_tfidf, y_train):
        """
        Extracts and visualizes feature importance (coefficients) for each class.
        """
        # Get feature names (words) from the vectorizer
        feature_names = self.vectorizer.get_feature_names_out()

        # Get coefficients from the logistic regression model
        coefficients = self.model.coef_

        # Iterate over each class and its corresponding coefficients
        for i, class_name in enumerate(self.model.classes_):
            print(f"\nClass: {class_name}")
            # Sort features by their absolute coefficient values (most important first)
            top_features = sorted(zip(feature_names, coefficients[i]), key=lambda x: abs(x[1]), reverse=True)[:20]  # Top 10 features
            for feature, coef in top_features:
                print(f"  {feature}: {coef:.4f}")

        # Visualize feature importance for a specific class
        # self.visualize_feature_importance(feature_names, coefficients)

    def visualize_feature_importance(self, feature_names, coefficients):
        """
        Visualizes feature importance using bar plots and heatmaps.
        """
        import matplotlib.pyplot as plt
        import seaborn as sns
        for i in range(6):      
            # Plot top features for a specific class
            class_index = i  # Index of the class you want to analyze
            top_n = 20  # Number of top features to display
            top_features = sorted(zip(feature_names, coefficients[class_index]), key=lambda x: abs(x[1]), reverse=True)[:top_n]
            features, importance = zip(*top_features)

            plt.figure(figsize=(10, 6))
            plt.barh(features, importance, color='skyblue')
            plt.xlabel('Coefficient Value')
            plt.title(f'Top {top_n} Features for Class: {self.model.classes_[class_index]}')
            plt.show()

        # Create a heatmap for all classes
        coef_df = pd.DataFrame(coefficients, columns=feature_names, index=self.model.classes_)
        plt.figure(figsize=(12, 8))
        sns.heatmap(coef_df, cmap='coolwarm', center=0)
        plt.title('Feature Importance (Coefficients) for Each Class')
        plt.xlabel('Features (Words)')
        plt.ylabel('Classes (Intents)')
        plt.show()

    
if __name__ == "__main__":
    from TextPreProcessing import text_processing as tp
    model = SmartHomeIntentModel()
    df = model.load_data()
    model.train(df)
    model.save_model("smart_home_intent_model.pkl", "tfidf_vectorizer.pkl")
    model.load_model("smart_home_intent_model.pkl", "tfidf_vectorizer.pkl")


    new_input = [
        "Turn off the living room lights",
        "open the lights in the living room",
        'open the livng room light',
        'Activate the lights in the living room',
        'Open the lights in the bedroom',
        'Open the light in the living room',
        'turn on the light in the bedroom',
        'what is the weather like in egypt',
        'turn on the lights in the living room',
        'open the door for the delevary',
        'lock the door ',
        'set the living room temperature for 25 ',
        'tell me a joke',
        'set the temperature in the living to 22',
        'add a new mode',
        'activate mode',
        'turn on the camera',
        'open the face id camera',


    ]
    for text in new_input:
        print(f"Input: {text}")
        text = tp.text_preprocessor(text)
        print(f"Processed text: {text}")
        intent = model.predict_intent(text)
        print(f"Predicted Intent: {intent}")
        print('-'*50)